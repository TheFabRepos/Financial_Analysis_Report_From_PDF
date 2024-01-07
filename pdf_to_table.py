from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai
import os
import io
import tempfile
import fitz  # import package PyMuPDF
import uuid
import pdf_engineering

from vertexai.preview.generative_models import GenerativeModel, Part
from PIL import Image as PIL_Image
from pdf2image import convert_from_path
import pdf2image
from google.cloud import storage





if __name__ == "__main__":

  # Get the list of PDF file in a bucket folder (or the whole bucket if folder is a specific not provided)
  list_pdf_files = pdf_engineering.list_pdf_files_in_GCS ("fabgoldendemo", "report")


  # Convert each PDF file to a list of images (but only the pages which contains a table)
  for pdf_file in list_pdf_files:
    #Identify the page with table(s) in the current processed PDF file
    list_page_table = pdf_engineering.list_table_in_pdf (list_pdf_files)

    #Extract the file name (without extension or folder name)
    filename_only = (pdf_file.name.split("/")[-1]).split(".")[0]

    # crete temp local directory to work with images
    temp_directory = pdf_engineering.create_tmp_directory (filename_only)


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

