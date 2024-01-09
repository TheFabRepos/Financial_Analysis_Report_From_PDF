import os
import uuid
import json
import re

def create_tmp_directory(filename_only):
  
  """Creates a temporary which will be used to do local work (e.g., converting PDF to images, getting JSON data, etc.).

  Args:
    filename_only: The name of the PDF file without the extension.

  Returns:
    The path to the temporary directory.
  """

  temp_directory = "{}/tmp_{}_{}".format(os.getcwd(),filename_only,str(uuid.uuid4()))
  os.makedirs(temp_directory, exist_ok=True)
  os.makedirs(os.path.join(temp_directory, "images"), exist_ok=True)
  os.makedirs(os.path.join(temp_directory, "json"), exist_ok=True)

  return temp_directory


def replace_numbers_between_parentheses(json_tables_string: str):
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

def remove_backticks(json_tables_string: str):
  """Removes all backticks from a string.

  Args:
    json_string: The string to remove backticks from.

  Returns:
    The string with all backticks removed.
  """
  #json_tables_string = (json_tables_string.encode('ascii', 'ignore')).decode("utf-8")
  json_tables_string = json_tables_string.replace("```", "")
  #json_tables_string = json_tables_string.replace("\\u00A0", "")
  #json_tables_string = json_tables_string.replace("\u2020", "")
  return json_tables_string

def convert_string_to_json(json_tables_string) :
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
        json_object = json.loads(json_doc)
        list_json_object.append(json_object)

    return list_json_object
