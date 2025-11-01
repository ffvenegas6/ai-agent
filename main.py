import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

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

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

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
