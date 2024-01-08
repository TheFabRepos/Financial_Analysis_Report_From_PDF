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


def replace_numbers_between_parentheses(json_string: str):
  """Replaces numbers between parentheses with the same number with a negative sign.

  Args:
    string: The string to search.

  Returns:
    The string with the numbers between parentheses replaced.
  """

  # Find all numbers between parentheses.
  numbers = re.findall(r"\((\d+)\)", json_string)

  # Replace each number with the same number with a negative sign.
  for number in numbers:
    json_string = json_string.replace("({})".format(number), f"-{number}")

  return json_string

def remove_backticks(json_string: str):
  """Removes all backticks from a string.

  Args:
    json_string: The string to remove backticks from.

  Returns:
    The string with all backticks removed.
  """
  
  json_string = json_string.replace("```", "")
  return json_string
