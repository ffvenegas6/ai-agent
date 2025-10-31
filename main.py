import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():

    if len(sys.argv) != 2:
        print("Usage: uv run main.py <prompt>")
        sys.exit(1)

    prompt = sys.argv[1]

    # prompt = ("Why is Boot.dev such a great place to " 
    #     "learn backend development? Use one paragraph maximum.")

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt
    )

    text = response.text
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(text)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
