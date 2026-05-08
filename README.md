# Multi-Agent BI Chatbot on Azure

A personal portfolio project that explores how to build a multi-agent Business Intelligence assistant using Python agents, a JavaScript MCP Server, Azure SQL Database and Microsoft Foundry models.

The goal is to create a BI assistant capable of answering business questions in natural language by planning the analysis, selecting the right schema context, generating SQL, executing queries safely and validating the final answer.

## Current Status

The project currently includes a functional MVP workflow:

```text
User question
  → Planner Agent
  → Schema Selector
  → SQL Agent
  → MCP Client
  → Azure SQL Database
  → Analyst Agent
  → Critic Agent
  → Final validated answer
```

## Main Components

- **Planner Agent**: understands the business question and creates an analysis plan.
- **Schema Selector**: selects the most relevant SQL view/table context.
- **SQL Agent**: generates SQL Server queries using the available schema.
- **MCP Client**: connects the Python agent layer with the MCP Server.
- **MCP Server**: JavaScript server exposing safe SQL tools through MCP.
- **Analyst Agent**: converts SQL results into a business-readable answer.
- **Critic Agent**: validates the answer and requests one revision if needed.

## Tech Stack

- Python
- JavaScript / Node.js
- Microsoft Foundry
- Azure SQL Database
- Azure Container Apps
- Model Context Protocol
- OpenAI-compatible API client

## Repository Structure

```text
.
├── agents/              # Python multi-agent workflow
├── mcp-server/          # JavaScript MCP Server
├── semantic-layer/      # Business definitions and semantic context
├── docs/                # Architecture, deployment and roadmap docs
├── tests/               # Future tests
└── README.md
```

## Current MVP Capabilities

- Receives a business question in natural language.
- Plans the analysis steps.
- Selects a relevant SQL view/table.
- Retrieves real schema metadata from Azure SQL.
- Generates SQL Server queries.
- Executes SQL through the MCP Server.
- Returns real query results.
- Generates a business explanation.
- Validates the answer with a Critic Agent.
- Performs one automatic revision if needed.

## Example Question

```text
¿Cuáles fueron las ventas totales por año?
```

Example flow:

```text
Planner → Schema Selector → SQL Agent → MCP/Azure SQL → Analyst → Critic
```

## Roadmap

- Improve the Schema Selector with dynamic scoring.
- Add Data Quality Agent.
- Add richer semantic layer integration.
- Add logging and observability.
- Migrate orchestration to Microsoft Agent Framework.
- Prepare deployment-ready architecture.
- Add portfolio-ready documentation and demo scenarios.

## Notes

This project is being developed incrementally.  
The current orchestration is manual in Python to make the internal workflow easier to understand and debug before migrating to a full agent framework.