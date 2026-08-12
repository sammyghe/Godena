---
title: Godena
emoji: 🌐
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Godena

**AI agents can't reach — or get paid by — most of the world.**
Godena is the discovery, trust, and access rail for AI agents and real services on messaging.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Live search](https://img.shields.io/badge/try%20it-sammyghe.github.io%2FGodena-1d9e75.svg)](https://sammyghe.github.io/Godena/)
[![Read the thesis](https://img.shields.io/badge/read-THESIS.md-blue.svg)](THESIS.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-1d9e75.svg)](CONTRIBUTING.md)

### ▶ Try it now — no app, no login, no account
- **Web:** **[sammyghe.github.io/Godena](https://sammyghe.github.io/Godena/)** ← live, works today
- **API:** `GET` [sammygh-godena.hf.space/api/search?q=lawyer+kampala](https://sammygh-godena.hf.space/api/search?q=lawyer+kampala)
- **From an AI agent:** MCP server in [`mcp/`](mcp/) · [`/llms.txt`](https://sammygh-godena.hf.space/llms.txt) · [agent card](https://sammygh-godena.hf.space/.well-known/agent-card.json)

**→ [Read the thesis](THESIS.md)** — why the agent economy has no last mile, and what that's worth building.

---

## What it is

Every AI agent shipped in the last two years assumes the same stack: **a browser, an app store, an API key, a credit card.** That's the stack of about a billion people. The next three billion have a different one: **WhatsApp, a phone number, and mobile money.**

The industry is racing to make agents smarter. Almost nobody is building the rail that lets them **reach**, be **trusted by**, or be **paid by** most of humanity.

Godena is that rail. You type what you need — a lawyer, a mechanic, a pharmacy, a video model, a sourcing agent — and Godena returns the best matches ranked by earned reputation, each with a real link. Then it steps back. No middleman, no commission, no data sold.

**Why a Kampala pharmacy and a Hugging Face model sit in the same index:** to a person with a need, an agent is *anything that can do the job*. That distinction is an artifact of how software people organize the world, not how a person with a problem experiences it. Godena's unit is **"a thing that can do a job for you — reachable, and rated."**

```
lawyer kampala      →  Uganda Law Society + real WhatsApp contact
flights nairobi     →  Kenya Airways + Ethiopian Airlines + KLM
send money africa   →  Wise + Chipper Cash + WorldRemit
ai coding           →  Claude + Cursor + Groq
china sourcing      →  Alibaba + Yiwu sourcing agents
```

## The three layers

| Layer | What it does | State |
|---|---|---|
| **Find** | Search 8,300+ AI agents and real services in one index | **Live** — web, API, MCP |
| **Trust** | Reputation earned through real interactions, not self-declaration | **Built**, accumulating |
| **Reach + Pay** | Messaging access + mobile-money payment intent | **In progress** — the defensible piece |

## Channels

- **Web + API + MCP** — live now. Any LLM can call Godena to find and verify real-world capacity.
- **WhatsApp** — reply-only on Meta's official Cloud API. Godena never messages first, so it needs no templates and cannot spam. Free to run today. → [docs/SETUP_WHATSAPP.md](docs/SETUP_WHATSAPP.md) (works with Meta's free test number — no phone number to buy).
- **Telegram** — [@GodenaBot](https://t.me/GodenaBot).

## Why this is a network, not an app

Software is becoming free — anyone can clone this repo and run it tonight. So the code is not the moat, and we do not pretend it is. We open-sourced it on purpose.

The moat is the **network**: the registry of agents, the reputation earned through real jobs, and the demand signal of what people actually search for. Every search, every rating, every claimed business makes the network more useful for the next person — and that value compounds in one place even when the code is everywhere. Open networks tend to win, because the value lives in the graph, not the binary.

## How it works

```
User texts Godena
       ↓
Search engine matches skill + location
       ↓
Reputation engine ranks results
       ↓
Top 3 returned with real contact links
       ↓
Godena steps back — the conversation is yours
```

No middleman. No commission. No data sold.

## Architecture

- **Bot:** FastAPI on Hugging Face Spaces (free tier)
- **Database:** Supabase (Postgres) — hundreds of thousands of agents on the free tier
- **WhatsApp:** Green API (inbound webhook)
- **Telegram:** Webhook mode (no polling, works on free hosting)
- **Search:** skill-first filtering + reputation ranking
- **Reputation:** an evidence-weighted score combining identity, performance, peer trust, and external signals

All secrets live in environment variables / Hugging Face Space settings — never in the code. See [SECURITY.md](SECURITY.md).

## API

Godena is open infrastructure. Any developer, platform, or AI agent can register and be discovered — free, forever.

Register an agent:

```bash
curl -X POST https://sammygh-godena.hf.space/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My_Service_Name",
    "skill": "legal",
    "location": "nairobi",
    "country": "kenya",
    "whatsapp": "https://wa.me/254712345678"
  }'
```

Search:

```
GET /api/search?q=lawyer+kampala
```

See the running service root (`/`) for the full list of endpoints (register, claim, rate, endorse, complete, gaps).

## Run your own / fork a city

Clone it. Change a few lines. Deploy your own Godena for your community.

```bash
git clone https://github.com/sammyghe/Godena
cd Godena
# Add your own secrets in Hugging Face Space settings (never commit them)
# Deploy to Hugging Face Spaces (free)
```

A Lagos mechanic network. An SF African-business directory. A Nairobi legal-referral line. Same code, different registries. The networks can stay separate or federate — your call. See [CONTRIBUTING.md](CONTRIBUTING.md) to add agents or improve the core.

## Roadmap

We are early — Stage 1 of 5 (a working directory). The path to a real reputation network and beyond is in [docs/ROADMAP.md](docs/ROADMAP.md). The contributions that move us fastest are **real, verified agents** — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Built by

**Samuel Gedamua** — Founder.
**Amanuel Asmerom** — Co-Founder.

First agent: Emmas_cars Kampala — March 11 2026.
Co-built with Claude (Anthropic).

## License

[MIT](LICENSE) — free forever. The network grows when you add to it.
