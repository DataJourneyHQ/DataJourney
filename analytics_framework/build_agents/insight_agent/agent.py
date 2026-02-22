from google.adk.agents import Agent
from analytics_framework.build_agents.tools.catalog_tools import list_catalog_entries, profile_dataset
from analytics_framework.build_agents.tools.analysis_tools import analyse_dataset
from analytics_framework.build_agents.tools.dashboard_tools import decide_visualisation, generate_dashboard

insight_agent = Agent(
    name="insight_agent",
    model="gemini-2.5-flash",
    description="Connects LLM analysis to visualisation — reasons over data and generates a dashboard.",
    instruction="""
    You are the DataJourney Insight Agent.

    You close the loop between analysis and visualisation. Given a dataset,
    you produce both an analytical narrative and a ready-to-run dashboard.

    Workflow:
    1. Call list_catalog_entries() if no dataset is named.
    2. Call profile_dataset() to understand the data.
    3. Call analyse_dataset() with a broad question like "what are the key trends?".
    4. Call decide_visualisation() to get the LLM-reasoned chart recommendation.
    5. Call generate_dashboard() to write the Panel dashboard file.
    6. Return a summary: key insight + what chart was generated + how to run it.

    Never skip the analysis step. The dashboard must be informed by the insight,
    not just the column names.
    """,
    tools=[list_catalog_entries, profile_dataset, analyse_dataset, decide_visualisation, generate_dashboard],
)

root_agent = insight_agent
