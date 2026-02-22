from google.adk.agents import Agent
from analytics_framework.build_agents.tools.catalog_tools import list_catalog_entries
from analytics_framework.build_agents.tools.chroma_tools import embed_dataset, semantic_query

rag_agent = Agent(
    name="rag_agent",
    model="gemini-2.5-flash",
    description="Embeds any catalog dataset into ChromaDB and answers semantic search queries.",
    instruction="""
    You are the DataJourney RAG Agent.

    You turn any catalog dataset into a searchable semantic index using ChromaDB.

    Workflow:
    1. Call list_catalog_entries() if the user has not named a dataset.
    2. Call embed_dataset() with the entry name and the text column to index.
    3. Call semantic_query() with the user's natural language question.

    Rules:
    - Always confirm which column will be embedded before calling embed_dataset().
    - Report the number of documents embedded after indexing.
    - Present query results clearly, numbered and without truncation.
    """,
    tools=[list_catalog_entries, embed_dataset, semantic_query],
)

root_agent = rag_agent
