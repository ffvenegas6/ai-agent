import os
from pathlib import Path
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    try:
        file_rel_path = os.path.join(working_directory, file_path)
        work_abs_path = Path(working_directory).resolve()
        file_abs_path = (work_abs_path / file_path).resolve()
        # print(f"File relative path: {file_rel_path}")
        # print(f"Working directory absolute path: {work_abs_path}")
        # print(f"File absolute path: {file_abs_path}")
    except Exception as e:
        return f'Error: \"{e}\"'

    if not file_abs_path.is_relative_to(work_abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # if working_directory not in file_abs_path:
    #     return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(file_abs_path):
            return f'Error: File "{file_path}" not found'
    except Exception as e:
        return f'Error: \"{e}\"'

    try:
        # base, extension = os.path.split(file_path)
        extension = file_path[-3:]
        if extension != ".py":
            return f'Error: "{file_path}" is not a Python file.'
    except Exception as e:
        return f'Error: \"{e}\"'

    try:
        commands = ["uv", "run", file_rel_path]
        commands.extend(args)
        response = subprocess.run(
            commands,
            capture_output=True,
            timeout=30
        )
        if response.stdout is None and response.stderr is None:
            return "Not output produced."
        else:
            stdout = f"STDOUT: {response.stdout}\n"
            stderr = f"STDERR: {response.stderr}\n"
            return_code = f"Process exited with code {response.returncode}\n" if response.returncode != 0 else ""
            return stdout + stderr + return_code
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="execute python file from specified path, with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the python file to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="the list of strings with the optional arguments to be run with the python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    )
)
