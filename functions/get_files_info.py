import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        dir_rel_path = os.path.join(working_directory, directory)  
        dir_abs_path = os.path.abspath(dir_rel_path)
    except Exception as e:
        return f'Error: \"{e}\"'

    # print(f"Working directory: {working_directory}")
    # print(f"Directory: {directory}")
    # print(f"Directory relative path: {dir_rel_path}")
    # print(f"Directory absolute path: {dir_abs_path}")

    if working_directory not in dir_abs_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    try:
        if not os.path.isdir(dir_abs_path):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f'Error: \"{e}\"'

    try:
        contents = os.listdir(dir_abs_path) 
    except Exception as e:
        return f'Error: \"{e}\"'

    # print(contents)
    if directory != ".":
        result = f'Result for \"{directory}\" directory:\n'
    else:
        result = f'Result for current directory:\n'
    for content in contents:
        try:
            # print(content) 
            abs_path = os.path.join(dir_abs_path, content)
            # print(abs_path)
            is_dir = os.path.isdir(abs_path)
            # print(is_dir)
            # if not is_dir:
            size = os.path.getsize(abs_path)
            # else:
            #     size = "dir size"
            result += f'- {content}: file_size={size} bytes, is_dir={is_dir}\n'
        except Exception as e:
            return f'Error: \"{e}\"'
    return result


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    )
)
