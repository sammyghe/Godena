# Messaging on Hugging Face — blocked, then solved with an egress relay

**Diagnosed live, not assumed.** `GET /api/egress` on the Space returns:

| Target | Result |
|---|---|
| `api.github.com` | ok 200 |
| `example.com` | ok 200 |
| **`api.telegram.org`** | **ConnectTimeout — SSL handshake times out** |
| **`graph.facebook.com`** | **ConnectTimeout — SSL handshake times out** |

General internet access works. The **messaging APIs specifically are blocked** — almost certainly Hugging Face's anti-spam policy for free Spaces.

## SOLVED (no migration required)

Probing 10 relay strategies from inside the Space found working paths. `egress_request()`
in `app.py` now tries direct first, then falls back through `proxy.cors.sh` →
`allorigins` → `cors.eu.org`, including a query-string GET retry so POST replies
survive GET-only relays.

Verified live: `/api/channels` reports `@GodenaBot` with the webhook registered, and
`/api/sendtest` gets `chat not found` straight from Telegram — proving replies arrive.
The same path carries WhatsApp Cloud API once its credentials are set.

Trade-off: relayed requests transit a third party, so rotate tokens periodically or set
`CORS_RELAY` to your own relay. Moving to an open-egress host (below) removes the relay
entirely and is still the cleaner long-term answer.

## The original diagnosis

- **Telegram could never work from the Space**, with any token. This explains every previous failure.
- **WhatsApp Cloud API will not work from the Space either** — so completing the Meta setup while hosting here would have produced a bot that silently never replies.
- **Everything else is unaffected**: web search, the chat, the public API, and the MCP server all run fine on Hugging Face, because none of them make outbound calls to blocked hosts.

## The split that fixes it

Keep Hugging Face for what it does well, and put only the messaging webhooks somewhere with open egress:

```
Hugging Face Space          →  web search · /api/* · MCP · the chat   (works today)
A host with open egress     →  /webhook (WhatsApp) · /telegram        (the bot)
```

Both run the *same* `app.py` from this repo — it is one codebase; only the reachable hosts differ.

## Hosts that allow outbound to messaging APIs (free tiers)

| Host | Notes |
|---|---|
| **Render** | Free web service, Python/Docker. Spins down when idle (~50s cold start) — the existing keep-alive workflow solves that. Easiest Docker path. |
| **Koyeb** | Free instance, no forced sleep, Docker support. Good fit. |
| **Fly.io** | Free allowance, Docker, fast global. |
| **Railway** | Simple, trial credit then low cost. |
| **Vercel / Cloudflare Workers** | Instant and free, but serverless — would need the webhook split out rather than running the whole FastAPI app. |

The repo already has a `Dockerfile`, so Render/Koyeb/Fly deploy it as-is. Set the same secrets there (`WHATSAPP_TOKEN`, `WHATSAPP_PHONE_ID`, `TELEGRAM_TOKEN`) and point the provider webhooks at the new host instead of the Space. Godena self-registers its Telegram webhook on boot (see `autoconnect_channels`), so Telegram needs no manual wiring once it's on a host that can reach it.

## Until then — the channel that already works

`POST /api/chat` is the complete conversational Godena — search, register, rate, share — over plain HTTP, with **no account, no phone number, and no app**. It powers the chat on the website:

**https://sammyghe.github.io/Godena/**

That link is shareable today and needs nothing from anyone. Verify any host's suitability before investing setup time by deploying and hitting `/api/egress`.
