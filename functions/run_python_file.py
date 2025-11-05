import os
import subprocess

# import sys

# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def run_python_file(working_directory, file_path, args=[]):
    try:
        file_rel_path = os.path.join(working_directory, file_path)  
        print(file_rel_path)
        file_abs_path = os.path.abspath(file_rel_path)
    except Exception as e:
        return f'Error: \"{e}\"'

    if working_directory not in file_abs_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

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

