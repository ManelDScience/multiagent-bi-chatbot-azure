from agents.src.sql_parser import extract_sql_from_markdown


def test_extract_sql_from_markdown_block():
    text = """## SQL propuesta
```sql
SELECT TOP 10 * FROM agg.TotalSalesPerYear;
```"""

    assert extract_sql_from_markdown(text) == "SELECT TOP 10 * FROM agg.TotalSalesPerYear;"


def test_extract_sql_without_markdown():
    text = "SELECT * FROM fact.fact_sales;"

    assert extract_sql_from_markdown(text) == "SELECT * FROM fact.fact_sales;"


def test_extract_sql_with_uppercase_sql_tag():
    text="""```SQL
SELECT Year, total_sales_peryear
FROM agg.TotalSalesPerYear;
```"""
    result = extract_sql_from_markdown(text)

    assert result == "SELECT Year, total_sales_peryear\nFROM agg.TotalSalesPerYear;"


def test_extract_sql_strips_whitespaces():
    text="""```sql
SELECT *
FROM agg.CustomerPerTotalSales;
```"""

    result = extract_sql_from_markdown(text)

    assert result == "SELECT *\nFROM agg.CustomerPerTotalSales;"