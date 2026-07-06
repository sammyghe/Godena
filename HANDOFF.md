# Godena — Multi-Model Handoff Queue

Standing task board so any model, in any session, picks up cold. **Protocol every session:**
1. Run the `godena-liveness` skill (`.claude/skills/godena-liveness/`).
2. Read this file, take the top task in YOUR lane.
3. Do it (tasks are sized ≤ 1 session, idempotent, resumable).
4. Update this file + `Desktop\Godena-strategy\STATE.md`.

## Model lanes
| Lane | Model | Owns |
|---|---|---|
| Final planning, audits, pivots | **Fable 5** (rare) | Strategy, quarterly review, this system's design |
| Orchestration, hard builds, DB | **Opus 4.8** | This queue's execution, Supabase restore, MCP polish |
| Build sprints | **Sonnet** | Seeders, endpoints, search-quality, Claude NLU |
| Ops + harvest + submissions | **Haiku** (cheap) | `godena-weekly`, run harvesters, registry submissions |

## Live facts
- Web: https://sammyghe.github.io/Godena/ · API: https://sammygh-godena.hf.space
- Index: embedded snapshot `data/agents_snapshot.json` (~886 real agents, cap 1200). Supabase (3,330) paused — restore needs Samuel re-login.
- Repo auto-deploys to the HF Space on push to `main`.

## QUEUE (top = do next)

### Haiku (ops)
- [ ] Weekly: run `godena-weekly`; append the report to STATE.md.
- [ ] Run `python seeders/harvest_hf.py 400` + `harvest_github.py` monthly; commit the grown snapshot.
- [ ] Submit the MCP server to Smithery, PulseMCP, Glama (see `mcp/README.md`).
- [ ] Submit Godena to directories in `Godena-strategy/POSTS.md` (there's-an-ai-for-that, aiagentsdirectory).

### Sonnet (build)
- [ ] Expand `SKILL_SYNONYMS` in app.py: add `research, sales, support, writing, voice, video, automation, agent-framework` → fixes ai-mode queries returning generic top-rep. KNOWN GAP.
- [ ] Add `harvest_osm.py` (Overpass API, phone/website-tagged businesses in Kampala/Nairobi/Lagos) — human-services mass source. Skeleton described in the plan.
- [ ] When DB restored: add a `searches` table + log every query (persistent gap map), and a `refresh_snapshot` script (top ~1000 by reputation → snapshot).

### Opus 4.8 (orchestrate)
- [ ] On Samuel's Supabase re-login: restore the paused project, then bulk-seed the full harvest (10k+) into Supabase (not just the 1200 snapshot cap).
- [ ] Verify the MCP server end-to-end in a real Claude client once published.

### Blocked on Samuel (surface every session)
- [ ] Supabase re-login → unlocks full DB + 10k seeding.
- [ ] Set existing `TELEGRAM_TOKEN` on the Space → messaging live.
- [ ] Anthropic Console w/ `info@maji-safi.com` → submit (answers in `ANTHROPIC_APPLICATION.md`).
- [ ] YC submit by **Jul 27, 8pm PT** (`YC_APPLICATION.md`).
- [ ] Approve + post launch drafts (`POSTS.md`).
