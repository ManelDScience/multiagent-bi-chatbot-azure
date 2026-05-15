# Dimensions

## Time

Business aliases:
- año
- mes
- trimestre
- fecha
- year
- month
- date

SQL references:
- agg.TotalSalesPerYear.Year
- agg.TotalSalesPerMonthYear.Year
- agg.TotalSalesPerMonthYear.MonthName

Notes:
- Use Year for yearly analysis.
- Use Year and MonthName for monthly analysis.

## Customer

Business aliases:
- cliente
- clientes
- customer
- customers

SQL references:
- agg.CustomerPerTotalSales.CustomerName
- dim.dim_customer

Notes:
- Use CustomerName when presenting customer rankings.