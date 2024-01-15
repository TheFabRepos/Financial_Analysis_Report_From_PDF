import streamlit as st

from vertexai.preview.generative_models import GenerativeModel, Part
import pdf_engineering.table_pdf_to_img as pdf_engineering
import generic_helper.helper as generic_helper

import image_recognition.extract_info as extract_info

import json
import shutil

from vertexai.preview.generative_models import GenerativeModel, Part
from PIL import Image as PIL_Image
from pdf2image import convert_from_path




def process_file():
    progressbar = st.progress(25, text = "Listing tables in PDF file...")
    #Find all thepage which got at least one table
    list_page_table = pdf_engineering.list_table_in_pdf_from_file(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}")
    logtxtbox = st.empty()
    logtxtbox.caption(f"{len(list_page_table)} pages containing tables found in {st.session_state.filename_with_extension}...") 
    #Convert the whole pdf file in images
    progressbar.progress(50, text = "Converting PDF file to images...")
    list_images = pdf_engineering.convert_pdf_page_with_table_to_image_from_file(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}")
    
    #Do for every page in the pdf file

    progressbar.progress(75, text = f"Extracting JSON from tables")

    for count, page in enumerate(list_page_table):
      json_tables_string:str = extract_info.extract_json_from_table(list_images[page])

      # Do string cleanup before converting to JSON object
      # Remove backtick if it exists because Python does not like it
      json_tables_string:str = generic_helper.remove_backticks(json_tables_string)

      list_json_doc:str = generic_helper.get_list_json_doc(json_tables_string)

      # Replace rounded parentheses with minus symbol for negative numbers becauextracted jsonse JSON does not like it
      #json_tables_string = generic_helper.replace_numbers_between_parentheses(json_tables_string)

      #filename_with_extension, filename_only = generic_helper.extract_filename (pdf_file.name)

      # Convert the string to a JSON object
      #list_json_oject_table = generic_helper.convert_string_to_json (page, json_tables_string)
      

      
      for table_number, json_doc  in enumerate(list_json_doc):


        description:str = extract_info.description_from_json(json_doc)
        source:str = "{}_page_{}_table_{}".format(st.session_state.filename_with_extension,page,table_number+1)
        json_doc = generic_helper.insert_string_in_json_doc(json_doc, description, source)
        # Save the JSON file
        with open("{}/json/{}_page{}_table{}.jsonl".format(st.session_state.temp_directory, st.session_state.filename_with_extension, page, table_number+1), "w") as fp:
          json.dump(json_doc, fp)
      
      
      logtxtbox.caption(f"""{len(list_page_table)} pages containing tables found in {st.session_state.filename_with_extension}... {count+1} processed out of {len(list_page_table)}""") 
  
    progressbar.progress(100, text = f"Embedding extracted json...")
    


    # for page in list_page_table:
    #   json_tables_string:str = extract_info.extract_json_from_table(list_images[page])

    #   # Do string cleanup before converting to JSON object
    #   # Remove backtick if it exists because Python does not like it
    #   json_tables_string:str = generic_helper.remove_backticks(json_tables_string)
    #   list_images = pdf_engineering.




     #titleProgressImage.write ("Listing tables in PDF file...")









st.write("# Import statement for analysis")
st.write("---")


file_uploader = st.empty()

if 'uploaded_already' not in st.session_state:
         st.session_state.uploaded_already = False
         st.session_state.filename_with_extension = ""
         st.session_state.temp_directory = ""

uploaded_file:str = file_uploader.file_uploader("Choose a PDF file", accept_multiple_files=False, type=['pdf'], key='uploader_key')

#uploaded_file:str = st.file_uploader("Choose a PDF file", accept_multiple_files=False, type=['pdf'], key='uploader_key', disabled=st.session_state.file_uploader_disabled)

if st.session_state.uploaded_already == False:
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()

        #Extract the file name (with extension but without folder name)
        st.session_state.filename_with_extension = uploaded_file.name
        #Extract the file name (without extension or folder name)
        filename_only = uploaded_file.name.split(".")[0]

        
        # create temp local directory to store teh resulting json file
        st.session_state.temp_directory = generic_helper.create_tmp_directory (filename_only)
        with open(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}", "wb") as f:
            f.write(bytes_data)
        st.session_state.uploaded_already = True
        file_uploader.empty()
        st.subheader('Uploaded files')
        st.success(f'files uploaded {st.session_state.filename_with_extension}')


if st.session_state.uploaded_already == True:
    file_uploader.empty()
    st.write(f"File {st.session_state.filename_with_extension} uploaded successfully...")
    st.button("Ready to process 📝...", on_click=process_file)






