from vertexai.preview.generative_models import GenerativeModel, Part
import pdf_engineering.table_pdf_to_img as pdf_engineering
import generic_helper.helper as generic_helper

import image_recognition.extract_info as extract_info

import os
import shutil

from vertexai.preview.generative_models import GenerativeModel, Part
from PIL import Image as PIL_Image
from pdf2image import convert_from_path





    #for i in list_page_table:
    #  images[i].save("{}/images/page{}.jpg".format(temp_directory, i))
      


if __name__ == "__main__":

  # Get the list of PDF file in a bucket folder (or the whole bucket if folder is a specific not provided)
  list_pdf_files = pdf_engineering.list_pdf_files_in_GCS ("fabgoldendemo", "report")

  # Convert each PDF file to a list of images (but only the pages which contains a table)
  for pdf_file in list_pdf_files:
    #Identify the page with table(s) in the current processed PDF file
    list_page_table = pdf_engineering.list_table_in_pdf(list_pdf_files)

    #Extract the file name (with extension but without folder name)
    filename_with_extension = (pdf_file.name.split("/")[-1])
    #Extract the file name (without extension or folder name)
    filename_only = (pdf_file.name.split("/")[-1]).split(".")[0]
    
    # create temp local directory to work with images
    #temp_directory = generic_helper.create_tmp_directory (filename_only)
    list_images = pdf_engineering.convert_pdf_page_with_table_to_image(pdf_file)
    

    #Do for every list item
    page=96
    #i=93
    json_tables_string = extract_info.extract_json_from_table(list_images[page])

    # Do string cleanup before converting to JSON object
    # Remove backtick if it exists because Python does not like it
    json_tables_string = generic_helper.remove_backticks(json_tables_string)

    # Replace rounded parentheses with minus symbol for negative numbers because JSON does not like it
    json_tables_string = generic_helper.replace_numbers_between_parentheses(json_tables_string)

    # 
    list_json_oject_table = generic_helper.convert_string_to_json (json_tables_string)
    
    for table_number, json_object in enumerate(list_json_oject_table):
      description = extract_info.description_from_json(json_object)
      json_object['description'] = description
      json_object['source'] = "{}_page_{}_table_{}".format(filename_with_extension,page,table_number+1)
      print(json_object)

      print(description)











    #print(json_table_string)


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

