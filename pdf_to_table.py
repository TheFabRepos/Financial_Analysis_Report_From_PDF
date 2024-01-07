from vertexai.preview.generative_models import GenerativeModel, Part
import pdf_engineering.table_pdf_to_img as pdf_engineering
import generic_helper.helper as generic_helper

import image_recognition.extract_info as extract_info_from_image

import os
import shutil

from vertexai.preview.generative_models import GenerativeModel, Part
from PIL import Image as PIL_Image
from pdf2image import convert_from_path





    #for i in list_page_table:
    #  images[i].save("{}/images/page{}.jpg".format(temp_directory, i))
      


if __name__ == "__main__":

  # Get the list of PDF file in a bucket folder (or the whole bucket if folder is a specific not provided)
  list_pdf_files =pdf_engineering.list_pdf_files_in_GCS ("fabgoldendemo", "report")

  # Convert each PDF file to a list of images (but only the pages which contains a table)
  for pdf_file in list_pdf_files:
    #Identify the page with table(s) in the current processed PDF file
    list_page_table = pdf_engineering.list_table_in_pdf (list_pdf_files)

    #Extract the file name (without extension or folder name)
    filename_only = (pdf_file.name.split("/")[-1]).split(".")[0]

    # create temp local directory to work with images
    #temp_directory = generic_helper.create_tmp_directory (filename_only)
    list_images = pdf_engineering.convert_pdf_page_with_table_to_image(pdf_file)
    
    answer = extract_info_from_image.extract_json_from_table(list_images[96])

    print(answer)


    # Save the images in the temp directory
    #for i in list_page_table:
      # Save the images in the temp directory for debugging purpose
      #list_images[i].save("{}/images/page{}.jpg".format(temp_directory, i))




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

