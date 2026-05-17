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


def test_table_validator_checks_all_time_series_rows_by_default():
    query_result = """
[
  {
    "Year": 2013,
    "MonthName": "January",
    "TotalSales": 100
  },
  {
    "Year": 2013,
    "MonthName": "February",
    "TotalSales": 200
  },
  {
    "Year": 2013,
    "MonthName": "March",
    "TotalSales": 300
  },
  {
    "Year": 2013,
    "MonthName": "April",
    "TotalSales": 400
  },
  {
    "Year": 2013,
    "MonthName": "May",
    "TotalSales": 500
  },
  {
    "Year": 2013,
    "MonthName": "June",
    "TotalSales": 600
  },
  {
    "Year": 2013,
    "MonthName": "July",
    "TotalSales": 700
  },
  {
    "Year": 2013,
    "MonthName": "August",
    "TotalSales": 800
  },
  {
    "Year": 2013,
    "MonthName": "September",
    "TotalSales": 900
  },
  {
    "Year": 2013,
    "MonthName": "October",
    "TotalSales": 1000
  },
  {
    "Year": 2013,
    "MonthName": "November",
    "TotalSales": 1100
  }
]
"""

    analyst_output = """
Enero 2013: 100
Febrero 2013: 200
Marzo 2013: 300
Abril 2013: 400
Mayo 2013: 500
Junio 2013: 600
Julio 2013: 700
Agosto 2013: 800
Septiembre 2013: 900
Octubre 2013: 1000
"""

    result = validate_table_coverage(query_result, analyst_output)

    assert "REVISAR" in result
    assert "1100" in result
  
