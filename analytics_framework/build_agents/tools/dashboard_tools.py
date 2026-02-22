import os
from pathlib import Path
from google import genai
from analytics_framework import INTAKE_LOC
from analytics_framework.build_agents.tools.catalog_tools import load_dataset, profile_dataset

_DASHBOARD_DIR = Path(__file__).resolve().parents[3] / "analytics_framework" / "dashboard"


def _get_client() -> genai.Client:
    """Initialise the Google GenAI client from the environment."""
    return genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


def decide_visualisation(entry_name: str) -> str:
    """
    Ask the LLM to reason over a dataset profile and decide the best visualisation.

    Reads the dataset profile and returns a structured recommendation:
    chart type, x column, y column and why.

    Args:
        entry_name: Catalog entry name to profile and reason about.

    Returns:
        LLM-generated visualisation recommendation as a string.
    """
    profile = profile_dataset(entry_name)
    if profile.startswith("❌"):
        return profile

    prompt = f"""
You are a data visualisation expert. Given this dataset profile, decide the single
most insightful chart to plot.

Respond in this exact format:
CHART_TYPE: <line|bar|scatter|hist|box|area>
X_COL: <column name or 'index'>
Y_COL: <column name>
REASON: <one sentence explaining why>

Dataset profile:
{profile}
"""
    client = _get_client()
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text


def generate_dashboard(entry_name: str) -> str:
    """
    Generate a Panel + HvPlot dashboard file for a catalog dataset.

    Uses the LLM to decide the best chart type and columns, then writes
    a ready-to-serve Panel dashboard Python file into analytics_framework/dashboard/.

    Args:
        entry_name: Catalog entry name to build a dashboard for.

    Returns:
        Path to the generated dashboard file, or an error string.
    """
    recommendation = decide_visualisation(entry_name)
    if recommendation.startswith("❌"):
        return recommendation

    # parse LLM recommendation
    config = {}
    for line in recommendation.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            config[key.strip()] = value.strip()

    chart_type = config.get("CHART_TYPE", "line")
    x_col = config.get("X_COL", "")
    y_col = config.get("Y_COL", "")
    reason = config.get("REASON", "")

    x_arg = f"x='{x_col}', " if x_col and x_col != "index" else ""
    y_arg = f"y='{y_col}', " if y_col else ""

    data_path = INTAKE_LOC / "catalog_entry.yml"
    safe_name = entry_name.lower().replace(" ", "_")
    out_path = _DASHBOARD_DIR / f"{safe_name}_dashboard.py"
    _DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    content = f"""import intake
import hvplot.pandas
import panel as pn
from analytics_framework import INTAKE_LOC

pn.extension()

catalog = intake.open_catalog(str(INTAKE_LOC / "catalog_entry.yml"))
df = catalog["{entry_name}"].read()

# Visualisation chosen by DataJourney Agent: {reason}
plot = df.hvplot.{chart_type}({x_arg}{y_arg}title="{entry_name}", responsive=True)

dashboard = pn.template.FastListTemplate(
    title="DataJourney | {entry_name}",
    main=[pn.panel(plot, sizing_mode="stretch_width")],
    accent="#e94560",
)

if __name__ == "__main__":
    dashboard.servable()
    pn.serve(dashboard, port=5006, show=True)
"""
    out_path.write_text(content, encoding="utf-8")
    return (
        f"✅ Dashboard written: analytics_framework/dashboard/{safe_name}_dashboard.py\n"
        f"   Chart : {chart_type} | x={x_col} | y={y_col}\n"
        f"   Reason: {reason}\n"
        f"   Run   : python analytics_framework/dashboard/{safe_name}_dashboard.py"
    )
