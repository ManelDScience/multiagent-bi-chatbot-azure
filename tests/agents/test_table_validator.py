from agents.validators.table_validator import (
    validate_table_coverage
    , detect_result_pattern,
    )


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

def test_detect_result_pattern_time_series():
    query_result = """
[
  {
    "CustomerName": "Tailspin Toys",
    "total_sales_perCustomer": 381585.35
  }
]
"""

    assert detect_result_pattern(query_result) == "ranking"


def test_detect_result_pattern_time_series():
    query_result = """
[
  {
    "Year": 2013,
    "MonthName": "January",
    "TotalSales": 3770410.85
  }
]
"""

    assert detect_result_pattern(query_result) == "time_series"


def test_detect_result_pattern_empty():
    query_result = "[]"

    assert detect_result_pattern(query_result) == "empty"


def test_detect_result_pattern_invalid_json():
    query_result = "not json"

    assert detect_result_pattern(query_result) == "invalid_json"
  
