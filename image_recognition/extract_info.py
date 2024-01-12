import base64
import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel, Image, Part
from  PIL.PpmImagePlugin import PpmImageFile
import io
import os

#from PIL.PpmImagePlugin import PpmImageFile

#PIL.PpmImagePlugin.PpmImageFile

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
  

def extract_json_from_table(pdf_page_image: PpmImageFile) -> str:
  """Extracts JSON from a PDF page image.

  Args:
    pdf_page_image: The PDF page image to extract JSON from.

  Returns:
    The extracted JSON as string
  """

    #Initilize variables
  final_response:str = ""
  multimodal_model = GenerativeModel ("gemini-pro-vision")

  #pdf_page_image = Image.load_from_file("tmp_2022-alphabet-annual-report_5e2355d1-af95-467a-97f6-1741a10e9217/images/page96.jpg")
  pdf_page_image = convert_ppm_to_vertexImage (pdf_page_image)

  # We try first restrictive prompt (because we whave better quality answer) If no output, then we will go with less restrictive prompt
  restrictive_prompt = True
  #prompt = "Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data, all the columns and rows faithfully represented as well as the headers."
  prompt = ["""Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data.""","""Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data, all the columns and rows faithfully represented as well as the headers. 
              Consistency of the format is key and the output format should always be as followed: every single table will have a JSON Document starting only with '```json' and end '```'""" ]
  
  contents = [
      pdf_page_image,
      prompt[int(restrictive_prompt)],
  ]

  # We test first with restrictive prompt then with relax prompt if no answers with restrictive prompt.
  responses = multimodal_model.generate_content(
        contents,  
        generation_config={
          "max_output_tokens": 2048,
          "temperature": 0,
          "top_p": 1,
          "top_k": 1
          },
      stream=True)
  
  # Force early evaluation
  responses = list(responses)
  
  # Here we test if the restricitve prompt returns a result.
  # If it doesn't then it tries again with relax prompt
  if len(responses) > 0:
    for response in responses:
        final_response = final_response + response.candidates[0].content.parts[0].text
    return final_response
  else:
    print("restrictive prompt failed. len(responses) = " + len(responses))
    restrictive_prompt = False
    responses = multimodal_model.generate_content(
          contents,  
          generation_config={
            "max_output_tokens": 2048,
            "temperature": 0,
            "top_p": 1,
            "top_k": 1
            },
        stream=True)    # Force early evaluation
    responses = list(responses)
    if len (responses) > 0:
      final_response = final_response + response.candidates[0].content.parts[0].text
      return final_response
    else:
       # If even relax prompt fails then we return the empty string
       return final_response


def description_from_json(json_string: str) -> str:

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
  \"Google Revenues diversification, 2020, 2021, 2022.\"""".format(json_string),
      **parameters
  )

  return response.text
