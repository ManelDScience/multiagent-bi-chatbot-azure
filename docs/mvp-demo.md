# MVP Demo — Multi-Agent BI Chatbot on Azure

## 1. Objective

This MVP demonstrates a **multi-agent Business Intelligence assistant** capable of answering business questions in natural language using real data from Azure SQL.

The system receives a business question, loads semantic business context, selects only the most relevant semantic definitions, plans the analysis, selects the most relevant data context, generates SQL, executes the query safely through an MCP Server, validates the result, produces a business-readable answer, validates table coverage deterministically and reviews the answer before delivery.

The current implementation has been refactored into a modular Python structure. `main.py` now acts as a lightweight CLI entry point, while `workflows/bi_workflow.py` contains the complete BI orchestration flow.

The current goal is not to build a final product yet, but to validate the core architecture of an agentic BI workflow.

---

## 2. Current Architecture

```text
CLI entry point
main.py
  ↓
BI Workflow Orchestrator
workflows/bi_workflow.py
  ↓
User question
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
Automatic revision if required
  ↓
Final validated answer
```

The project is now organized by responsibility:

```text
agent_modules/      → LLM-based agents
clients/            → external clients, such as MCP client
context_selectors/  → semantic and schema selection
utils/              → small utility modules
validators/         → deterministic validation and critic parsing
workflows/          → workflow orchestration
```

---

## 3. Main Components

### BI Workflow Orchestrator

Located in:

```text
agents/workflows/bi_workflow.py
```

The workflow orchestrator coordinates the complete BI agent pipeline.

Responsibilities:

- Load the semantic layer.
- Select the relevant semantic context.
- Run the Planner Agent.
- Select the relevant SQL schema context.
- Run the SQL Agent.
- Extract and execute SQL through MCP.
- Run Data Quality validation.
- Generate the Analyst response.
- Run deterministic Table Validator checks.
- Run Critic Agent validation.
- Trigger automatic revision when required.
- Normalize the final Critic decision.

This refactor keeps `main.py` small and prepares the project for a future migration to Microsoft Agent Framework.

Current `main.py` responsibility:

```text
1. Print CLI header.
2. Read the user business question.
3. Call run_bi_workflow(user_question).
```

---

### Planner Agent

Understands the business question and creates a short analysis plan.

Responsibilities:

- Identify the business objective.
- Identify required metrics.
- Identify required dimensions.
- Define the analysis steps.

Example output:

```text
Objective: calculate total sales by year.
Metrics needed: total sales.
Dimensions needed: year.
Plan:
1. Identify the sales metric.
2. Group results by year.
3. Calculate total sales per year.
```

---

### Semantic Layer Loader

Loads business context from the `semantic-layer` folder.

Current files loaded:

```text
semantic-layer/metrics.md
semantic-layer/dimensions.md
semantic-layer/business_rules.md
```

Purpose:

- Provide business definitions.
- Improve metric interpretation.
- Reduce ambiguity.
- Give agents additional context about metrics, dimensions and rules.

---

### Semantic Context Selector

Filters the semantic layer before passing it to the agents.

Instead of passing the full semantic layer to every agent, it scores semantic sections against the user question and keeps only the most relevant context.

Example:

```text
Question:
¿Cuáles son las ventas totales por año?

Selected semantic context:
- Total Sales
- Time
- Time granularity
```

Current behavior:

- Reads the loaded semantic layer.
- Extracts semantic sections.
- Scores sections using keyword matching.
- Selects the most relevant metric, dimension and business rule context.
- Prints selection traceability.

Benefits:

- Reduces prompt size.
- Improves traceability.
- Avoids sending unnecessary semantic context.
- Keeps the MVP simple without requiring embeddings yet.

Current limitation:

- It uses simple keyword scoring.
- It does not use embeddings, vector search or RAG yet.

---

### Schema Selector

Selects the most relevant SQL view/table for the user question.

It currently uses a simple scoring approach based on:

- Question keywords.
- Table/view names.
- Preferred schemas.
- Business heuristics.
- Temporal granularity, such as year vs month.
- Ranking intent, such as top customers.

Example:

```text
Question:
¿Cuáles son las ventas totales por año?

Selected view:
agg.TotalSalesPerYear

Candidate scores:
- agg.TotalSalesPerYear → score 50
- agg.TotalSalesPerMonthYear → score 30
- agg.CustomerPerTotalSales → score 20
- fact.fact_sales → score 18
```

---

### SQL Agent

Generates SQL Server queries using the selected schema context.

Responsibilities:

- Generate read-only SQL.
- Use real tables/views and columns.
- Avoid inventing schema.
- Use SQL Server syntax.
- Apply `TOP 10` for ranking queries by default.
- Avoid destructive SQL operations.

Example:

```sql
SELECT TOP 10
    CustomerName,
    total_sales_perCustomer
FROM agg.CustomerPerTotalSales
ORDER BY total_sales_perCustomer DESC;
```

---

### SQL Parser

Extracts SQL from the Markdown output generated by the SQL Agent.

Purpose:

- Receive the SQL Agent output.
- Extract the SQL block.
- Send only the executable SQL to the MCP Client.

---

### MCP Client

Python client that connects the agent workflow with the MCP Server.

Main responsibilities:

- Initialize MCP communication.
- Call MCP tools.
- Execute SQL through the MCP Server.
- Retrieve schema metadata.
- Retrieve query results.

Main functions:

```python
execute_sql(query)
list_views(search=None)
get_columns(schema, table)
```

---

### MCP Server

JavaScript MCP Server that exposes safe SQL tools.

Current tools:

```text
query
list_views
```

Responsibilities:

- Connect to Azure SQL.
- Execute read-only SELECT queries.
- Reject dangerous SQL keywords.
- Return query results as JSON.
- Serve as the controlled tool layer between agents and database.

Safety mechanisms:

- Only SELECT queries are allowed.
- Keywords such as DELETE, UPDATE, DROP, ALTER, TRUNCATE, MERGE and EXEC are blocked.
- SQL access is centralized in the MCP layer.

---

### Data Quality Agent

Reviews the SQL result before it is used by the Analyst Agent.

Checks:

- Empty result.
- Null values.
- Negative values in sales/amount metrics.
- Excessive number of rows.
- Possible duplicates.
- Insufficient data.

Example output:

```text
Estado de calidad: OK

Observaciones:
- No hay resultados vacíos.
- No se detectan valores negativos.
- Los datos parecen suficientes para responder a la pregunta.
```

---

### Analyst Agent

Converts SQL results into a business-readable answer.

Responsibilities:

- Answer the original question.
- Use only the data received.
- Avoid inventing causes.
- Format numbers clearly.
- Use Spanish business language.
- For rankings, present the Top N clearly.
- For period-based outputs, present the values by period.

---

### Table Validator

Performs deterministic validation over structured SQL results.

Responsibilities:

- Parse SQL results as JSON.
- Compare query result values with the Analyst Agent response.
- Normalize numeric formats.
- Accept equivalent numeric formats such as:
  - `381585.35`
  - `381,585.35`
  - `381.585,35`
- Detect possible missing values in tabular answers.
- Provide a deterministic validation signal to the Critic Agent.

The validator also supports equivalent month names between English SQL results and Spanish business responses.

Example:

```text
SQL result: January
Analyst response: Enero
```

This is accepted as equivalent.

This reduces the risk of the Critic Agent incorrectly flagging valid answers due to formatting differences, translated month names or long lists.

---

### Critic Agent

Reviews the Analyst Agent response before final delivery.

Checks:

- Whether the answer responds to the original question.
- Whether the figures are aligned with SQL results.
- Whether the answer invents causes.
- Whether the response is understandable for business users.
- Whether the response needs revision.

The Critic Agent receives the deterministic Table Validator output as additional context.

---

### Critic Decision Normalizer

Because LLM-generated validations can sometimes be inconsistent, the system normalizes the final Critic decision by code.

Example of possible LLM inconsistency:

```text
Validation: REQUIRES REVISION
Recommendation: APPROVED
```

The parser normalizes the decision to avoid unnecessary loops.

Main functions:

```python
critic_requires_revision(critic_output)
get_normalized_critic_decision(critic_output)
```

The system now treats inconclusive Critic outputs as requiring revision unless a deterministic validation signal supports approval.

---

## 4. Validated Demo Scenarios

## Demo 1 — Total Sales by Year

### User question

```text
¿Cuáles son las ventas totales por año?
```

### Selected semantic context

```text
Total Sales
Time
Time granularity
```

### Selected schema

```text
agg.TotalSalesPerYear
```

### Columns detected

```text
Year
total_sales_peryear
```

### SQL generated

```sql
SELECT
  Year,
  total_sales_peryear
FROM
  agg.TotalSalesPerYear
ORDER BY
  Year;
```

### Result returned by Azure SQL

```json
[
  {
    "Year": 2013,
    "total_sales_peryear": 45707188
  },
  {
    "Year": 2014,
    "total_sales_peryear": 49929487.2
  },
  {
    "Year": 2015,
    "total_sales_peryear": 53991490.45
  },
  {
    "Year": 2016,
    "total_sales_peryear": 22633175.55
  }
]
```

### Final business answer

```text
Las ventas totales por año son las siguientes:

- 2013: 45.707.188
- 2014: 49.929.487,20
- 2015: 53.991.490,45
- 2016: 22.633.175,55
```

### Validation

```text
Data Quality Agent → OK
Table Validator → OK
Critic Decision → APROBADA
```

---

## Demo 2 — Top Customers by Sales

### User question

```text
¿Cuáles son los clientes con más ventas?
```

### Selected semantic context

```text
Total Sales
Customer
Ranking queries
```

### Selected schema

```text
agg.CustomerPerTotalSales
```

### Columns detected

```text
CustomerName
total_sales_perCustomer
```

### SQL generated

```sql
SELECT TOP 10
    CustomerName,
    total_sales_perCustomer
FROM agg.CustomerPerTotalSales
ORDER BY total_sales_perCustomer DESC;
```

### Example result returned by Azure SQL

```json
[
  {
    "CustomerName": "Tailspin Toys (Inguadona, MN)",
    "total_sales_perCustomer": 381585.35
  },
  {
    "CustomerName": "Tailspin Toys (Minidoka, ID)",
    "total_sales_perCustomer": 371822.3
  },
  {
    "CustomerName": "Mauno Laurila",
    "total_sales_perCustomer": 369058.3
  },
  {
    "CustomerName": "Wingtip Toys (Sarversville, PA)",
    "total_sales_perCustomer": 365427
  },
  {
    "CustomerName": "Nasrin Omidzadeh",
    "total_sales_perCustomer": 361939.75
  }
]
```

### Final business answer

```text
Los diez clientes con más ventas son:

1. Tailspin Toys (Inguadona, MN): 381.585,35 €
2. Tailspin Toys (Minidoka, ID): 371.822,30 €
3. Mauno Laurila: 369.058,30 €
4. Wingtip Toys (Sarversville, PA): 365.427,00 €
5. Nasrin Omidzadeh: 361.939,75 €
...
```

### Validation

```text
Data Quality Agent → OK
Table Validator → OK
Critic Decision → APROBADA
```

---

## Demo 3 — Total Sales by Month

### User question

```text
¿Cuáles fueron las ventas totales por mes?
```

### Selected semantic context

```text
Total Sales
Time
Time granularity
Data interpretation
```

### Selected schema

```text
agg.TotalSalesPerMonthYear
```

### Columns detected

```text
Year
MonthName
total_sales_peryear
```

### SQL generated

```sql
SELECT
    Year,
    MonthName,
    total_sales_peryear AS TotalSales
FROM
    agg.TotalSalesPerMonthYear
ORDER BY
    Year,
    CASE
        WHEN MonthName = 'January' THEN 1
        WHEN MonthName = 'February' THEN 2
        WHEN MonthName = 'March' THEN 3
        WHEN MonthName = 'April' THEN 4
        WHEN MonthName = 'May' THEN 5
        WHEN MonthName = 'June' THEN 6
        WHEN MonthName = 'July' THEN 7
        WHEN MonthName = 'August' THEN 8
        WHEN MonthName = 'September' THEN 9
        WHEN MonthName = 'October' THEN 10
        WHEN MonthName = 'November' THEN 11
        WHEN MonthName = 'December' THEN 12
        ELSE 13
    END;
```

### Example result returned by Azure SQL

```json
[
  {
    "Year": 2013,
    "MonthName": "January",
    "TotalSales": 3770410.85
  },
  {
    "Year": 2013,
    "MonthName": "February",
    "TotalSales": 2776786.2
  },
  {
    "Year": 2013,
    "MonthName": "March",
    "TotalSales": 3870505.3
  }
]
```

### Final business answer

```text
A continuación se presentan las ventas totales por mes y año:

2013:
- Enero: 3.770.410,85 €
- Febrero: 2.776.786,20 €
- Marzo: 3.870.505,30 €
- Abril: 4.059.606,85 €
...

2016:
- Enero: 4.447.705,95 €
- Febrero: 4.005.616,85 €
- Marzo: 4.645.254,00 €
- Abril: 4.563.666,10 €
- Mayo: 4.970.932,65 €
```

### Validation

```text
Data Quality Agent → OK
Table Validator → OK
Critic Decision → APROBADA
```

### Important behavior validated

The SQL result returns month names in English:

```text
January
February
March
```

The Analyst response presents them in Spanish:

```text
Enero
Febrero
Marzo
```

The Table Validator accepts these as equivalent.

---

## 5. Automated Tests

The project includes basic automated tests with `pytest`.

Current tested modules:

```text
tests/agents/test_sql_parser.py
tests/agents/test_critic_parser.py
tests/agents/test_table_validator.py
tests/agents/test_schema_selector.py
tests/agents/test_semantic_selector.py
tests/agents/test_critic_agent.py
```

Current result:

```text
19 passed
```

The tests cover:

- SQL extraction from Markdown.
- Critic decision normalization.
- Handling inconclusive Critic outputs.
- Deterministic table validation.
- European number format handling.
- English/Spanish month equivalence.
- Schema selector scoring.
- Semantic context selection.
- Basic Critic Agent behavior.

---

## 6. Current Repository Structure

```text
.
├── agents/
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── agent_modules/
│   │   ├── __init__.py
│   │   ├── planner_agent.py
│   │   ├── sql_agent.py
│   │   ├── analyst_agent.py
│   │   ├── critic_agent.py
│   │   └── data_quality_agent.py
│   ├── clients/
│   │   ├── __init__.py
│   │   └── mcp_client.py
│   ├── context_selectors/
│   │   ├── __init__.py
│   │   ├── schema_selector.py
│   │   ├── semantic_loader.py
│   │   └── semantic_selector.py
│   ├── prompts/
│   │   ├── planner.md
│   │   ├── sql_agent.md
│   │   ├── analyst.md
│   │   ├── critic.md
│   │   └── data_quality.md
│   ├── utils/
│   │   ├── __init__.py
│   │   └── sql_parser.py
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── table_validator.py
│   │   └── critic_parser.py
│   └── workflows/
│       ├── __init__.py
│       └── bi_workflow.py
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
│   └── agents/
│       ├── test_sql_parser.py
│       ├── test_critic_parser.py
│       ├── test_table_validator.py
│       ├── test_schema_selector.py
│       ├── test_semantic_selector.py
│       └── test_critic_agent.py
│
├── README.md
└── LICENSE
```

Important naming decision:

```text
The selector package is named context_selectors/ instead of selectors/.
```

Reason:

```text
selectors is the name of a Python standard-library module. Using selectors/ as a local package shadows the standard module and can break dependencies such as subprocess, asyncio, pydantic and openai.
```

---

## 7. Technical Decisions

### Manual orchestration before Microsoft Agent Framework

The workflow is still manually orchestrated in Python, but it has now been extracted from `main.py` into:

```text
agents/workflows/bi_workflow.py
```

Current design:

```text
main.py → CLI entry point
bi_workflow.py → complete BI orchestration
```

Reason:

- Easier to understand.
- Easier to debug.
- Better for learning.
- Keeps the orchestration explicit.
- Avoids mixing framework migration with still-evolving BI logic.
- Makes the future migration to Microsoft Agent Framework cleaner.

Future plan:

```text
Manual orchestration in bi_workflow.py
  ↓
Microsoft Agent Framework workflow
  ↓
Cloud-ready orchestration
```

---

### Modular refactor before framework migration

The project has been reorganized by responsibility before migrating to Microsoft Agent Framework.

Current modules:

```text
agent_modules/      → LLM agent wrappers
clients/            → MCP and external clients
context_selectors/  → schema and semantic context selection
utils/              → low-level helpers
validators/         → deterministic validation and critic parsing
workflows/          → orchestration flow
```

Purpose:

- Reduce `main.py` complexity.
- Improve readability.
- Make imports and responsibilities clearer.
- Prepare the codebase for Microsoft Agent Framework.
- Reduce the risk of a large migration breaking current functionality.

---

### JavaScript MCP Server

The MCP Server remains in JavaScript because:

- It was already working locally.
- It was already deployed to Azure Container Apps.
- It was already connected to Microsoft Foundry.
- It provides a clean tool boundary between agents and Azure SQL.

---

### Python for agents

Python is used for the agent workflow because:

- It is better suited for AI orchestration.
- It integrates naturally with data and ML tooling.
- It will make future migration to Microsoft Agent Framework easier.
- It allows clear separation between reasoning and tool execution.

---

### Azure SQL as real backend

The system uses real Azure SQL data instead of mock data.

This makes the project more valuable as a portfolio project because it demonstrates:

- Real cloud data access.
- MCP tool execution.
- SQL generation.
- Metadata discovery.
- Query result interpretation.

---

### Semantic layer in Markdown

The semantic layer is stored as Markdown files.

Benefits:

- Easy to read.
- Easy to version in Git.
- Understandable for both humans and agents.
- Good first step before introducing RAG or vector search.

---

### Deterministic validation before LLM validation

The system now separates deterministic validation from qualitative LLM validation.

```text
Structured validation → Table Validator by code
Qualitative review → Critic Agent
```

This reduces the risk of LLM-based validation errors on long lists, translated values or numeric formatting.

---

## 8. Current Limitations

### Modular refactor is complete but imports remain local-execution oriented

The project is now modularized, but imports are still optimized for running from the `agents` folder during local development.

Current behavior:

```bash
cd agents
python main.py
```

Future improvement:

```text
Package the Python agent project more formally so it can be executed cleanly from the repository root and later deployed as a service.
```

---

### Schema Selector is still simple

The current selector uses rule-based scoring.

It works for the validated demo cases, but it is not yet robust enough for complex ambiguous questions.

Future improvement:

```text
Semantic schema retrieval
Embeddings
RAG
Better scoring
Domain routing
```

---

### Semantic Context Selector is basic

The semantic layer is now filtered by a basic Semantic Context Selector, but the selection still uses simple keyword scoring instead of embeddings or RAG.

Future improvement:

```text
Use embeddings or semantic search to retrieve only the most relevant definitions.
```

---

### Critic Agent can be inconsistent

The Critic Agent may sometimes produce contradictory output.

Example:

```text
Validation: REQUIRES REVISION
Recommendation: APPROVED
```

Current mitigation:

```text
Critic Decision is normalized by code.
Table Validator output is used as deterministic validation signal.
```

Future improvement:

```text
Use more deterministic validators for tabular outputs.
Use LLM only for qualitative review.
```

---

### Long tabular answers are hard for LLM validation

For long lists, the Critic Agent may incorrectly claim that rows are missing.

Current mitigation:

```text
Table Validator checks result coverage by code.
```

Future improvement:

```text
Validate row counts and values by code.
Use LLM only for qualitative review.
```

---

### Monthly ordering needs improvement

The `agg.TotalSalesPerMonthYear` view contains:

```text
Year
MonthName
total_sales_peryear
```

But it does not include `MonthNumber`.

This makes chronological ordering harder and forces the SQL Agent to generate a CASE statement.

Future improvement:

```text
Add MonthNumber to the view.
Document MonthName language in the semantic layer.
```

---

### Test suite is still small

The project now includes basic tests, but coverage is still limited.

Current result:

```text
19 passed
```

Future improvement:

```text
Add tests for:
- MCP client behavior
- SQL Agent prompt regression cases
- Data Quality Agent outputs
- Semantic selector edge cases
- End-to-end smoke tests
```

---

## 9. Roadmap

### Immediate next steps

```text
1. Update README.md with the latest modular architecture.
2. Add architecture diagram.
3. Improve Semantic Context Selector robustness.
4. Add lightweight integration tests for the full BI workflow.
5. Add more deterministic validators for tabular outputs.
6. Improve schema selector scoring.
```

### Short term

```text
1. Improve README and documentation.
2. Add architecture diagram.
3. Add demo scripts.
4. Add more tests for agent utilities.
5. Add deterministic validation for more table patterns.
6. Improve schema selector scoring.
```

### Medium term

```text
1. Add semantic context retrieval with embeddings or RAG.
2. Add logging and observability.
3. Add a simple UI or API layer.
4. Improve error handling and retries.
5. Add portfolio-ready screenshots and demo outputs.
```

### Long term

```text
1. Migrate orchestration to Microsoft Agent Framework.
2. Deploy the Python agent workflow.
3. Integrate more domains/datamarts.
4. Add stronger governance and human-in-the-loop controls.
5. Prepare a cloud-ready enterprise architecture.
```

### Future architecture

```text
User / UI
  ↓
Microsoft Agent Framework Orchestrator
  ↓
Semantic Context Retriever
  ↓
Planner Agent
  ↓
Schema Selector
  ↓
SQL Agent
  ↓
MCP Server
  ↓
Azure SQL
  ↓
Data Quality Agent
  ↓
Analyst Agent
  ↓
Table Validator
  ↓
Critic Agent
  ↓
Final Answer
```

---

## 10. Portfolio Value

This project demonstrates practical experience with:

- Multi-agent AI systems.
- Business Intelligence automation.
- Azure SQL.
- Microsoft Foundry.
- Model Context Protocol.
- Python agent workflows.
- JavaScript backend tooling.
- Semantic layers.
- Semantic context selection.
- SQL generation.
- Data quality validation.
- Deterministic table validation.
- Answer validation and revision loops.
- Automated testing.
- Cloud-ready architecture.

It is positioned as an **Agentic BI Assistant** rather than a simple SQL chatbot.

The core value proposition:

```text
From natural language business questions
to validated BI answers
using a multi-agent architecture connected to real enterprise-style data.
```

---

## 11. Current MVP Status

```text
Status: Functional MVP
```

Validated capabilities:

```text
Business question understanding
Semantic layer loading
Semantic context selection
Planning
Schema selection
SQL generation
SQL parsing
SQL execution through MCP
Azure SQL result retrieval
Data quality validation
Business answer generation
Deterministic table validation
Critic validation
Automatic revision
Normalized final decision
Basic automated testing
Modular project structure
Separated BI workflow orchestration
```

Validated questions:

```text
¿Cuáles son las ventas totales por año?
¿Cuáles son los clientes con más ventas?
¿Cuáles fueron las ventas totales por mes?
```

Current test status:

```text
19 passed
```

Current recommended next milestone:

```text
Update README.md with the latest modular architecture, then improve Semantic Context Selector robustness and add an architecture diagram for portfolio presentation.
```