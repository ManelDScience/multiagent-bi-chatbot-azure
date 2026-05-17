import json
import re
from typing import Any

MONTH_TRANSLATIONS = {
    "january": ["january", "enero"],
    "february": ["february", "febrero"],
    "march": ["march", "marzo"],
    "april": ["april", "abril"],
    "may": ["may", "mayo"],
    "june": ["june", "junio"],
    "july": ["july", "julio"],
    "august": ["august", "agosto"],
    "september": ["september", "septiembre"],
    "october": ["october", "octubre"],
    "november": ["november", "noviembre"],
    "december": ["december", "diciembre"],
}


def detect_result_pattern(query_result: str) -> str:
    try:
        data = json.loads(query_result)
    except Exception:
        return "invalid_json"
    
    if not data:
        return "empty"
    
    if not isinstance(data, list):
        return "invalid_json"
    
    if not all(isinstance(row, dict) for row in data):
        return "invalid_json"
    
    columns = set()
    for row in data:
        columns.update(row.keys())

    normalized_columns = {column.lower() for column in columns}

    has_time = any(
        column in normalized_columns
        for column in ["year", "month", "monthname", "monthnumer", "yearmonth", "date"]
    )

    has_customer_or_name = any(
        column in normalized_columns
        for column in ["customername", "customer", "name"]
    )

    has_metric = any(
        any(keyword in column for keyword in ["sales", "ventas", "total", "amount", "revenue"])
        for column in normalized_columns
    )

    if has_time and has_metric:
        return "time_series"
    
    if has_customer_or_name and has_metric:
        return "ranking"
    
    return "simple_table"


def get_rows_to_check_by_pattern(
    rows: list[dict],
    pattern: str,
    max_rows_to_check: int,
) -> list[dict]:
    if pattern == "time_series":
        return rows[:max(max_rows_to_check, 100)]

    if pattern == "ranking":
        return rows[:max_rows_to_check]

    return rows[:max_rows_to_check]


def parse_query_result(query_result: str) -> list[dict[str, Any]]:
    try:
        data = json.loads(query_result)
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def normalize_number(value: Any) -> str:
    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")

    return str(value)


def to_european_number(value: Any) -> str:
    try:
        number = float(value)
    except (ValueError, TypeError):
        return str(value)

    formatted = f"{number:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def value_appears_in_text(value: Any, text: str) -> bool:
    text_lower = text.lower()

    raw = str(value).lower()
    normalized = normalize_number(value).lower()
    european = to_european_number(value).lower()

    variants = {
        raw,
        normalized,
        european,
        european.rstrip("0").rstrip(","),
    }

    if raw in MONTH_TRANSLATIONS:
        variants.update(MONTH_TRANSLATIONS[raw])

    return any(variant in text_lower for variant in variants if variant)


def validate_table_coverage(
    query_result: str,
    analyst_output: str,
    max_rows_to_check: int = 10,  
) -> str:
    rows = parse_query_result(query_result)
    pattern = detect_result_pattern(query_result)
    if pattern == "time_series":
        max_rows_to_check = max(max_rows_to_check, 100)

    if not rows:
        return f"""
    ## Table Validator

    Pattern detected: {pattern}

    REVISAR

    - El resultado SQL está vacío o no se pudo interpretar como JSON.
    """

    rows_to_check = get_rows_to_check_by_pattern(
        rows=rows,
        pattern=pattern,
        max_rows_to_check=max_rows_to_check,
    )

    missing_values = []

    for row in rows_to_check:
        for value in row.values():
            if not value_appears_in_text(value, analyst_output):
                missing_values.append(str(value))

    if missing_values:
        return f"""
## Table Validator

Pattern detected: {pattern}

REVISAR

- Algunas cifras o valores del resultado SQL podrían no aparecer explícitamente en la respuesta.
- Valores no encontrados directamente: {missing_values[:10]}
"""

    return f"""
## Table Validator

Pattern detected: {pattern}

OK

- La respuesta cubre los primeros {len(rows_to_check)} registros del resultado SQL.
- No se detectan omisiones evidentes en los valores principales.
"""

