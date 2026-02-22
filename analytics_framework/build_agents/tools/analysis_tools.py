import os
from google import genai
from analytics_framework.build_agents.tools.catalog_tools import load_dataset, profile_dataset


def _get_client() -> genai.Client:
    """Initialise the Google GenAI client from the environment."""
    return genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def analyse_dataset(entry_name: str, question: str) -> str:
    """
    Run a natural language analysis against any intake catalog dataset.

    Loads the dataset, builds a statistical profile, then asks the LLM
    the user's question grounded in that profile.

    Args:
        entry_name: Catalog entry name (e.g. 'twilio_stock_price').
        question: The analytical question to answer about the data.

    Returns:
        LLM-generated analysis as a string.
    """
    profile = profile_dataset(entry_name)
    if profile.startswith("❌"):
        return profile

    df, err = load_dataset(entry_name)
    if err:
        return err

    sample = df.head(5).to_string()

    prompt = f"""
You are a senior data analyst. You have been given a dataset profile and a 5-row sample.
Answer the user's question using only the data provided. Be specific and concise.

Dataset: {entry_name}
Profile:
{profile}

Sample rows:
{sample}

Question: {question}
"""
    client = _get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


def suggest_transformations(entry_name: str) -> str:
    """
    Ask the LLM to suggest meaningful data transformations for a dataset.

    Reads the dataset profile and returns a list of suggested Dagster
    assets or pandas operations that would add analytical value.

    Args:
        entry_name: Catalog entry name.

    Returns:
        LLM-generated transformation suggestions as a string.
    """
    profile = profile_dataset(entry_name)
    if profile.startswith("❌"):
        return profile

    prompt = f"""
You are a data engineering expert familiar with Dagster and pandas.
Given this dataset profile, suggest 3-5 meaningful data transformations or
derived metrics that would add analytical value.

For each suggestion output:
- A short name (Python function-safe)
- What it computes
- The pandas code to implement it

Dataset profile:
{profile}
"""
    client = _get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text
