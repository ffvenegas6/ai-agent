import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():

    verbose = False

    if len(sys.argv) != 2:
        if len(sys.argv) == 3 and "--verbose" in sys.argv:
            verbose = True
            for arg in sys.argv:
                if arg not in ["main.py", "--verbose"]:
                    prompt = arg
                    break
        else:
            print("Usage: uv run main.py <prompt>")
            sys.exit(1)
    else:
        if sys.argv[1] != "--verbose":
            prompt = sys.argv[1]
        else:
            print("Usage: uv run main.py <prompt>")
            sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # prompt = ("Why is Boot.dev such a great place to " 
    #     "learn backend development? Use one paragraph maximum.")

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    # - Execute Python files with optional arguments
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt,
        ),
    )
    
    function_calls = response.function_calls
    # print(function_calls)
    if function_calls:
        for function_call_part in function_calls:
            function_call_result = call_function(function_call_part, verbose=True)
            if function_call_result.parts[0].function_response.response:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            else:
                raise Exception("Fatal Exception")
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        text = response.text
        print(text)

    if verbose:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
