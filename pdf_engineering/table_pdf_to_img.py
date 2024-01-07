import fitz  # import package PyMuPDF
from vertexai.preview.generative_models import GenerativeModel, Part
from PIL import Image as PIL_Image
from pdf2image import convert_from_bytes
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
  
def convert_pdf_page_with_table_to_image(pdf_file):
    images = convert_from_bytes(pdf_file.download_as_bytes())
    return images