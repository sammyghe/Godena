"""Shared helpers for Godena harvesters. No fakes: every agent must carry a
real, verifiable URL. Idempotent by slug. Snapshot is capped for the free Space."""
import json, os, re

SNAP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "agents_snapshot.json")
CAP = 12000  # max entries in the git-native index (a few MB; loads in memory, fast)

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:80] or "agent"

def load():
    with open(SNAP, encoding="utf-8") as f:
        return json.load(f)

def save(snap):
    json.dump(snap, open(SNAP, "w", encoding="utf-8"), indent=0)

# Fields that are POINTERS or freshness stamps — always refreshed on re-harvest.
# Facts (phone/website/hours) may change too, but pointers are what let us
# re-resolve later, so they must never be lost on a duplicate.
POINTER_FIELDS = ("osm_id", "lat", "lon", "last_verified", "verification")


def merge(new, snap=None):
    """Add candidates (each a dict with a real website) deduped by slug, up to CAP."""
    if snap is None:
        snap = load()
    by_slug = {a.get("slug"): a for a in snap}
    have = set(by_slug)
    added = refreshed = 0
    for a in new:
        # Must have a slug and at least ONE real, verifiable contact.
        # A phone counts: most real African businesses have a number long
        # before a website. Never accept an entry with no way to reach it.
        has_contact = a.get("website") or a.get("phone") or a.get("whatsapp") or a.get("contact_link")
        if not a.get("slug") or not has_contact:
            continue
        if a["slug"] in have:
            # Re-harvest = refresh, not skip. Backfill pointers and the
            # freshness stamp onto entries that predate them.
            cur = by_slug[a["slug"]]
            touched = False
            for f in POINTER_FIELDS:
                if a.get(f) is not None and cur.get(f) != a.get(f):
                    cur[f] = a[f]
                    touched = True
            refreshed += touched
            continue
        if len(snap) >= CAP:
            break
        a.setdefault("tier", 1)
        a.setdefault("location", "global")
        a.setdefault("country", "global")
        a.setdefault("skill_primary", "coding")
        a.setdefault("skill_tags", ["ai"])
        a.setdefault("reputation_score", 8)
        # service = a real business/person; agent = an AI tool/model
        a.setdefault("verification", "listed")   # listed | licensed | claimed
        a.setdefault("entity_type",
                     "service" if a.get("source") in
                     {"osm_scraped", "verified_global", "claimed"} else "agent")
        snap.append(a)
        have.add(a["slug"])
        added += 1
    save(snap)
    if refreshed:
        print(f"  refreshed pointers on {refreshed} existing entries")
    # integrity
    slugs = [x["slug"] for x in snap]
    assert len(slugs) == len(set(slugs)), "duplicate slugs after merge"
    return added, len(snap)
