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