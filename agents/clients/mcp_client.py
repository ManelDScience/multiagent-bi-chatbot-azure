import requests
from typing import Optional


MCP_URL = "http://localhost:3000/mcp"

_session_id = None


def initialize_mcp() -> Optional[str]:
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "python-agent-client",
                "version": "1.0.0",
            },
        },
    }

    response = requests.post(
        MCP_URL,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.headers.get("mcp-session-id")


def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    global _session_id

    if not _session_id:
        _session_id = initialize_mcp()

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    if _session_id:
        headers["mcp-session-id"] = _session_id

    response = requests.post(
        MCP_URL,
        json=payload,
        headers=headers,
        timeout=60,
    )

    if response.status_code >= 400:
        print("MCP ERROR STATUS:", response.status_code)
        print("MCP ERROR BODY:", response.text)

    response.raise_for_status()

    data = response.json()

    if "error" in data:
        raise RuntimeError(data["error"])

    content = data["result"]["content"]

    if not content:
        return ""

    return content[0]["text"]


def execute_sql(query: str) -> str:
    return call_mcp_tool(
        tool_name="query",
        arguments={"query": query},
    )


def list_views(search: Optional[str] = None) -> str:
    arguments = {}

    if search:
        arguments["search"] = search

    return call_mcp_tool(
        tool_name="list_views",
        arguments=arguments,
    )

def get_columns(schema: str, table: str) -> str:
    query = f"""
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = '{schema}'
  AND TABLE_NAME = '{table}'
ORDER BY ORDINAL_POSITION;
"""
    return execute_sql(query)