import os
import sys
from google.genai import types

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        file_rel_path = os.path.join(working_directory, file_path)  
        file_abs_path = os.path.abspath(file_rel_path)
    except Exception as e:
        return f'Error: \"{e}\"'

    if working_directory not in file_abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.isfile(file_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f'Error: \"{e}\"'

    with open(file_abs_path, "r") as file:
        file_content_string = file.read(MAX_CHARS)
    
    if len(file_content_string) == MAX_CHARS:
        file_content_string += f'[...File \"{file_path}\" truncated at {MAX_CHARS} characters]'
    
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read content from the specified path, as a truncated string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to read the content from, relative to the working directory.",
            ),
        },
    )
)
