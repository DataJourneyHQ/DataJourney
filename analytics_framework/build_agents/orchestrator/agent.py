from google.adk.agents import Agent
from analytics_framework.build_agents.data_agent.agent import data_agent
from analytics_framework.build_agents.rag_agent.agent import rag_agent
from analytics_framework.build_agents.insight_agent.agent import insight_agent

root_agent = Agent(
    name="datajourney_orchestrator",
    model="gemini-2.5-flash",
    description="Root orchestrator for the DataJourney multi-agent system.",
    instruction="""
    You are the DataJourney Orchestrator.

    You coordinate three specialist agents. Route every request to the
    correct agent based on intent:

    📊 data_agent
        → analytical questions about any dataset
        → "what does the twilio dataset contain?"
        → "what are the trends in trees.csv?"
        → "suggest transformations for coral bleaching data"

    🔍 rag_agent
        → semantic search over dataset content
        → "find youtube comments about broken laptops"
        → "search the comments dataset for shipping complaints"

    💡 insight_agent
        → end-to-end: analysis + chart decision + dashboard generation
        → "give me insights and build a dashboard for twilio_stock_price"
        → "analyse simple_trees and create a visualisation"

    Rules:
    - Delegate to exactly one agent per request
    - If the intent spans analysis AND visualisation, use insight_agent
    - If unsure, ask one clarifying question before routing
    """,
    sub_agents=[data_agent, rag_agent, insight_agent],
)
