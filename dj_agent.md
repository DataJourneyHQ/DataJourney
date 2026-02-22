# DataJourney Agent

A multi-agent system built on **Google ADK** that reasons over the DataJourney
intake catalog — analysing datasets, answering semantic queries and generating
dashboards — without hardcoding a single dataset or chart type.

---

## Architecture

```
orchestrator/agent.py
├── 📊 data_agent     → analyses any catalog dataset with LLM reasoning
├── 🔍 rag_agent      → embeds any dataset into ChromaDB, answers semantic queries
└── 💡 insight_agent  → chains analysis → chart decision → dashboard generation
```

```
tools/
├── catalog_tools.py   → list entries, load dataset, profile columns + stats
├── analysis_tools.py  → LLM analysis against any dataset, transformation suggestions
├── chroma_tools.py    → embed any column into ChromaDB, semantic query
└── dashboard_tools.py → LLM decides chart type + columns, writes Panel file
```

---

## What is genuinely new

| Old approach | New approach |
|---|---|
| Analysis hardcoded to `twilio_stock_price` | Any catalog entry, resolved at runtime |
| ChromaDB only held YouTube comments | Any dataset column can be embedded |
| Chart type chosen by the user | LLM reasons over the data profile and decides |
| Dashboard was a template fill-in | Dashboard is informed by the LLM analysis |
| Agents wrapped `subprocess` pixi calls | Agents reason over real data using tools |

---

## Agents

### 📊 `data_agent`
Answers analytical questions grounded in real data.

| Tool | What it does |
|---|---|
| `list_catalog_entries` | Lists all datasets in the intake catalog |
| `profile_dataset` | Returns shape, columns, dtypes and statistics |
| `analyse_dataset` | Runs LLM analysis against any catalog entry |
| `suggest_transformations` | LLM suggests meaningful Dagster assets / pandas ops |

### 🔍 `rag_agent`
Turns any catalog dataset into a searchable semantic index.

| Tool | What it does |
|---|---|
| `list_catalog_entries` | Lists all datasets in the intake catalog |
| `embed_dataset` | Embeds a column from any catalog entry into ChromaDB |
| `semantic_query` | Natural language search over the embedded collection |

### 💡 `insight_agent`
End-to-end: analysis → chart decision → ready-to-run dashboard file.

| Tool | What it does |
|---|---|
| `list_catalog_entries` | Lists all datasets in the intake catalog |
| `profile_dataset` | Profiles the dataset before analysis |
| `analyse_dataset` | Produces an LLM narrative of key trends |
| `decide_visualisation` | LLM picks the best chart type, x col and y col |
| `generate_dashboard` | Writes a Panel + HvPlot dashboard file |

---

## Setup

### 1. Install and activate

```bash
pixi install
pixi shell
```

### 2. API key

```bash
# .env at repo root
GOOGLE_API_KEY=your_key_here
```

Get a key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).
Enable billing — the free tier daily quota is exhausted quickly.

---

## Running

### Full orchestrator via web UI

```bash
pixi run DJ_agent_ui
# opens at http://localhost:8000
```

### Individual agent via web UI

```bash
cd analytics_framework/build_agents/agents
adk web
# select data_agent, rag_agent or insight_agent
```

---

## Routing reference

| What you say | Agent |
|---|---|
| `"what datasets are available?"` | 📊 `data_agent` |
| `"profile the coral bleaching dataset"` | 📊 `data_agent` |
| `"what are the trends in twilio stock price?"` | 📊 `data_agent` |
| `"suggest transformations for simple_trees"` | 📊 `data_agent` |
| `"search youtube comments for broken laptop"` | 🔍 `rag_agent` |
| `"find shipping complaints in the comments"` | 🔍 `rag_agent` |
| `"analyse twilio and build a dashboard"` | 💡 `insight_agent` |
| `"give me insights on simple_trees"` | 💡 `insight_agent` |

---

## Example flows

**Data analysis**
```
You:   what are the key trends in twilio_stock_price?
Agent: → data_agent
       → profile_dataset("twilio_stock_price")
       → analyse_dataset("twilio_stock_price", "what are the key trends?")
       ← LLM-grounded narrative based on real statistics
```

**Semantic search**
```
You:   find youtube comments about broken laptops
Agent: → rag_agent
       → embed_dataset("youtube_comments", "Comment")   [1000 docs indexed]
       → semantic_query("youtube_comments", "broken laptop")
       ← top 5 semantically matched comments
```

**End-to-end insight**
```
You:   analyse simple_trees and create a visualisation
Agent: → insight_agent
       → profile_dataset("simple_trees")
       → analyse_dataset("simple_trees", "what are the key trends?")
       → decide_visualisation("simple_trees")            [LLM picks scatter: Girth vs Volume]
       → generate_dashboard("simple_trees")
       ← analytics_framework/dashboard/simple_trees_dashboard.py
          run: python analytics_framework/dashboard/simple_trees_dashboard.py
```

---

## Pixi tasks

| Task | What it runs |
|---|---|
| `pixi run DJ_agent_ui` | `adk web` from `orchestrator/` — full multi-agent system |
| `pixi run DJ_agent_data` | `adk web` from `agents/` — pick a single agent |
