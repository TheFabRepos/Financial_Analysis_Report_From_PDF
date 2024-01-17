import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel, Image, Part
from  PIL.PpmImagePlugin import PpmImageFile
import io
import os
import google.api_core.exceptions as google_exceptions
from ratelimit import limits, sleep_and_retry
from backoff import on_exception, expo
import generic_helper.helper as generic_helper
import json
import streamlit as st
import time


def convert_ppm_to_vertexImage(ppm_image: PpmImageFile) -> Image:
  """Converts a PPM image to a Vertex AI Image object.

  Args:
    ppm_image: The PPM image to convert.

  Returns:
    The Vertex AI Image object.
  """
  imgByteArr = io.BytesIO()
  ppm_image.save(imgByteArr, format='JPEG')
  imgByteArr = imgByteArr.getvalue()
  ppm_image = Image.from_bytes(imgByteArr)
  return ppm_image

def extract_json_from_table_with_iteration (list_page_table, list_images, temp_directory, filename_with_extension, logtxtbox:st.empty =None):

  for count, page in enumerate(list_page_table):
    json_tables_string:str = extract_json_from_table(list_images[page])
    # Do string cleanup before converting to JSON object
    # Remove backtick if it exists because Python does not like it
    json_tables_string:str = generic_helper.remove_backticks(json_tables_string)
    list_json_doc:list[str] = generic_helper.get_list_json_doc(json_tables_string)
    #time.sleep(15)
    for table_number, json_doc  in enumerate(list_json_doc):
      description:str = description_from_json_bison(json_doc)
      source:str = "{}_page_{}_table_{}".format(filename_with_extension,page,table_number+1)
      json_doc = generic_helper.insert_string_in_json_doc(json_doc, description, source)
      # Save the JSON file
      with open("{}/json/{}_page{}_table{}.jsonl".format(temp_directory, filename_with_extension, page, table_number+1), "w") as fp:
        json.dump(json_doc, fp)
    if logtxtbox != None:
      logtxtbox.write(f"{st.session_state.filename_with_extension} - {count+1} page(s) with table(s) extracted to JSON ...") 


def extract_json_from_table(pdf_page_image: PpmImageFile) -> str:
  """Extracts JSON from a PDF page image.

  Args:
    pdf_page_image: The PDF page image to extract JSON from.

  Returns:
    The extracted JSON as string
  """
  multimodal_model = GenerativeModel ("gemini-pro-vision")
  text_model = TextGenerationModel.from_pretrained("text-bison")

  #pdf_page_image = Image.load_from_file("tmp_2022-alphabet-annual-report_5e2355d1-af95-467a-97f6-1741a10e9217/images/page96.jpg")
  pdf_page_image = convert_ppm_to_vertexImage (pdf_page_image)

  #pdf_page_image
  final_answer = json_from_table_image_using_geminivision(multimodal_model, pdf_page_image, True)

  if final_answer != "":
    return final_answer
  else:
    return json_from_table_image_using_geminivision(multimodal_model, pdf_page_image, False)

  
# rate is 1 QPS.
#@sleep_and_retry # If there are more request to this function than rate, sleep shortly
#@on_exception(expo, google_exceptions.ResourceExhausted, max_tries=10) # if we receive exceptions from Google API, retry
#@limits(calls=60, period=60)
def json_from_table_image_using_geminivision(multimodal_model:GenerativeModel, pdf_page_image: PpmImageFile, restrictive_prompt:bool ) -> str:
  #Initilize variables
  final_response:str = ""
  multimodal_prompt = ["""Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data.""","""Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data, all the columns and rows faithfully represented as well as the headers. 
              Consistency of the format is key and the output format should always be as followed: every single table will have a JSON Document starting only with '```json' and end '```'""" ]
  
  contents = [
      pdf_page_image,
      multimodal_prompt[int(restrictive_prompt)],
  ]
  responses = multimodal_model.generate_content(
      contents,  
      generation_config={
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1,
        "top_k": 1
        },
    stream=True)
  
  try:
    responses = list(responses)
  except:
    print("Exception occured")
    return ''
  
  if len(responses) > 0:
    for response in responses:
        final_response = final_response + response.candidates[0].content.parts[0].text
    return final_response    
  else:
    return ''

#@sleep_and_retry # If there are more request to this function than rate, sleep shortly
#@on_exception(expo, google_exceptions.ResourceExhausted, max_tries=10) # if we receive exceptions from Google API, retry
#@limits(calls=4, period=60)
def description_from_json_bison(json_string: str) -> str:

  LOCATION=os.getenv('LOCATION')
  PROJECT=os.getenv('PROJECT_ID')
  
  #vertexai.init(project=PROJECT, location=LOCATION)
  vertexai.init(project=PROJECT, location=LOCATION)
  parameters = {
      "candidate_count": 1,
      "max_output_tokens": 400,
      "temperature": 0,
      "top_p": 1
  }
  model = TextGenerationModel.from_pretrained("text-bison")
  response = model.predict(
      """Provide the one best possible 20 words description, including every single year for which the following JSON document applies:

  {}

  Output example:
  "Google Revenues diversification, 2020, 2021, 2022.\"""".format(json_string),
      **parameters
  )

  return response.text
