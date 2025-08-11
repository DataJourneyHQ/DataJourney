import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def read_markdown_prompt():
    markdown_file_path = 'Prompt.md'
    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as md_file:
            markdown_content = md_file.read()
        print("Markdown content read successfully:")
    except FileNotFoundError:
        print(f"Error: The file '{markdown_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return markdown_content

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b:novita",
    messages=[
        {
            "role": "system",
            "content": "you are an expert AI dev + software engineer who has deep understanding of tooling"
        },
        {
            "role": "user",
            "content": read_markdown_prompt()
        }
    ],
)

save_as_enhanced_prompt = completion.choices[0].message.content
with open("Enhanced_Prompt.md", "w", encoding='utf-8') as file:
    file.write(save_as_enhanced_prompt)
