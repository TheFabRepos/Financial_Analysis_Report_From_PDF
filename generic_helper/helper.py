import os
import uuid


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

import json

def extract_json_objects(string):
  """Extracts all the JSON objects from a string and returns one object per JSON document.

  Args:
    string: The string to extract the JSON objects from.

  Returns:
    A list of JSON objects.
  """

  json_objects = []
  for match in re.finditer(r'(\{.*?\})', string):
    json_objects.append(json.loads(match.group(1)))

  return json_objects
