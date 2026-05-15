# Business Rules

## Ranking queries

If the user asks for:
- clientes con más ventas
- top clientes
- mayores ventas
- best customers

Default behavior:
- Return TOP 10 unless the user specifies another number.
- Sort sales metrics in descending order.

## Time granularity

If the user asks for sales by year:
- Prefer agg.TotalSalesPerYear.

If the user asks for sales by month:
- Prefer agg.TotalSalesPerMonthYear.

## Data interpretation

Do not infer causes from sales increases or decreases unless supporting data is available.

If a period has fewer months than other years:
- Mention only that the available data covers those months.
- Do not assume the year is incomplete unless explicitly indicated.