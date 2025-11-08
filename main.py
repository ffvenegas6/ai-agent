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
    i = 0
    while i < 20:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt,
                ),
            )
        except Exception as e:
            print(f"Error while generating content with gemini api: {e}")
            sys.exit(1)

        function_calls = response.function_calls
        # print("Function calls:")
        # print(function_calls)
        
        # text = response.text
        # print("Text:")
        # print(text)

        candidates = response.candidates
        # print("Candidates:")
        # print(candidates)

        if candidates:
            for candidate in candidates:
                # print("Candidate content:")
                # print(candidate.content)
                # print(type(candidate.content))
                messages.append(candidate.content)

        if function_calls:
            for function_call_part in function_calls:
                try:
                    function_call_result = call_function(function_call_part, verbose=True)
                    function_response = function_call_result.parts[0].function_response.response
                    if function_response:
                        # print("Function response:")
                        # print(f"-> {function_response}")
                        messages.append(
                            types.Content(role="user", parts=[types.Part(text=function_response["result"])]),
                        )
                    else:
                        raise Exception("Fatal Exception")
                except Exception as e:
                    print(f"Error while calling function: {e}")
                    sys.exit(1)
        elif response.text:
            print("Final response:")
            print(response.text)
            break

        # if verbose:
        #     prompt_tokens = response.usage_metadata.prompt_token_count
        #     response_tokens = response.usage_metadata.candidates_token_count
        #     print(f"User prompt: {prompt}")
        #     print(f"Prompt tokens: {prompt_tokens}")
        #     print(f"Response tokens: {response_tokens}")

        i += 1

    # print("We are out of the loop")
if __name__ == "__main__":
    main()
