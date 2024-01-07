from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai
import os
import io
import tempfile
import fitz  # import package PyMuPDF
import uuid

from vertexai.preview.generative_models import GenerativeModel, Part
from PIL import Image as PIL_Image
from pdf2image import convert_from_path
import pdf2image
from google.cloud import storage


def list_pdf_files_in_GCS(bucket_name, folder_name) -> list[storage.Blob]:
  """Lists all the PDF files in a specific folder of a Google Cloud Storage bucket.

  Args:
    bucket_name: The name of the Google Cloud Storage bucket.
    folder_name: The name of the folder to list the files from.

  Returns:
    A list of all the PDF files in the specified folder.
  """

  # Create a client.
  storage_client = storage.Client()

  # Get a list of all the objects in the bucket.
  objects = storage_client.list_blobs(bucket_name)

  # Filter the list of objects to only include PDF files.
  pdf_files = [object for object in objects if object.content_type == "application/pdf"]

  # Filter the list of objects to only include objects in the specified folder.
  folder_objects = [object for object in pdf_files if object.name.startswith(folder_name)]

  return folder_objects

  # Return the list of objects in the specified folder.
  # return [object.name for object in folder_objects]


def load_image(image_path):
  image = PIL_Image.open(image_path)
  return image

def convert_pdf_to_image(pdf_path: str)-> list[str]:
  """Converts a PDF file to a list of JPEG files.

  Args:
      pdf_path: The path to the PDF file.

  Returns:
      A list of the paths to the JPEG files.
  """

  # Convert the PDF file to a list of images.
  pdf_path = "gs://fabgoldendemo/report/2022-alphabet-annual-report.pdf"

  # Convert the PDF file to a list of images
  #images = convert_from_path(pdf_path)

  return images


def list_table_in_pdf(list_pdf_files:list[storage.Blob]) -> list[int]:
  """Lists all the tables in a PDF file.

  Args:
    pdf_file: The PDF file to list the tables from.

  Returns:
    A list of the tables in the PDF file.
  """

  page_list = []

  for pdf_file in list_pdf_files:
    doc = fitz.open("pdf", pdf_file.download_as_bytes())
    for page in doc:
      tabs = page.find_tables()
      if len(tabs.tables) > 0:
        page_list.append(page.number) #index start at 0
                   
  return page_list
  
def create_tmp_directory(filename_only):

  temp_directory = "{}/tmp_{}_{}".format(os.getcwd(),filename_only,str(uuid.uuid4()))
  os.makedirs(temp_directory, exist_ok=True)
  os.makedirs(os.path.join(temp_directory, "images"), exist_ok=True)
  os.makedirs(os.path.join(temp_directory, "json"), exist_ok=True)

  return temp_directory


if __name__ == "__main__":

  # Get the list of PDF file in a bucket folder (or the whole bucket if folder is a specific not provided)
  list_pdf_files = list_pdf_files_in_GCS ("fabgoldendemo", "report")


  # Convert each PDF file to a list of images (but only the pages which contains a table)
  for pdf_file in list_pdf_files:
    #Identify the page with table(s) in the current processed PDF file
    list_page_table = list_table_in_pdf (list_pdf_files)

    #Extract the file name (without extension or folder name)
    filename_only = (pdf_file.name.split("/")[-1]).split(".")[0]

    # crete temp local directory to work with images
    temp_directory = create_tmp_directory (filename_only)


    images = pdf2image.convert_from_bytes(pdf_file.download_as_bytes())
    for i in list_page_table:
      images[i].save("{}/images/page{}.jpg".format(temp_directory, i))


  #shutil.rmtree(temp_directory)




#  val = convert_pdf_to_image("./images/2022-alphabet-annual-report.pdf") 

#  print (val)
  
  
  
    # Store Pdf with convert_from_path function
  #images = convert_from_path('./images/2022-alphabet-annual-report.pdf')
  
  #for i in range(len(images)):
    
        # Save pages as images in the pdf
  #images[i].save('./images/'+'page'+ str(i) +'.jpg', 'JPEG')
      #print(i)
      #images[i].save('page'+ str(i) +'.jpg', 'JPEG')

    
# https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/use-cases/retail/multimodal_retail_recommendations.ipynb
# https://realpython.com/image-processing-with-the-python-pillow-library/

