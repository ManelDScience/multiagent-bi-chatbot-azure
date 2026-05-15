# Multi-Agent BI Chatbot on Azure

A personal portfolio project that explores how to build an **agentic Business Intelligence assistant** using Python agents, a JavaScript MCP Server, Azure SQL Database and Microsoft Foundry models.

The goal is to move beyond a simple SQL chatbot and build a multi-agent BI workflow capable of understanding business questions, selecting the right data context, generating SQL, executing queries safely, validating data quality and producing business-readable answers.

---

## Current Status

```text
Status: Functional MVP
```

The current version includes a working end-to-end flow:

```text
User question
  ↓
CLI entrypoint (`agents/main.py`)
  ↓
BI workflow orchestrator (`agents/workflows/bi_workflow.py`)
  ↓
Semantic Layer Loader
  ↓
Semantic Context Selector
  ↓
Planner Agent
  ↓
Schema Selector
  ↓
SQL Agent
  ↓
SQL Parser
  ↓
MCP Client
  ↓
MCP Server JS
  ↓
Azure SQL Database
  ↓
Data Quality Agent
  ↓
Analyst Agent
  ↓
Table Validator
  ↓
Critic Agent
  ↓
Critic Decision
  ↓
Final validated answer
```

Validated demo questions:

```text
¿Cuáles son las ventas totales por año?
¿Cuáles son los clientes con más ventas?
¿Cuáles fueron las ventas totales por mes?
```

---

## Project Objective

This project aims to demonstrate how AI agents can support BI workflows by transforming natural language business questions into validated data-driven answers.

The assistant can currently:

- Understand a business question.
- Plan the analysis.
- Load semantic business context.
- Select the most relevant SQL view/table.
- Generate SQL Server queries.
- Execute SQL through an MCP Server.
- Retrieve real data from Azure SQL.
- Validate basic data quality.
- Generate a business-readable answer.
- Validate tabular outputs deterministically.
- Review the answer with a Critic Agent.
- Normalize the Critic decision by code.
- Trigger one automatic revision if needed.

---

## Architecture

The project has been refactored into a modular Python workflow. The CLI entrypoint is intentionally small, while the full BI orchestration lives in a dedicated workflow module.

```text
┌──────────────────────────────┐
│        User Question         │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ agents/main.py               │
│ CLI entrypoint               │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ workflows/bi_workflow.py     │
│ Multi-agent orchestration    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Semantic Layer Loader        │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Semantic Context Selector    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Planner Agent                │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Schema Selector              │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ SQL Agent                    │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ SQL Parser                   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ MCP Client Python            │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ MCP Server JS                │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Azure SQL Database           │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Data Quality Agent           │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Analyst Agent                │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Table Validator              │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Critic Agent                 │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Normalized Critic Decision   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│ Final Answer / Revision Loop │
└──────────────────────────────┘
```

---

## Main Components

### BI Workflow Orchestrator

The orchestration logic has been extracted from `main.py` into:

```text
agents/workflows/bi_workflow.py
```

Current responsibility split:

```text
agents/main.py              → CLI entrypoint
agents/workflows/bi_workflow.py → full BI multi-agent workflow
```

The workflow orchestrator coordinates:

- Semantic context loading and selection.
- Planning.
- Schema selection.
- SQL generation and parsing.
- SQL execution through MCP.
- Data quality validation.
- Analyst response generation.
- Deterministic table validation.
- Critic review.
- Automatic revision when needed.

This refactor prepares the project for a future migration to Microsoft Agent Framework by separating the business workflow from the local command-line execution.

---

### Planner Agent

Interprets the user question and creates an analysis plan.

It identifies:

- Business objective.
- Required metrics.
- Required dimensions.
- Analysis steps.

---

### Semantic Layer Loader

Loads business context from:

```text
semantic-layer/metrics.md
semantic-layer/dimensions.md
semantic-layer/business_rules.md
```

This gives the agents additional context about metrics, dimensions and business rules.

---

### Semantic Context Selector

Selects the most relevant semantic context for each user question.

Instead of passing the full semantic layer to every agent, it scores semantic sections based on the user question and keeps only the most relevant context.

Current behavior:

- Reads the loaded semantic layer.
- Extracts semantic sections.
- Scores sections using keyword matching.
- Selects the most relevant metric, dimension and business rule context.
- Prints selection traceability.

This reduces prompt size and improves explainability.

Current limitation:

- It uses simple keyword scoring.
- It does not use embeddings or vector search yet.

---

### Schema Selector

Selects the most relevant SQL view/table using a scoring approach.

It considers:

- User question keywords.
- Available SQL views/tables.
- Preferred schemas such as `agg`, `fact`, and `dim`.
- Temporal granularity such as year vs month.
- Ranking intent such as top customers.

It also prints traceability information:

```text
Selected view
Selection score
Evaluated candidates
Available columns
```

---

### SQL Agent

Generates SQL Server queries using real schema metadata.

Rules:

- Use only `SELECT`.
- Use SQL Server syntax.
- Use real tables/views and columns.
- Avoid inventing schema.
- Use `TOP 10` by default for ranking questions.
- Avoid destructive SQL operations.

---

### MCP Server

The MCP Server is implemented in JavaScript and exposes safe SQL tools.

Current tools:

```text
query
list_views
```

The MCP Server connects to Azure SQL and acts as the controlled execution layer.

Safety controls:

- Only SELECT queries are allowed.
- Dangerous SQL keywords are blocked.
- SQL access is centralized through the MCP tool layer.

---

### Data Quality Agent

Reviews SQL results before analysis.

It checks for:

- Empty results.
- Null values.
- Negative values.
- Excessive number of rows.
- Possible duplicates.
- Insufficient data.

---

### Analyst Agent

Transforms SQL results into a clear business answer.

It focuses on:

- Answering the original question.
- Using only retrieved data.
- Avoiding unsupported causes.
- Formatting figures clearly.
- Producing business-friendly Spanish responses.

---

### Table Validator

Performs deterministic checks over structured SQL results before the Critic Agent reviews the final answer.

It helps validate that key values from the SQL result are present in the Analyst response, while normalizing numeric formats such as European and SQL decimal notation.

Current capabilities:

- Parses SQL results as JSON.
- Checks that key values returned by SQL are present in the Analyst response.
- Accepts equivalent numeric formats:
  - `381585.35`
  - `381,585.35`
  - `381.585,35`
- Supports translated month names between English SQL outputs and Spanish business responses:
  - `January` ↔ `Enero`
  - `February` ↔ `Febrero`
  - `March` ↔ `Marzo`
- Re-runs after the Analyst Agent produces a revised answer.
- Provides a deterministic signal that can override noisy Critic Agent feedback for structured table coverage.

This is an important design decision:

```text
Structured validation → deterministic Python code
Qualitative validation → Critic Agent
```

---

### Critic Agent

Reviews the Analyst Agent response.

It checks:

- Whether the answer responds to the original question.
- Whether figures match the SQL result.
- Whether unsupported causes were introduced.
- Whether the answer is clear for a business user.

A normalized critic decision is produced by code to avoid relying only on free-form LLM text.

---

## Tech Stack

- **Python** — agent workflow and orchestration.
- **JavaScript / Node.js** — MCP Server.
- **Azure SQL Database** — real data backend.
- **Azure Container Apps** — MCP deployment target.
- **Microsoft Foundry** — model endpoint.
- **Model Context Protocol** — tool interface.
- **Markdown semantic layer** — business definitions and context.

---

## Repository Structure

The Python agent workflow has been refactored into responsibility-based modules.

```text
.
├── agents/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── prompts/
│   │   ├── planner.md
│   │   ├── sql_agent.md
│   │   ├── analyst.md
│   │   ├── critic.md
│   │   └── data_quality.md
│   │
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── bi_workflow.py
│   │
│   ├── agent_modules/
│   │   ├── __init__.py
│   │   ├── planner_agent.py
│   │   ├── sql_agent.py
│   │   ├── analyst_agent.py
│   │   ├── critic_agent.py
│   │   └── data_quality_agent.py
│   │
│   ├── clients/
│   │   ├── __init__.py
│   │   └── mcp_client.py
│   │
│   ├── context_selectors/
│   │   ├── __init__.py
│   │   ├── schema_selector.py
│   │   ├── semantic_loader.py
│   │   └── semantic_selector.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── sql_parser.py
│   │
│   └── validators/
│       ├── __init__.py
│       ├── critic_parser.py
│       └── table_validator.py
│
├── mcp-server/
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile
│
├── semantic-layer/
│   ├── metrics.md
│   ├── dimensions.md
│   ├── business_rules.md
│   └── README.md
│
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── roadmap.md
│   └── mvp-demo.md
│
├── tests/
│   ├── conftest.py
│   ├── README.md
│   └── agents/
│       ├── test_critic_agent.py
│       ├── test_critic_parser.py
│       ├── test_schema_selector.py
│       ├── test_semantic_selector.py
│       ├── test_sql_parser.py
│       └── test_table_validator.py
│
├── README.md
└── LICENSE
```

Refactor completed:

```text
src/planner_agent.py        → agent_modules/planner_agent.py
src/sql_agent.py            → agent_modules/sql_agent.py
src/analyst_agent.py        → agent_modules/analyst_agent.py
src/critic_agent.py         → agent_modules/critic_agent.py
src/data_quality_agent.py   → agent_modules/data_quality_agent.py

src/mcp_client.py           → clients/mcp_client.py

src/schema_selector.py      → context_selectors/schema_selector.py
src/semantic_loader.py      → context_selectors/semantic_loader.py
src/semantic_selector.py    → context_selectors/semantic_selector.py

src/sql_parser.py           → utils/sql_parser.py

src/table_validator.py      → validators/table_validator.py
src/critic_parser.py        → validators/critic_parser.py

main.py orchestration       → workflows/bi_workflow.py
```

Important lesson from the refactor:

```text
Do not create a Python package called selectors.
```

Reason: `selectors` is also a Python standard library module used by `subprocess`. A local package with that name shadows the standard library and can break imports with errors such as:

```text
AttributeError: module 'selectors' has no attribute 'SelectSelector'
```

The final package name is therefore:

```text
context_selectors/
```

---

## Tests

The project includes basic automated tests for core utility modules.

Current coverage includes:

```text
- SQL parser.
- Critic parser.
- Table validator.
- Schema selector scoring.
- Semantic context selector.
- Critic agent behavior.
```

Run tests from the repository root:

```bash
python -m pytest tests
```

Current result:

```text
19 passed
```

---

## Demo

Detailed MVP demo documentation is available here:

```text
docs/mvp-demo.md
```

Validated scenarios:

1. Total sales by year.
2. Top customers by sales.
3. Total sales by month.

Example question:

```text
¿Cuáles son los clientes con más ventas?
```

Generated SQL:

```sql
SELECT TOP 10
    CustomerName,
    total_sales_perCustomer
FROM agg.CustomerPerTotalSales
ORDER BY total_sales_perCustomer DESC;
```

---

## Current Limitations

- The agent orchestration is still manual in Python, but it is now isolated in `workflows/bi_workflow.py`.
- `main.py` is only a CLI entrypoint.
- The Schema Selector uses rule-based scoring.
- Semantic context selection is implemented with simple keyword scoring, but not yet with embeddings or RAG.
- The Semantic Context Selector can still mix Markdown sections because it currently splits by headings.
- The Critic Agent can still be inconsistent on long tabular outputs, although the final decision is normalized by code and supported by deterministic validation.
- Tabular validation is partially deterministic and supports numeric normalization and month name translations.
- The current test suite covers core utilities, but end-to-end tests are not implemented yet.
- Monthly ordering should be improved by adding `MonthNumber` to the view.
- Microsoft Agent Framework migration is still pending.

---

## Roadmap

### Immediate next steps

- Update `docs/architecture.md` and `docs/roadmap.md` to reflect the modular structure.
- Add a visual architecture diagram for portfolio presentation.
- Add lightweight integration/smoke tests for the full BI workflow.

### Short term

- Improve Semantic Context Selector robustness.
- Add deterministic validation for more table patterns.
- Add more regression tests.
- Improve Schema Selector scoring.
- Add demo scripts.
- Add portfolio-ready screenshots and terminal outputs.

### Medium term

- Add semantic context retrieval with embeddings or RAG.
- Add logging and observability.
- Add a simple UI or API layer.
- Improve error handling and retries.
- Add richer metadata to the semantic layer.

### Long term

- Migrate orchestration to Microsoft Agent Framework.
- Deploy the Python agent workflow.
- Integrate more domains/datamarts.
- Add stronger governance and human-in-the-loop controls.
- Prepare a cloud-ready enterprise architecture.

---

## Why This Project Matters

This project demonstrates a practical implementation of an **Agentic BI Assistant**.

It combines:

- BI and analytics engineering.
- SQL generation.
- Semantic layer design.
- Azure cloud architecture.
- MCP tool integration.
- Multi-agent reasoning.
- Data quality validation.
- Answer review and correction loops.

The core value proposition:

```text
From natural language business questions
to validated BI answers
using real enterprise-style data and a multi-agent architecture.
```

---

## Current Milestone

```text
Functional Multi-Agent BI MVP with modular Python workflow, semantic context selection, deterministic validation utilities and 19 passing tests