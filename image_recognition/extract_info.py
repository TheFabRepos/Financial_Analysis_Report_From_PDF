import base64
import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel, Image, Part
from  PIL.PpmImagePlugin import PpmImageFile
import io

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

  final_response = ""
  multimodal_model = GenerativeModel ("gemini-pro-vision")

  #pdf_page_image = Image.load_from_file("tmp_2022-alphabet-annual-report_5e2355d1-af95-467a-97f6-1741a10e9217/images/page96.jpg")
  pdf_page_image = convert_ppm_to_vertexImage (pdf_page_image)
  
  prompt = "Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data, all the columns and rows faithfully represented as well as the headers."
  contents = [
      prompt,
      pdf_page_image
  ]

  responses = multimodal_model.generate_content(contents, stream=True)

  for response in responses:
        final_response = final_response + response.candidates[0].content.parts[0].text

  return final_response

def create_image_description_from_table(pdf_page_image: PpmImageFile) -> str:
  """Extracts JSON from a PDF page image.

  Args:
    pdf_page_image: The PDF page image to extract JSON from.

  Returns:
    The extracted JSON as string
  """

  final_response = ""
  multimodal_model = GenerativeModel ("gemini-pro-vision")

  #pdf_page_image = Image.load_from_file("tmp_2022-alphabet-annual-report_5e2355d1-af95-467a-97f6-1741a10e9217/images/page96.jpg")
  pdf_page_image = convert_ppm_to_vertexImage (pdf_page_image)
  
  #prompt = "Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data, all the columns and rows faithfully represented as well as the headers."
  prompt = """Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data, all the columns and rows faithfully represented as well as the headers. 
              Consistency of the format is key and the output format should always be as followed: every single table will have a JSON Document starting only with '```json' and end '```'"""
  contents = [
      prompt,
      pdf_page_image
  ]

  generation_config={
        "max_output_tokens": 2048,
        "temperature": 0,
        "top_p": 1,
        "top_k": 1
        }

  responses = multimodal_model.generate_content(contents, generation_config, stream=True)

  for response in responses:
        final_response = final_response + response.candidates[0].content.parts[0].text

  return final_response


def description_from_json(json_string: str) -> str:

  vertexai.init(project="testfab-362608", location="us-central1")
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
