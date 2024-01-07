import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image, Part
from  PIL.PpmImagePlugin import PpmImageFile
import io

#from PIL.PpmImagePlugin import PpmImageFile

#PIL.PpmImagePlugin.PpmImageFile

def convert_ppm_to_vertexImage(ppm_image: PpmImageFile) -> Image:

  imgByteArr = io.BytesIO()
  ppm_image.save(imgByteArr, format='JPEG')
  imgByteArr = imgByteArr.getvalue()
  ppm_image = Image.from_bytes(imgByteArr)
  return ppm_image
  


def extract_json_from_table(pdf_page_image: PpmImageFile) -> str:

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


