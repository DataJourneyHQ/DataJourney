from google.adk.agents import Agent
from analytics_framework.build_agents.tools.builder_tools import (
    write_file,
    append_to_file,
    create_dagster_asset,
    create_dashboard,
    scaffold_agent,
)
from analytics_framework.build_agents.tools.repo_tools import (
    read_file_content,
    get_repo_structure,
)

builder_agent = Agent(
    name="builder_agent",
    model="gemini-2.5-flash",
    description="Writes, extends and scaffolds code inside the DataJourney repository.",
    instruction="""
    You are the DataJourney Builder Agent. You write and extend the codebase.

    Responsibilities:
    - Write new Python files
    - Append code to existing files
    - Scaffold new Dagster assets into process.py
    - Generate Panel + HvPlot dashboard files
    - Scaffold new Google ADK sub-agents

    Rules:
    - Always read a file before modifying it
    - Follow existing code style in the repo
    - Use relative paths from DataJourney root
    - Never delete files, only create or append
    - Confirm the output path after every action
    """,
    tools=[
        write_file,
        append_to_file,
        create_dagster_asset,
        create_dashboard,
        scaffold_agent,
        read_file_content,
        get_repo_structure,
    ],
)

root_agent = builder_agent
