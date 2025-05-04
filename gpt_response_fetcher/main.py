import os
from openai import OpenAI
from dotenv import load_dotenv



load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt: str):
    """
    Sends the user's prompt to OpenAI and returns hte assistant's reply. 
    """

    response = client.responses.create(
        model="gpt-4.1-nano",
        input=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.output_text

def main():
    
    prompt = input("Ask a question: ")
    answer = ask_gpt(prompt)
    
    print(answer)

if __name__ == "__main__":
    main()