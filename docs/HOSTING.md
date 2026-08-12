# Why messaging doesn't work on Hugging Face — and where to host it

**Diagnosed live, not assumed.** `GET /api/egress` on the Space returns:

| Target | Result |
|---|---|
| `api.github.com` | ok 200 |
| `example.com` | ok 200 |
| **`api.telegram.org`** | **ConnectTimeout — SSL handshake times out** |
| **`graph.facebook.com`** | **ConnectTimeout — SSL handshake times out** |

General internet access works. The **messaging APIs specifically are blocked** — almost certainly Hugging Face's anti-spam policy for free Spaces.

## What this means

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
