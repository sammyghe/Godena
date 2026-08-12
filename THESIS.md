# The agent economy has no last mile

**AI agents can't reach — or get paid by — most of the world.**

Godena is the discovery, trust, and access rail for AI agents and real services on messaging: the last mile of the agent economy for the three billion people who will never use an app store.

---

## The assumption nobody is examining

Every AI agent shipped in the last two years assumes the same stack:

> a browser · an app store · an API key · a credit card

That is the stack of maybe a billion people. The next three billion have a different one:

> **WhatsApp · a phone number · mobile money**

The entire industry is racing to make agents *smarter*. Almost nobody is building the rail that lets them **reach**, be **trusted by**, or be **paid by** most of humanity. Capability is compounding fast; distribution to the majority of the planet is not moving at all.

That gap is not a market segment. It is a missing layer in the stack.

## What is actually missing

Ask a person in Kampala to use an AI agent today and you hit three walls in order:

1. **They can't find it.** Agent directories are web apps aimed at developers. In WhatsApp — where a billion people already live — there is no search at all. Not for agents, not for services, not for anything.
2. **They can't trust it.** A listing is not trust. Trust in these markets is social: *do you know a guy?* Nothing digital carries that signal, so people fall back on group chats and word of mouth, which don't scale and can't be queried.
3. **They can't pay it.** Every agentic-payment rail shipped in 2026 — Stripe's MCP server, Coinbase's x402, AP2, even Paystack's — is card- or crypto-first. An AI agent literally cannot pay a Nairobi mechanic who takes M-Pesa.

Find, trust, pay. Three walls, one missing rail.

## Why "AI agents" and "a Kampala pharmacy" are the same thing

This is the part that reads as a category error and isn't.

To a person with a need, an agent is **anything that can do the job**: a lawyer, a pharmacy, a mechanic, a video-generation model, a research agent. The distinction between "AI agent" and "human business" is an artifact of how software people organize the world, not how a person with a problem experiences it.

So Godena's unit is not "an AI agent." It is:

> **a thing that can do a job for you — reachable, and rated.**

Godena indexes both, because in the messaging-first world the distinction is meaningless. Nobody else does this, because nobody else is standing here.

## Why now

Four things became true at once:

- **Protocols arrived.** MCP, A2A, x402, AP2, `llms.txt` — agents can now be described, discovered, and called programmatically. The plumbing for an open agent layer exists for the first time.
- **Agent supply exploded.** Hundreds of thousands of models, tools, and agents now exist, with no consumer-grade way to find the right one.
- **Messaging became the operating system** for the next three billion — not a channel *on* the internet, but *the* internet for most of Africa, South Asia, and Latin America.
- **The economics of reaching them are open — briefly.** Reply-only services on WhatsApp's official API currently sit in a free lane. Meta has announced that changes on **October 1, 2026**. There is a window to establish the rail while it costs nothing.

## The product

Three layers. Two are live today.

| Layer | What it does | State |
|---|---|---|
| **Find** | Search 8,300+ AI agents and real services in one index, ranked by relevance | **Live** — web, API, MCP |
| **Trust** | Reputation earned through real interactions and ratings, not self-declaration | **Built**, accumulating |
| **Reach + Pay** | WhatsApp access + mobile-money payment intent | **The missing, defensible piece** |

It runs git-native: the registry is an open, versioned file in the repository. No database to pause, no server to bill, no company to trust. Search cannot be taken offline by an infrastructure failure, and the data is as open as the code.

## The two-way gateway

Godena is being built to run in both directions, and this is the part that makes it infrastructure rather than a directory.

**Inbound — messaging to agents.** A person in Kampala texts a plain sentence and reaches any agent or service, including ones that only speak MCP or REST. No app, no API key, no card. Godena translates chat into agent protocol.

**Outbound — agents to the real world.** Any AI agent — Claude, ChatGPT, an autonomous system — that needs to *do something real* in an emerging market calls Godena. Ask a frontier model today to "find a verified water supplier in Kampala and contact them" and it cannot. Godena is the tool that makes that possible.

This is the Paystack pattern. Paystack didn't chase app downloads; it put payments *inside* the models via an MCP server. Godena does the same for finding and trusting real-world capacity.

## Why this is defensible

The code is open source and always will be — so the code is explicitly not the moat. Three things are:

- **The trust graph.** A fork copies the index in one command. It cannot copy reputation earned through real interactions. Trust data compounds and cannot be cloned.
- **Structural non-spam.** Godena only ever replies; it never initiates. It is architecturally incapable of the unsolicited outbound that gets competitors banned from messaging platforms. Anyone approaching this from a marketing-blast background cannot follow.
- **Standing in the market.** The wedge is emerging-market services, indexed by people who live there. That is not a dataset you buy.

## The honest counter-case

Anyone serious will raise these, so here they are first.

*Discovery businesses monetize through ads or take-rate, and this has renounced both.* Correct. The introduction stays free permanently; revenue sits **beside** the connection — verified-identity badges for providers, and B2B API access to the trust graph for platforms and AI assistants that need vetted real-world capacity. Never a toll on the free introduction.

*The reputation graph is empty until real usage.* Also correct, and it is the single biggest risk. It is why usage — not index size — is the only metric that matters here.

*Meta could build or absorb this.* True, and it is simultaneously the acquisition thesis and the risk. Platform-owned directories (Claude Skills, the GPT Store) have never been open or cross-platform; that is the space Godena occupies. Mitigation is multi-channel: web, API, and MCP are already live, so no single platform is fatal.

*It's small.* It starts small on purpose. Own agent and service discovery in one city, on one channel, completely — then expand along the same primitive. Every rail that mattered started as a toy in a market nobody was defending.

## Where it stands

Live and working: **8,300+** indexed AI agents and real services, searchable on the web, through a free public API, and inside Claude via MCP. Open source (MIT), git-native, running at approximately zero cost. Pre-users by design — the product was built first so that the demand test would be honest.

Built in Kampala, by a founder who runs a licensed manufacturing business in the same market, and who has spent years finding suppliers, lawyers, and technicians the hard way — by asking around.

- **Try it:** https://sammyghe.github.io/Godena/
- **Source:** https://github.com/sammyghe/Godena
- **Use it from an AI agent:** `/.well-known/agent-card.json` · `/llms.txt` · MCP server in `mcp/`

---

*Godena is open source and free forever. The network grows when you add to it.*
