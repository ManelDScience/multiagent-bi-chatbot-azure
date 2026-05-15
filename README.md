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
Semantic Layer Loader
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
Critic Agent
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
- Review the answer with a Critic Agent.
- Trigger one automatic revision if needed.

---

## Architecture

```text
┌────────────────────┐
│   User Question    │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Semantic Layer     │
│ Loader             │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Planner Agent      │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Schema Selector    │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ SQL Agent          │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ SQL Parser         │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ MCP Client Python  │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ MCP Server JS      │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Azure SQL Database │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Data Quality Agent │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Analyst Agent      │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Tabular Validator  │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Critic Agent       │
└─────────┬──────────┘
          ↓
┌────────────────────┐
│ Final Answer       │
└────────────────────┘
```

---

## Main Components

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

```text
.
├── agents/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── prompts/
│   └── src/
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
│   └── README.md
│
├── README.md
└── LICENSE
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

- The agent orchestration is still manual in Python.
- The Schema Selector uses rule-based scoring.
- The semantic layer is loaded fully, not selectively.
- The Critic Agent can be inconsistent on long tabular outputs.
- No automated test suite is implemented yet.
- Monthly ordering should be improved by adding `MonthNumber` to the view.

---

## Roadmap

### Short term

- Improve README and documentation.
- Add architecture diagram.
- Add demo scripts.
- Add basic tests.
- Add deterministic validation for tabular outputs.
- Improve schema selector scoring.

### Medium term

- Add semantic context retrieval instead of loading the full semantic layer.
- Add logging and observability.
- Add a simple UI or API layer.
- Improve error handling and retries.
- Add portfolio-ready screenshots and demo outputs.

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
Functional Multi-Agent BI MVP with Azure SQL and MCP
```