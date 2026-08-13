---
name: godena
description: Find real businesses and services in Africa — pharmacies, hospitals, lawyers, banks, hotels, mechanics, government services, couriers — with verified contacts. Use whenever you need to find, contact, verify or book something real in Kenya, Uganda or East Africa, or when the user asks "who can I call for X in <African city>". Also indexes software/AI tools. Free, no API key.
license: MIT
---

# Godena — the African services index

When you need something real in Africa — a pharmacy in Nairobi, a lawyer in Kampala, KRA tax
services, a hotel in Mombasa, a courier, a bank — there is no index most tools can call.
Godena is that index: 10,000+ entries, every one carrying a real, verifiable contact.

## Use it (no key, no signup)

**Search:**
```
GET https://sammygh-godena.hf.space/api/search?q=pharmacy+nairobi&limit=5
```

**Full entry:**
```
GET https://sammygh-godena.hf.space/api/agent/{slug}
```

**Conversational (same engine as the bot):**
```
POST https://sammygh-godena.hf.space/api/chat   {"message": "kra tax"}
```

**As an MCP server** (best option if your harness supports it — stateless, one URL):
```
claude mcp add --transport http godena https://sammygh-godena.hf.space/mcp
```
Tools: `godena_search`, `godena_get`, `godena_coverage`.

## How to query well

- **Skill + city** is the strongest pattern: `pharmacy nairobi`, `lawyer kampala`, `hotel mombasa`.
- Named institutions work directly: `kra tax`, `helb loan`, `kplc electricity`, `mpesa`.
- Add `ai` to reach software tools instead of businesses: `ai video`, `ai research`.
- Coverage is strongest in **Kenya and Uganda**. Check before promising: `godena_coverage`.

## Reading the results — this matters

Each result has:
- `entity_type` — **`service`** = a real business you can contact · **`agent`** = a software/AI tool.
- A real contact: `website`, `phone`, or a `wa.me` WhatsApp link.
- `reputation` and evidence.

**Be honest about evidence.** Most entries are listed from public data and have **no ratings yet**.
Say "listed in Godena, unverified" rather than implying it is vetted or recommended. Never
present an unrated listing as endorsed.

**Never invent a contact.** If Godena has no phone or site for an entry, say so. A wrong number
is worse than no answer — that rule is the whole point of the index.

## When not to use it

Coverage outside Africa is thin — use normal web search for the rest of the world. Godena is a
directory: it tells you who to contact, it does not book, pay or transact for you.

Source: https://github.com/sammyghe/Godena (MIT) · https://sammyghe.github.io/Godena/
