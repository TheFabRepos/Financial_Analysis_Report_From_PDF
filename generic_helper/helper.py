import os
import uuid
import json
import re
import json
import logging

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True


def create_tmp_directory(filename_only) -> str:
  
  """Creates a temporary which will be used to do local work (e.g., converting PDF to images, getting JSON data, etc.).

  Args:
    filename_only: The name of the PDF file without the extension.

  Returns:
    The path to the temporary directory.
  """

  temp_directory = "{}/tmp_{}_{}".format(os.getcwd(),filename_only,str(uuid.uuid4()))
  os.makedirs(temp_directory, exist_ok=True)
  #os.makedirs(os.path.join(temp_directory, "images"), exist_ok=True)
  os.makedirs(os.path.join(temp_directory, "json"), exist_ok=True)

  return temp_directory


def replace_numbers_between_parentheses(json_tables_string: str) -> str:
  """Replaces numbers between parentheses with the same number with a negative sign.

  Args:
    string: The string to search.

  Returns:
    The string with the numbers between parentheses replaced.
  """

  # Find all numbers between parentheses.
  numbers = re.findall(r"\((\d+)\)", json_tables_string)

  # Replace each number with the same number with a negative sign.
  for number in numbers:
    json_tables_string = json_tables_string.replace("({})".format(number), f"-{number}")

  return json_tables_string

def remove_backticks(json_tables_string: str) -> str:
  """Removes all backticks from a string.

  Args:
    json_string: The string to remove backticks from.

  Returns:
    The string with all backticks removed.
  """
  json_tables_string = json_tables_string.replace("```", "")
  return json_tables_string

def get_list_json_doc(json_tables_string:str) -> list[str]:
    
    list_json_docs = json_tables_string.split("json")

    # Here we use a heuristic to avoit meaningless JSON object
    list_json_docs_no_empty = [json_doc for json_doc in list_json_docs if len(json_doc) > 10]
    return list_json_docs_no_empty

def insert_string_in_json_doc(json_doc:str, description:str, source:str) -> str:
  """Inserts a string into a JSON document. The string is inserted just after the first "{" character.

  Args: 
    json_doc: The JSON document to insert the string into. 
    description: The description of the JSON document. 
    source: The source of the JSON document.

  Returns: 
    The JSON document with the string inserted. 
  """

  info_to_insert_in_json_doc:str = f'"description": "{description}" \n "source": "{source}"'
  # We want to insert a few elements just after the first "{"
  substr:str = "{"

  idx:int = json_doc.index(substr)
  json_doc = json_doc[:(idx+1)] + info_to_insert_in_json_doc + json_doc[(idx+1):]
  return json_doc
 


def convert_string_to_json(page, json_tables_string) -> str:
    """Converts a string with multiple JSON docuemnt to a JSON object.

    Args:
        string: The string to convert to JSON objects.

    Returns:
        A list of JSON object.
    """
    list_json_object = []
    list_json_docs = json_tables_string.split("json")

    # Here we use a heuristic to avoit meaningless JSON object
    list_json_docs_no_empty = [json_doc for json_doc in list_json_docs if len(json_doc) > 10]


    for json_doc in list_json_docs_no_empty:
        if is_json(json_doc)==True:
          json_object = json.loads(json_doc)
          list_json_object.append(json_object)
        else:
           print("************ FAILED ************")
           print (f"page #{page}")
           print(json_doc)

    return list_json_object

def extract_filename (full_name: str) -> str:
    """Extracts the filename from a full path.

    Args:
        full_name: The full path to the file with extension and folder name.


    Returns:
        The filename (with extension) and the filename (without extension) as string
    """

    #Extract the file name (with extension but without folder name)
    filename_with_extension = (full_name.split("/")[-1])
    #Extract the file name (without extension or folder name)
    filename_only = (full_name.split("/")[-1]).split(".")[0]
    return filename_with_extension, filename_only