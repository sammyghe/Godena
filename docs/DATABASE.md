# Does Godena have to run on Supabase?

Short answer: **no — and as of July 2026 it no longer fully depends on it.**

## The problem this answers

Godena's registry lived only in a free-tier Supabase project. Free projects pause after ~7 days idle, and a paused project's API hostname is deprovisioned — so search returned zero results even though all data was intact. The database was the single point of failure for the whole product.

## The architecture now: three layers of resilience

1. **Primary — Supabase Postgres.** Live reputation, ratings, registrations, the full registry. Still the system of record.
2. **Keep-alive — GitHub Actions cron** (`.github/workflows/keepalive.yml`). Pings `/health` (which touches the DB) every ~10 minutes: the HF Space never sleeps, Supabase never idles into a pause. Back it up with a free external pinger (cron-job.org / UptimeRobot) since GitHub disables cron on repos inactive for 60 days.
3. **Embedded snapshot — `data/agents_snapshot.json`.** A curated registry of real, verified agents (official websites only) ships inside the repo and loads into memory at startup. Search always merges it in (DB rows win by slug), and when the database is unreachable the snapshot carries search alone. **The core product — search — can no longer fully die.** `/health` reports which mode is active.

Degradation contract: with the DB down, search works from the snapshot; registrations and ratings fail gracefully and users are asked to retry later.

## If/when to move off Supabase

| Option | Why | When |
|---|---|---|
| Stay (free) + layers above | $0, data already there | Now — default |
| **Neon Postgres (free)** | Compute suspends but **auto-resumes on any connection** — no manual dashboard resume, the exact failure Supabase has | First choice if a migration happens; near drop-in (Postgres) |
| Turso / libSQL (free) | Generous free tier, no pause | Alternative; more code changes (not Postgres wire) |
| Supabase Pro ($25/mo) | No pausing, backups | When funded |

Migration is simple by design: one `agents` table (see `Desktop`-side `schema.sql` in the maintainers' recovery kit), `pg_dump` → restore, change `SUPABASE_URL`/`SUPABASE_KEY`. The snapshot layer keeps search alive during any migration.

## Refreshing the snapshot

When the database is healthy, regenerate the snapshot from the top verified agents (highest reputation, claimed/verified first) and commit it. Never hand-edit fake entries in — every snapshot agent must be a real, verifiable service with its official website. See `CONTRIBUTING.md`'s no-fake-data rule.
