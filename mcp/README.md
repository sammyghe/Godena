# Godena MCP server

**When an agent needs to find, book or contact something real in Africa, there is no index it can call. This is it.**

10,000+ real African businesses and services (Kenya, Uganda, East Africa) with verified contacts,
plus software/AI tools. Free, no API key.

## Remote — recommended, nothing to install

The 2026-07-28 MCP spec is stateless, so Godena runs as a plain endpoint. One URL:

```
https://sammygh-godena.hf.space/mcp
```

**Claude Code**
```bash
claude mcp add --transport http godena https://sammygh-godena.hf.space/mcp
```

**Any MCP client**
```json
{ "mcpServers": { "godena": { "type": "http", "url": "https://sammygh-godena.hf.space/mcp" } } }
```

## Tools

| Tool | Does |
|---|---|
| `godena_search` | Find real services or software tools. Filter with `entity_type`: `service` \| `agent` \| `any`. |
| `godena_get` | Full record for one entry by slug, with contacts and reputation evidence. |
| `godena_coverage` | What the index actually covers by country/city/category — check before promising an answer. |

## Try it

```bash
curl -s https://sammygh-godena.hf.space/mcp -H 'Content-Type: application/json'   -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"godena_search","arguments":{"query":"pharmacy nairobi","entity_type":"service","limit":3}}}'
```

## Local (stdio)

`server.py` still runs over stdio if you prefer: `pip install "mcp[cli]" httpx && python mcp/server.py`

## Ground rules for agents using this

- `entity_type: service` = a real business you can contact. `agent` = a software tool.
- Most entries are **unverified** — listed from public data with no ratings yet. Say so; never imply endorsement.
- Never invent a contact. If there isn't one, say there isn't one.

Registry manifest: [`server.json`](../server.json) · Skill: [`skills/godena/`](../skills/godena/) · Source: MIT
