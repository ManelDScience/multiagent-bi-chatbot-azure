from agents.src.table_validator import validate_table_coverage


def test_table_validator_accepts_european_number_format():
    query_result = """
[
  {
    "CustomerName": "Tailspin Toys",
    "total_sales_perCustomer": 381585.35
  }
]
"""

    analyst_output = "Tailspin Toys: 381.585,35 €"

    result = validate_table_coverage(query_result, analyst_output)

    assert "OK" in result


def test_table_validator_detects_missing_value():
    query_result = """
[
  {
    "CustomerName": "Tailspin Toys",
    "total_sales_perCustomer": 381585.35
  }
]
"""

    analyst_output = "Otro cliente: 100 €"

    result = validate_table_coverage(query_result, analyst_output)

    assert "REVISAR" in result


def test_table_validator_handles_empty_result():
    query_result = "[]"
    analyst_output = "No hay datos disponibles."

    result = validate_table_coverage(query_result, analyst_output)

    assert "REVISAR" in result

    def test_table_validator_accepts_translated_month_names():
      query_result = """
  [
    {
      "Year": 2013,
      "MonthName": "January",
      "TotalSales": 3770410.85
    }
  ]
  """

      analyst_output = "Enero 2013: 3.770.410,85 €"

      result = validate_table_coverage(query_result, analyst_output)

      assert "OK" in result