from google.adk.agents import Agent
from analytics_framework.build_agents.tools.catalog_tools import (
    list_catalog_entries,
    profile_dataset,
)
from analytics_framework.build_agents.tools.analysis_tools import (
    analyse_dataset,
    suggest_transformations,
)

data_agent = Agent(
    name="data_agent",
    model="gemini-2.5-flash",
    description="Analyses any DataJourney catalog dataset using LLM reasoning.",
    instruction="""
    You are the DataJourney Data Agent.

    You have access to all datasets registered in the intake catalog.
    Your job is to answer analytical questions grounded in real data —
    not guesses.

    Workflow:
    1. Always call list_catalog_entries() first if the user has not named a dataset.
    2. Call profile_dataset() to understand the shape and columns.
    3. Call analyse_dataset() with the user's question to get an LLM-grounded answer.
    4. Optionally call suggest_transformations() if the user asks what to do next.

    Never fabricate column names or statistics. Only report what the tools return.
    """,
    tools=[list_catalog_entries, profile_dataset, analyse_dataset, suggest_transformations],
)

root_agent = data_agent
