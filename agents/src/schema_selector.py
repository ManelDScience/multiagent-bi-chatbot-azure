from src.mcp_client import get_columns


def select_schema_context(user_question: str) -> str:
    question = user_question.lower()

    if "año" in question or "year" in question:
        selected_schema = "agg"
        selected_table = "TotalSalesPerYear"

    elif "mes" in question or "month" in question:
        selected_schema = "agg"
        selected_table = "TotalSalesPerMonthYear"

    elif "cliente" in question or "customer" in question:
        selected_schema = "agg"
        selected_table = "CustomerPerTotalSales"

    elif "grupo" in question or "buying" in question:
        selected_schema = "agg"
        selected_table = "BuyingGroupSalesPerMonth_without_others"

    else:
        selected_schema = "fact"
        selected_table = "fact_sales"

    columns_context = get_columns(selected_schema, selected_table)

    return f"""
TABLA/VISTA SELECCIONADA:
{selected_schema}.{selected_table}

COLUMNAS DISPONIBLES:
{columns_context}
"""