import re


def extract_sql_from_markdown(text: str) -> str:
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    return text.strip()