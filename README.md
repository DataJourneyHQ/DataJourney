<h1 align="center">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)\
[![DataJourney Stats](https://img.shields.io/badge/DataJourney-Visitors-orange)](https://datajourneyhq.github.io/DataJourney/)
[![Code of Conduct](https://img.shields.io/badge/Code_of_Conduct-Contributor%20Covenant-blue)](https://www.contributor-covenant.org/version/2/0/code_of_conduct/)\
[![CI](https://github.com/sayantikabanik/DataJourney/actions/workflows/CI.yml/badge.svg)](https://github.com/sayantikabanik/DataJourney/actions/workflows/CI.yml)
[![github-repo-stats](https://github.com/sayantikabanik/DataJourney/actions/workflows/github-repo-stats.yml/badge.svg)](https://github.com/sayantikabanik/DataJourney/actions/workflows/github-repo-stats.yml)
[![Deploy DataJourney Stats](https://github.com/sayantikabanik/DataJourney/actions/workflows/static.yml/badge.svg)](https://github.com/sayantikabanik/DataJourney/actions/workflows/static.yml)
[![Lint prose](https://github.com/sayantikabanik/DataJourney/actions/workflows/review.yml/badge.svg)](https://github.com/sayantikabanik/DataJourney/actions/workflows/review.yml)
[![Monitor GitHub API Rate Limit](https://github.com/sayantikabanik/DataJourney/actions/workflows/rate-limit-monitor.yml/badge.svg)](https://github.com/sayantikabanik/DataJourney/actions/workflows/rate-limit-monitor.yml)

</h1>

<p align="center">
  <img src="./assets/DataJourney_logo_svg/dj_darkmode.svg" alt="DJ rocks" style="width:500px; height:600px;">
</p>


### 🚌 DataJourney

#### 🪶Short version

Design- first Open Source Data Management Toolkit. Simplifies data workflows with modular, reproducible solutions

#### 🌲Long version

DataJourney demonstrates how organizations can effectively manage and utilize data by harnessing the power of open-source technologies. It's designed to help navigate the complex landscape of data tools, offering a structured approach to building **scalable**, and **reproducible** data workflows.

Built on open-source principles, the framework guides users through essential steps—from **identifying** goals and **selecting tools** to **testing** and **customising** workflows. With its flexible, modular design, DataJourney can be tailored to individual needs, making it an invaluable toolkit for data professionals.

### 🚦 Hold on, looking to contribute?

Head over to the [wiki](https://github.com/DataJourneyHQ/DataJourney/wiki/Contribute-to-DataJourney), let's make it happen together. We don't bite :)


### 🧱 Design Philosophy (LEGO)
Built with additive, subtractive capabilities glued with open source.
Each layer has a certain strength of communication inbuilt

- PO (Base): Static home(s) to keep it together `(GitHub)`
- P1 (Tooling): Tooling, strings `(Powered by open source)`
- P2 (Maintenance + Monitoring): Env, automations `(Pixi + GHA)`
- P3 (Abstraction): Layer(s), CLI/task manager for users to interact with `(Pixi)`


![DJ Design](assets/design/dj_vision.png)

### 🛠 Current workflows covered
{✨= Experimental,
✅ = Implemented}

| Status | Workflow Description                                                                                                                     |
|--------|------------------------------------------------------------------------------------------------------------------------------------------|
| ✅     | `Python Packaging framework` design principles                                                                                           |
| ✅     | `GitHub actions` configured                                                                                                              |
| ✅     | `Vale.sh` configured at PR level                                                                                                         |
| ✅     | `Pre-commit hooks` configured for code linting/formatting                                                                                |
| ✅     | `Hello world` LLM design example based on [LangChain](https://python.langchain.com/)                                                     |
| ✅     | Environment management via [pixi](https://prefix.dev/)                                                                                   |
| ✅     | Reading data from online sources using [intake](https://github.com/intake/intake)                                                        |
| ✅     | Sample pipeline built using [Dagster](https://github.com/dagster-io/dagster)                                                             |
| ✅     | Building Dashboard using [holoviews](https://holoviews.org/gallery/index.html) + [panel](https://panel.holoviz.org/reference/index.html) |
| ✅     | Exploratory data analysis (EDA) using [mito](https://www.trymito.io/)                                                                    |
| ✅     | Web UI build on [Flask](https://flask.palletsprojects.com/en/3.0.x/)                                                                     |
| ✅     | Web UI re-done and expanded with [FastHTML](https://docs.fastht.ml/)                                                                     |
| ✅     | Leverage AI models to analyse data [GitHub AI models Beta](https://docs.github.com/en/github-models/prototyping-with-ai-models)          |
| ✅     | Query engine for LLM application using [Chromadb](https://docs.trychroma.com/docs/overview/introduction)                                 |


### ☕️ Quickly getting started with DataJourney

- Fork the repository
- Generate & add `GITHUB_TOKEN`, instructions [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic)
  - Added requirement to run the LLM based workflows
- Switch directory `cd DataJourney`
- Download pixi : [prefix.dev](https://prefix.dev/)
- Activate env: `pixi shell`
- Install DJ framework locally `pixi run DJ_package`
- List all the tasks: `pixi run DJ_list`
- Execute a specific task from the list: `pixi run <TASK_NAME>`
- Execute a specific task with additional logs: `pixi run -v <TASK_NAME>`

### 🏃🏽‍♀️ Active `tasks` under DJ

| **Task Name**                 | **Description**                                                                                  |
|-------------------------------|--------------------------------------------------------------------------------------------------|
| `GIT_TOKEN_CHECK`             | Verifies the availability and validity of the Git authentication token.                          |
| `DJ_package`                  | Prepares and builds the Python package for the DataJourney project.                              |
| `DJ_pre_commit`               | Runs pre-commit hooks to ensure code quality and adherence to standards.                         |
| `DJ_dagster`                  | Sets up and runs a Dagster workflow for orchestration in the project.                            |
| `DJ_fasthtml_app`             | Executes a FastAPI-based HTML application.                                                       |
| `DJ_flask_app`                | Configures and runs a Flask-based application for data services.                                 |
| `DJ_mito_app`                 | Launches the Mito application for interactive data analysis in notebooks.                        |
| `DJ_panel_app`                | Executes a Panel dashboard app for data visualization and analytics.                             |
| `DJ_llm_analysis`             | Performs analysis using large language models (LLMs) on project data.                            |
| `DJ_hello_world_langchain`    | Sets up a basic LangChain app as a "Hello World" example for LLMs.                               |
| `DJ_spanish_eng_translation`  | Performs Spanish to English translation with Deepseek-R1 (`NOTE`: Takes about ~30 secs to execute this task) |
| `DJ_sync_dataset_trees`       | Downloads and synchronizes the `trees.csv` dataset into the project structure.                   |
| `DJ_chromadb_gen_embedding`   | Query engine for LLM applications                                                                |


### 🔌 About pre-commit-hooks and activating
Just like the name suggests, pre-commit-hooks are designed to format the code based on PEP standards before committing. [More details](https://pre-commit.com/)

```shell
pixi run DJ_pre_commit
```

### 🦭 Executing LLM script: Generate stock price recommendations

```shell
pixi run DJ_llm_analysis
```

### 🪼 Execute pre-configured Dagster pipeline

```shell
pixi run DJ_dagster
```
![Dagit UI output](assets/pipeline/dagster_ui.png)

### 🐙 Panel app
```shell
pixi run DJ_panel_app
```

*NOTE:*
The dashboard generated is exported into HTML format and saved as [stock_price_twilio_dashboard](analytics_framework%2Fdashboard%2Fstock_price_twilio_dashboard.html)

![Panel app output](assets/dashboard/panel_app_stock.png)

### 🐵 Mito

To explore further visit [trymito.io](https://docs.trymito.io/)
```shell
pixi run DJ_mito_app
```

[//]: # (![mito output]&#40;assets/pipeline/mito_graph.png "Graph generated via mitosheet"&#41; ![mito output operation]&#40;assets/pipeline/mito_operations.png "Operations performed via mitosheet"&#41;)

<div style="display: flex; justify-content: space-between;">
    <img src="assets/pipeline/mito_graph.png" alt="mito_output" width="400"/>
    <img src="assets/pipeline/mito_operations.png" alt="mito_output" width="400"/>
</div>

### 🦋 Display all data sources present via web UI

```shell
# Run FastHTML app
pixi run DJ_fasthtml_app
```
![data_sources_fasthtml.png](assets/pipeline/data_sources_fasthtml.png)
