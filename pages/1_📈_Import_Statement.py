import streamlit as st

import pdf_engineering.table_pdf_to_img as pdf_engineering
import generic_helper.helper as generic_helper

import image_recognition.extract_info as extract_info

import json
from embedding_helper import pgvector_embedding
import time


def process_file():
    logtxtbox = st.empty()
    logtxtbox.write("") 
    progressbar = st.progress(0, text = "")

    with st.spinner(text = f"Searching page(s) with table(s) in {st.session_state.filename_with_extension}..."):
    #Find all thepage which got at least one table
      list_page_table = pdf_engineering.list_table_in_pdf_from_file(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}")
      logtxtbox.write(f"##### {len(list_page_table)} pages containing tables found in {st.session_state.filename_with_extension}...") 
    progressbar = progressbar.progress(0.25, text = "Page containing tables in PDF file have been found...")

    with st.spinner(text = "Converting pages in PDF files to images..."):
      list_images = pdf_engineering.convert_pdf_page_with_table_to_image_from_file(f"{st.session_state.temp_directory}/{st.session_state.filename_with_extension}")
    progressbar.progress(0.5, text = "Pages in PDF file has been converted to images ...")
    
    #Do for every page in the pdf file

    with st.spinner(text = "Extracting json from tables found in PDF file..."):
      extract_info.extract_json_from_table_with_iteration (list_page_table, list_images, st.session_state.temp_directory, st.session_state.filename_with_extension, logtxtbox)
    progressbar.progress(0.75, text = "JSON extracted from tables found in PDF file...")

    # # ToDo : Logic has to be moved in one of the python module
    # for count, page in enumerate(list_page_table):
    #   json_tables_string:str = extract_info.extract_json_from_table(list_images[page])
    #   # Do string cleanup before converting to JSON object
    #   # Remove backtick if it exists because Python does not like itf
    #   json_tables_string:str = generic_helper.remove_backticks(json_tables_string)
    #   list_json_doc:list[str] = generic_helper.get_list_json_doc(json_tables_string)

    #   for table_number, json_doc  in enumerate(list_json_doc):
    #     description:str = extract_info.description_from_json_bison(json_doc)
    #     source:str = "{}_page_{}_table_{}".format(st.session_state.filename_with_extension,page,table_number+1)
    #     json_doc = generic_helper.insert_string_in_json_doc(json_doc, description, source)
    #     # Save the JSON file
    #     with open("{}/json/{}_page{}_table{}.jsonl".format(st.session_state.temp_directory, st.session_state.filename_with_extension, page, table_number+1), "w") as fp:
    #       json.dump(json_doc, fp)
              
    with st.spinner(text = "Embedding extracted json..."):
      pgvector_embedding.embed_file_in_path (f"{st.session_state.temp_directory}/json", st.session_state.collection_name)
    progressbar.progress(1, text = f"JSON has been embedded...")




st.write("# Import statement for analysis")
st.write("---")

file_uploader = st.empty()

if 'uploaded_already' not in st.session_state:
         st.session_state.uploaded_already = False
         st.session_state.filename_with_extension = ""
         st.session_state.temp_directory = ""
         st.session_state.collection_name = ""
         st.session_state.buttonClicked = False


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

myButton = st.empty()

if st.session_state.uploaded_already == True:
    file_uploader.empty()
    st.write(f"File {st.session_state.filename_with_extension} uploaded successfully...")
    collection_name = st.text_input("Enter the name of the collection.")
    st.session_state.collection_name = collection_name
    st.session_state.buttonClicked = True
    myButton =st.button("Ready to process 📝...", on_click=process_file)

if st.session_state.buttonClicked == False:
    myButton.empty()



