import os
import pandas as pd
from openai import OpenAI
import intake
from analytics_framework import INTAKE_LOC
from pathlib import Path
from deepeval.tracing import observe
from dotenv import load_dotenv
load_dotenv()

# Data read via intake catalog
CATALOG_LOC = Path.joinpath(INTAKE_LOC, "catalog_entry.yml")
catalog = intake.open_catalog(CATALOG_LOC)

# Load the token and endpoint from environment variables
token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

# Initialize OpenAI client
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

@observe() #setting up deepeval tracing decorator
def analyze_data(intake_catalog_entry):
    # Load the data via intake
    try:
        df_input = catalog[intake_catalog_entry].read()
        print(f"Data loaded successfully {df_input.head()}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Prepare the data for analysis (simple description of the dataset)
    summary = df_input.describe().to_string()

    # Create the system and user messages for the model
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant skilled in analyzing data.",
        },
        {
            "role": "user",
            "content": f"Here is a summary of my data:\n{summary}\nProvide an analysis of this dataset, "
                       f"provide 03 recommendation regarding investment options",
        }
    ]

    return client.chat.completions.create(
        messages=messages,
        model=model_name,
        temperature=1.0,
        max_tokens=1000,
        top_p=1.0
    ).choices[0].message.content
    return

if __name__ == "__main__":
    intake_catalog_entry = "twilio_stock_price" # Example catalog entry name
    try:
        response = analyze_data(intake_catalog_entry)
        print("Analysis completed successfully.")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error during analysis: {e}")
