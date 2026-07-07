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
- [ ] **PERF — TOP PRIORITY: bucket index.** At 8.3k, search scans the whole snapshot every query (~1s on the free HF CPU; ~40ms locally). Build `SNAPSHOT_BY_SKILL = {skill_primary: [agents]}` at load. In `search_agents`, when `skill_words` present, gather candidates only from the relevant skill buckets (map via skill_kws) + a bounded name pass, instead of merging all `SNAPSHOT_AGENTS`. Target <300ms. Test locally: `SUPABASE_KEY=x python -c "import app; app.search_agents('video ai')"` — results must stay identical. `USE_SUPABASE` unset = git-native path.
- [x] SKILL_SYNONYMS (+30 keys) + relevance ranking — DONE.
- [x] harvest_osm.py (8 African cities) — DONE.
- [ ] Optional (only if DB ever returns): `searches` table for a persistent gap map.

### Opus 4.8 (orchestrate)
- [ ] On Samuel's Supabase re-login: restore the paused project, then bulk-seed the full harvest (10k+) into Supabase (not just the 1200 snapshot cap).
- [ ] Verify the MCP server end-to-end in a real Claude client once published.

### Blocked on Samuel (surface every session)
- [ ] Supabase re-login → unlocks full DB + 10k seeding.
- [ ] Set existing `TELEGRAM_TOKEN` on the Space → messaging live.
- [ ] Anthropic Console w/ `info@maji-safi.com` → submit (answers in `ANTHROPIC_APPLICATION.md`).
- [ ] YC submit by **Jul 27, 8pm PT** (`YC_APPLICATION.md`).
- [ ] Approve + post launch drafts (`POSTS.md`).
