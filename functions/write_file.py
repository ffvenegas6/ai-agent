import os


def write_file(working_directory, file_path, content):
    try:
        file_rel_path = os.path.join(working_directory, file_path)  
        file_abs_path = os.path.abspath(file_rel_path)
    except Exception as e:
        return f'Error: \"{e}\"'

    if working_directory not in file_abs_path:
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
