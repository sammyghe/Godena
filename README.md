---
title: Godena
emoji: 🌐
colorFrom: green
colorTo: blue
sdk: docker
pinned: false
---
# Godena — The Open Agent Network

> Text what you need. Get connected.

**WhatsApp:** +256761966728  
**Telegram:** @GodenaBot  
**Live at:** [sammygh-godena.hf.space](https://sammygh-godena.hf.space)

---

## What it does

One number. You text it what you need.  
Godena finds the best matching agent or service, returns three results, and steps back.  
Your conversation. Your business. Godena just made the introduction.

```
lawyer kampala      →  Uganda Law Society + real WhatsApp contact
tax kenya           →  Kenya Revenue Authority (KRA)
flights nairobi     →  Kenya Airways + Ethiopian Airlines + KLM
send money africa   →  Wise + Chipper Cash + WorldRemit
ai coding           →  Claude + ChatGPT + Cursor + Groq
china sourcing      →  Alibaba + Yiwu sourcing agents
```

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
Godena steps back — conversation is yours
```

No middleman. No commission. No data sold.  
Godena connects and leaves.

## Fork for your city or niche marekt or service 

Clone this. Change a few lines. Deploy your own Godena for your community.

```bash
git clone https://github.com/sammygedamua/godena
cd godena
# Add your own secrets in HuggingFace Space settings
# Deploy to HuggingFace Spaces (free)
```

A Lagos mechanic network. An SF African business directory.  
A Nairobi legal referral system. All the same code, different registries.

## Architecture

- **Bot:** FastAPI running on HuggingFace Spaces (free tier)
- **Database:** Supabase (Postgres) — up to 800k agents on free tier
- **WhatsApp:** Green API (inbound webhook)
- **Telegram:** Webhook mode (no polling, works on free hosting)
- **Search:** Skill-first filtering + reputation ranking in Python
- **Reputation:** Uber + Airbnb + Upwork + Yelp + GitHub models combined

## API

Register an agent programmatically:

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

## Built by

**Samuel Gedamua** — Founder.  
**Amanuel Asmerom** — Co-Founder  

First agent: Emmas_cars Kampala — March 11 2026  
Co-built with Claude (Anthropic)

---

*Open source. Free forever. The network grows when you add to it.*
