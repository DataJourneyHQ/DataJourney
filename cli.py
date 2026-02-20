import click
import rich_click as rclick
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import tomlkit
import os
from pathlib import Path
from dotenv import load_dotenv, set_key

rclick.rich_click.USE_RICH_MARKUP = True  # Enable rich formatting
console = Console()
ENV_FILE = Path(".env")

def read_pixi_toml():
    with open("pixi.toml", "r") as f:
        return tomlkit.parse(f.read())

config = read_pixi_toml()

@click.group()
def cli():
    """🚀 CLI for Managing DataJourney Workflows"""
    pass

@cli.command()
def list_workflows():
    """📜 Show available workflows in pixi.toml"""
    table = Table(title="🚀 Available Workflows under DataJourney", show_lines=True, header_style="bold magenta")

    table.add_column("🔹 Task Name", style="bold cyan", justify="left")
    table.add_column("📁 Source", style="bold green", justify="left")

    workflows = config.get("tasks", {})

    if not workflows:
        table.add_row("[dim]No workflows found[/dim]", "[dim]N/A[/dim]")
    else:
        for name, details in workflows.items():
            path = details.get("cwd", "[dim]N/A[/dim]")
            table.add_row(f"[bold]{name}[/bold]", path)

    console.print(table)

# ─────────────────────────────────────────────
# Agent command group
# ─────────────────────────────────────────────

@cli.group()
def agent():
    """🤖 DataJourney Multi-Agent System (Google ADK)"""
    pass


def _get_or_prompt_api_key() -> str:
    """Load API key from .env or prompt the user once."""
    load_dotenv(ENV_FILE)
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key:
        console.print(Panel(
            "[bold yellow]🔑 No GOOGLE_API_KEY found.[/bold yellow]\n"
            "Your key will be saved to [cyan].env[/cyan] for future runs.",
            title="DataJourney Agent Setup",
            border_style="yellow",
        ))
        key = Prompt.ask("[bold cyan]Enter your Google API key[/bold cyan]", password=True)
        set_key(ENV_FILE, "GOOGLE_API_KEY", key)
        console.print("[green]✅ Key saved to .env[/green]\n")
    os.environ["GOOGLE_API_KEY"] = key
    return key


@agent.command()
def run():
    """
    🧠 Start the DataJourney multi-agent chat loop.

    The orchestrator routes your requests across:
      🔍 Repo Agent     → understand the codebase
      🏗️  Builder Agent  → write & extend code
      🔧 Pipeline Agent → run Dagster / pixi tasks
      📊 Dashboard Agent → create Panel dashboards
    """
    _get_or_prompt_api_key()

    from analytics_framework.build_agents.orchestrator.agent import build_root_agent
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import Content, Part
    import asyncio

    session_service = InMemorySessionService()
    APP_NAME = "datajourney"
    USER_ID  = "user"
    SESSION_ID = "session_1"

    asyncio.run(session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    ))

    root_agent = build_root_agent()

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    console.print(Panel(
        "[bold green]DataJourney Multi-Agent System[/bold green]\n\n"
        "  [cyan]🔍 repo_agent[/cyan]      → ask about any file or structure\n"
        "  [cyan]🏗️  builder_agent[/cyan]  → create files, assets, dashboards\n"
        "  [cyan]🔧 pipeline_agent[/cyan]  → run pixi tasks & Dagster pipelines\n"
        "  [cyan]📊 dashboard_agent[/cyan] → generate Panel + HvPlot dashboards\n\n"
        "Type [bold yellow]exit[/bold yellow] or [bold yellow]quit[/bold yellow] to stop.",
        title="🤖 DataJourney Agent",
        border_style="green",
    ))

    async def chat_loop():
        while True:
            try:
                user_input = Prompt.ask("\n[bold magenta]You[/bold magenta]")
            except (EOFError, KeyboardInterrupt):
                console.print("\n[yellow]👋 Exiting DataJourney Agent.[/yellow]")
                break

            if user_input.strip().lower() in {"exit", "quit", "q"}:
                console.print("[yellow]👋 Exiting DataJourney Agent.[/yellow]")
                break

            message = Content(role="user", parts=[Part(text=user_input)])

            console.print("\n[bold cyan]🤖 Agent[/bold cyan]")
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=SESSION_ID,
                new_message=message,
            ):
                if event.is_final_response():
                    reply = event.content.parts[0].text if event.content.parts else ""
                    console.print(Panel(reply, border_style="cyan", padding=(1, 2)))

    asyncio.run(chat_loop())


@agent.command()
def status():
    """📋 Show the multi-agent system structure and sub-agents."""
    table = Table(
        title="🤖 DataJourney Multi-Agent System",
        show_lines=True,
        header_style="bold magenta",
    )
    table.add_column("Agent", style="bold cyan")
    table.add_column("Role", style="green")
    table.add_column("Tools", style="yellow")

    rows = [
        ("🧭 orchestrator", "Routes all requests to sub-agents", "sub_agents delegation"),
        ("🔍 repo_agent",   "Reads & searches the full codebase", "get_repo_structure, read_file_content, search_repo, list_pixi_tasks"),
        ("🏗️  builder_agent","Writes files, assets & agents",     "write_file, append_to_file, create_dagster_asset, create_dashboard, scaffold_agent"),
        ("🔧 pipeline_agent","Runs pixi tasks & Dagster assets",  "run_pixi_task, run_pipeline_asset, list_pipeline_assets"),
        ("📊 dashboard_agent","Generates Panel + HvPlot dashboards","create_dashboard, run_pixi_task, search_repo"),
    ]
    for row in rows:
        table.add_row(*row)

    console.print(table)


if __name__ == "__main__":
    cli()
