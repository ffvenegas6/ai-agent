import os
from pathlib import Path
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        file_rel_path = os.path.join(working_directory, file_path)  
        work_abs_path = Path(working_directory).resolve()
        file_abs_path = (work_abs_path / file_path).resolve()
        print(f"File relative path: {file_rel_path}")
        print(f"Working directory absolute path: {work_abs_path}")
        print(f"File absolute path: {file_abs_path}")
    except Exception as e:
        return f'Error: \"{e}\"'

    if not file_abs_path.is_relative_to(work_abs_path):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(file_abs_path):
            # print(f"{file_abs_path} does not exists")
            os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)
        # elif not os.path.isfile(file_abs_path):
        #     return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f'Error: \"{e}\"'

    with open(file_abs_path, "w") as file:
        file.write(content)

    return f'Successfully wrote to "{file_abs_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes (or overwrites) content to file from specified path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to be written to the file.",
            ),
        },
        required=["file_path", "content"],
    )
)
