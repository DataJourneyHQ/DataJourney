from openai import OpenAI
from deepeval.tracing import observe
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

# Initialize OpenAI client
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

@observe()
def llm_app(query: str) -> str:
    return client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": query}
        ]
    ).choices[0].message.content
    return

if __name__ == "__main__":
    try:
        response = llm_app("What are the top 10 LLM evaluation tools?")
        print(response)
    except Exception as e:
        print(f"Error generating response: {e}")
