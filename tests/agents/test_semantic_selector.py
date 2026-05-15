from agents.src.semantic_selector import (
    extract_sections,
    score_section,
    select_semantic_context,
)


SEMANTIC_CONTEXT = """
## MÉTRICAS

# Metrics

## Total Sales

Business aliases:
- ventas
- ventas totales
- sales

SQL references:
- agg.TotalSalesPerYear.total_sales_peryear

## DIMENSIONES

# Dimensions

## Customer

Business aliases:
- cliente
- clientes
- customer

SQL references:
- agg.CustomerPerTotalSales.CustomerName

## Time

Business aliases:
- año
- mes
- year
- month

SQL references:
- agg.TotalSalesPerYear.Year
- agg.TotalSalesPerMonthYear.MonthName

## REGLAS DE NEGOCIO

# Business Rules

## Ranking queries

If the user asks for clientes con más ventas, return TOP 10.
"""


def test_extract_sections_returns_sections():
    sections = extract_sections(SEMANTIC_CONTEXT)

    assert len(sections) > 0
    assert any(section["title"] == "Total Sales" for section in sections)


def test_score_section_prioritizes_sales_metric():
    section = {
        "title": "Total Sales",
        "content": "ventas ventas totales sales total sales",
    }

    score = score_section("¿Cuáles son las ventas totales por año?", section)

    assert score > 0


def test_select_semantic_context_includes_relevant_sales_context():
    result = select_semantic_context(
        user_question="¿Cuáles son las ventas totales por año?",
        semantic_context=SEMANTIC_CONTEXT,
    )

    assert "Total Sales" in result
    assert "Trazabilidad de selección" in result