import "dotenv/config";
import express from "express";
import sql from "mssql";
import { z } from "zod";
import { randomUUID } from "node:crypto";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

/* =========================
   SQL CONFIG
========================= */

const sqlConfig = {
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  server: process.env.DB_SERVER,
  database: process.env.DB_NAME,
  port: 1433,
  options: {
    encrypt: true,
    trustServerCertificate: false,
    connectionTimeout: 30000,
    requestTimeout: 60000,
  },
};

let pool;

async function getPool() {
  if (!pool) {
    pool = await sql.connect(sqlConfig);
  }

  return pool;
}

/* =========================
   SAFE SQL EXECUTION
========================= */

function validateSelectOnly(query) {
  const cleanQuery = query.trim();
  const lowerQuery = cleanQuery.toLowerCase();

  if (!lowerQuery.startsWith("select")) {
    throw new Error("Only SELECT queries are allowed");
  }

  const forbiddenKeywords = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "truncate",
    "create",
    "merge",
    "exec",
    "execute",
  ];

  for (const keyword of forbiddenKeywords) {
    const pattern = new RegExp(`\\b${keyword}\\b`, "i");

    if (pattern.test(cleanQuery)) {
      throw new Error(`Forbidden SQL keyword detected: ${keyword}`);
    }
  }

  return cleanQuery;
}

async function runQuery(query) {
  const cleanQuery = validateSelectOnly(query);

  const p = await getPool();

  const result = await p.request().query(cleanQuery);

  return result.recordset;
}

/* =========================
   MCP SERVER
========================= */

function buildServer() {
  const server = new McpServer({
    name: "azure-sql-mcp",
    version: "1.0.0",
  });

  server.registerTool(
    "query",
    {
      title: "SQL Query",
      description: "Execute read-only SELECT query against Azure SQL Database",
      inputSchema: z.object({
        query: z.string().describe("SQL SELECT query to execute"),
      }),
    },
    async ({ query }) => {
      try {
        const data = await runQuery(query);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      } catch (err) {
        return {
          content: [
            {
              type: "text",
              text: `Error: ${err?.message || String(err)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  server.registerTool(
    "list_views",
    {
      title: "List SQL Views",
      description: "List available views in Azure SQL Database",
      inputSchema: z.object({
        search: z
          .string()
          .optional()
          .describe("Optional text to filter view names"),
      }),
    },
    async ({ search }) => {
      try {
        let query = `
          SELECT 
            TABLE_SCHEMA,
            TABLE_NAME
          FROM INFORMATION_SCHEMA.VIEWS
        `;

        if (search) {
          const safeSearch = search.replaceAll("'", "''");

          query += `
            WHERE TABLE_NAME LIKE '%${safeSearch}%'
          `;
        }

        query += `
          ORDER BY TABLE_SCHEMA, TABLE_NAME
        `;

        const data = await runQuery(query);

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(data, null, 2),
            },
          ],
        };
      } catch (err) {
        return {
          content: [
            {
              type: "text",
              text: `Error: ${err?.message || String(err)}`,
            },
          ],
          isError: true,
        };
      }
    }
  );

  return server;
}

/* =========================
   MCP HTTP TRANSPORT
========================= */

const transports = new Map();

app.all("/mcp", async (req, res) => {
  try {
    const sessionId = req.header("mcp-session-id");

    let transport = sessionId ? transports.get(sessionId) : undefined;

    if (!transport) {
      transport = new StreamableHTTPServerTransport({
        sessionIdGenerator: () => randomUUID(),
        enableJsonResponse: true,
        onsessioninitialized: (id) => {
          transports.set(id, transport);
        },
      });

      transport.onclose = () => {
        if (transport.sessionId) {
          transports.delete(transport.sessionId);
        }
      };

      const server = buildServer();

      await server.connect(transport);
    }

    await transport.handleRequest(req, res, req.body);
  } catch (err) {
    console.error("MCP endpoint error:", err);

    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: "2.0",
        error: {
          code: -32603,
          message: err?.message || "Internal server error",
        },
        id: req.body?.id ?? null,
      });
    }
  }
});

/* =========================
   HEALTH CHECK
========================= */

app.get("/", (_req, res) => {
  res.status(200).send("MCP Server OK");
});

/* =========================
   START SERVER
========================= */

app.listen(PORT, "0.0.0.0", () => {
  console.log(`MCP Server running on port ${PORT}`);
});
