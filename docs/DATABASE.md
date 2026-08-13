# How Godena stores things — finder + judgment, not a phonebook

Godena does **not** keep a private copy of the world's phone numbers. It stores the
layer that doesn't exist anywhere else — *which businesses are real, worth contacting,
and what people are asking for* — plus **pointers** back to the public sources that
hold the volatile facts.

## Why, in numbers

Measured on the live index:

| Finding | Number | Consequence |
|---|---|---|
| Storage per entry | ~422 bytes | 1M entries ≈ 0.4 GB of git — a miserable repo. Millions-as-stored-records is not viable. |
| Services with a phone | 1,567 (70%) | We were warehousing the volatile, rot-prone field. |
| Services with `osm_id` | 0 (before this change) | We had thrown away the stable pointer that lets an entry be re-resolved for free. |
| Phones resembling personal mobiles | ~527 | Kenya's Data Protection Act 2019 makes bulk-warehousing personal contacts a real exposure. |

We were storing the commodity that rots and creates liability, and none of the thing
nobody else has.

## The layers

| Layer | Contents | Where |
|---|---|---|
| **Canonical** — own it, permanent, tiny | slug, name, category, `entity_type`, geo, **pointers** (`osm_id`, official domain) | `data/agents_snapshot.json` + `data/godena.db` |
| **Judgment** — the moat | reputation, ratings, evidence count, `verification`, `last_verified` | same |
| **Demand** — uniquely ours | what people search for, what returned nothing | gap log |
| **Volatile** — cache, never the source of truth | phone, website, hours, address | cached, refreshed by harvest |

`verification` is one of `listed` (found in public data), `licensed` (confirmed against an
official registry), or `claimed` (the owner claimed it). Entries with no interactions say so
honestly — *"listed from public data, no ratings yet"* — rather than implying endorsement.

## Storage

- **`data/agents_snapshot.json`** — the human-readable, forkable, downloadable index. Source of truth.
- **`data/godena.db`** — SQLite with an FTS5 full-text index, built by `seeders/build_db.py` and
  committed. Used to *narrow candidates* before the Python ranking runs; the ranking itself is
  unchanged, so results are identical (verified: 10/10 benchmark queries).
- No external database. Nothing to pause, bill, or take offline.

### An honest note on speed

FTS5 finds candidates in **under a millisecond** versus ~40 ms for a full JSON scan. That matters
for **scale** — it is what makes millions of pointers viable without the scan growing linearly.

It does **not** make the live site feel faster today, and it was wrong to expect it to. Measured
against the deployed Space: `/health` — which does essentially no work — takes ~1040 ms, and
`/api/search` takes ~1075 ms. **The ~1.1 s is network round-trip plus free-tier platform
overhead, not compute.** Search compute is roughly 34 ms of it. Cutting compute to 1 ms is
correct engineering for growth, but the user-visible latency lives somewhere else entirely, and
would only be fixed by hosting closer to users or on a warmer tier.

## Refreshing

`seeders/harvest_osm.py` captures `osm_id`, `lat/lon` and `last_verified` on every entry, and
`_common.merge()` **upserts** those pointers onto existing rows rather than skipping duplicates —
so every re-harvest re-verifies instead of no-opping.

`.github/workflows/curate.yml` runs this weekly with no API key and no model: harvest → rebuild
static pages, sitemap and SQLite → integrity-check → commit. It refuses to commit an index that
shrank, has duplicate slugs, or contains an entry with no contact.

## Ground rules

- **Never invent a contact.** A wrong number is worse than no answer.
- **Never invent evidence.** Ratings and `licensed` status must come from a real source.
- **Prefer published business lines to personal mobiles.** Godena indexes businesses, not people.
- **Pointers over facts.** Facts rot; pointers let you refresh them forever.
- Wrong or unwanted listing? Open an issue — takedown requests are honoured.
