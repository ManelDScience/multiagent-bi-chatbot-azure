from agents.context_selectors.schema_selector import score_candidate


def test_score_prefers_yearly_sales_view_for_year_question():
    question = "¿Cuáles son las ventas totales por año?"

    yearly_score = score_candidate(question, "agg", "TotalSalesPerYear")
    monthly_score = score_candidate(question, "agg", "TotalSalesPerMonthYear")

    assert yearly_score > monthly_score


def test_score_prefers_monthly_sales_view_for_month_question():
    question = "¿Cuáles fueron las ventas totales por mes?"

    monthly_score = score_candidate(question, "agg", "TotalSalesPerMonthYear")
    buying_group_score = score_candidate(question, "agg", "BuyingGroupSalesPerMonth_without_others")

    assert monthly_score > buying_group_score


def test_score_prefers_customer_sales_view_for_customer_question():
    question = "¿Cuáles son los clientes con más ventas?"

    customer_score = score_candidate(question, "agg", "CustomerPerTotalSales")
    yearly_score = score_candidate(question, "agg", "TotalSalesPerYear")

    assert customer_score > yearly_score