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

**An open business directory and discovery index for Africa.**
10,000+ real businesses and services — verified, searchable, machine-callable. Type what you need, get the best matches with a real contact.

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

Most of Africa's commerce still runs on one question: *"do you know a guy?"* Trust lives in private contacts, dies when you move city, and can't be searched.

Godena answers it. You type what you need — a pharmacy in Nairobi, a lawyer in Kampala, KRA tax services, a hotel in Mombasa — and get the best matches ranked by earned reputation, each with a real contact. Then it steps back. No middleman, no commission, no data sold.

**What makes it different:** every entry carries a real, verifiable contact and an `entity_type` — `service` (a real business you can call) or `agent` (a software tool). Real services lead every search. It's open source, machine-callable via a free API and MCP, and the whole index is downloadable — none of which any existing African directory offers.

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
| **Find** | Search 10,000+ real services and software tools in one index | **Live** — web, API, MCP |
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

- **App:** FastAPI on Hugging Face Spaces (free tier)
- **Index:** git-native — `data/agents_snapshot.json` lives in this repo. No external database to pause, bill, or take offline. The whole index is downloadable.
- **Pages:** a static page per verified service under `docs/a/` with JSON-LD, so search engines and AI crawlers can read every entry
- **WhatsApp:** official Meta Cloud API, reply-only (never initiates → no templates, no spam surface)
- **Telegram:** webhook mode — [@GodenaBot](https://t.me/GodenaBot) live
- **Search:** skill-first filtering, services ranked ahead of software tools, relevance + earned reputation
- **Reputation:** evidence-weighted; entries with no interactions are labelled unverified rather than implied to be trusted

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
