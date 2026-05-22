import click
import rich_click as rclick
from rich.console import Console
from rich.table import Table
import tomlkit

from analytics_framework import PACKAGE_LOC
from analytics_framework.workflows.explain import (
    WorkflowCatalogError,
    filter_workflows_by_category,
    get_workflows,
    list_to_text,
    list_workflow_names,
    validate_workflow_catalog,
    workflow_detail_panel,
    workflow_overview_panel,
    workflow_table,
)

rclick.rich_click.USE_RICH_MARKUP = True  # Enable rich formatting
console = Console()


def read_pixi_toml():
    candidate_paths = [
        PACKAGE_LOC.parent / "pixi.toml",
        PACKAGE_LOC.parent.parent / "pixi.toml",
    ]
    for path in candidate_paths:
        if path.exists():
            with path.open(encoding="utf-8") as f:
                return tomlkit.parse(f.read())
    return {"tasks": {}}


@click.group()
def cli():
    """CLI for exploring and explaining DataJourney workflows."""
    pass


@cli.command()
def list_workflows():
    """Show available workflows in pixi.toml."""
    table = Table(title="Available Workflows under DataJourney", show_lines=True, header_style="bold magenta")

    table.add_column("Task Name", style="bold cyan", justify="left")
    table.add_column("Source", style="bold green", justify="left")

    config = read_pixi_toml()
    workflows = config.get("tasks", {})

    if not workflows:
        table.add_row("[dim]No workflows found[/dim]", "[dim]N/A[/dim]")
    else:
        for name, details in workflows.items():
            path = details.get("cwd", "[dim]N/A[/dim]")
            table.add_row(f"[bold]{name}[/bold]", path)

    console.print(table)


@cli.command()
@click.argument("workflow_name", required=False)
@click.option("--list", "show_list", is_flag=True, help="Show a compact guide for all documented workflows.")
@click.option("--category", help="Show workflows for a specific category.")
@click.option("--validate", "show_validation", is_flag=True, help="Validate the workflow explanation catalog.")
def explain(workflow_name, show_list, category, show_validation):
    """Explain what a DataJourney workflow does and why it matters."""
    try:
        if show_validation:
            errors = validate_workflow_catalog()
            if errors:
                console.print("[bold red]Workflow catalog has validation errors:[/bold red]")
                console.print(list_to_text(errors))
                raise click.Abort()
            console.print("[bold green]Workflow catalog looks good.[/bold green]")
            return

        if category:
            workflows = filter_workflows_by_category(category)
            if not workflows:
                console.print(f"[yellow]No workflows found for category:[/yellow] {category}")
                return
            console.print(workflow_table(workflows))
            return

        if show_list:
            console.print(workflow_table(get_workflows()))
            return

        if workflow_name:
            console.print(workflow_detail_panel(workflow_name))
            return

        console.print(workflow_overview_panel())
    except WorkflowCatalogError as error:
        console.print(f"[bold red]{error}[/bold red]")
        suggestions = list_workflow_names()
        if suggestions:
            console.print("\nTry one of these workflows:")
            console.print(list_to_text(suggestions))
        raise click.Abort() from error


if __name__ == "__main__":
    cli()
