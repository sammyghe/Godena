"""Build a read-only SQLite FTS5 index from the snapshot.

Why: scanning a JSON array is O(n) per query and caps out around 10k entries.
SQLite FTS5 does full-text search over millions of rows in milliseconds, ships
as ONE file committed to the repo (still git-native, no server, no cost), and
reads from disk instead of loading everything into RAM.

This is what makes the pointer architecture scale: millions of pointers is
cheap, and the judgment layer travels with them.

Run: python seeders/build_db.py
"""
import json
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "data", "agents_snapshot.json")
DB = os.path.join(ROOT, "data", "godena.db")

COLS = [
    "slug", "name", "entity_type", "skill_primary", "location", "country",
    "website", "phone", "whatsapp", "contact_link", "source", "osm_id",
    "lat", "lon", "verification", "last_verified",
    "reputation_score", "interactions_count", "avg_rating", "tier",
]


def build():
    with open(SNAP, encoding="utf-8") as f:
        rows = json.load(f)

    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(f"""
        CREATE TABLE agents (
            id INTEGER PRIMARY KEY,
            {', '.join(c + ' TEXT' for c in COLS)},
            skill_tags TEXT
        )""")
    # FTS over the text people actually type: name, category, tags, place.
    cur.execute("""
        CREATE VIRTUAL TABLE agents_fts USING fts5(
            name, skill_primary, skill_tags, location, country,
            content='agents', content_rowid='id', tokenize='porter unicode61'
        )""")

    payload = []
    for i, a in enumerate(rows, 1):
        vals = []
        for c in COLS:
            v = a.get(c)
            vals.append(None if v is None else str(v))
        tags = " ".join(str(t) for t in (a.get("skill_tags") or []))
        payload.append((i, *vals, tags))

    cur.executemany(
        f"INSERT INTO agents (id, {', '.join(COLS)}, skill_tags) "
        f"VALUES ({', '.join('?' * (len(COLS) + 2))})",
        payload,
    )
    cur.execute("""
        INSERT INTO agents_fts(rowid, name, skill_primary, skill_tags, location, country)
        SELECT id, COALESCE(name,''), COALESCE(skill_primary,''), COALESCE(skill_tags,''),
               COALESCE(location,''), COALESCE(country,'') FROM agents""")

    # Indexes for the non-FTS filters the ranker uses
    for col in ("entity_type", "skill_primary", "country", "location", "slug"):
        cur.execute(f"CREATE INDEX idx_{col} ON agents({col})")

    con.commit()
    cur.execute("VACUUM")
    con.commit()
    con.close()

    size = os.path.getsize(DB) / 1e6
    print(f"built {DB}")
    print(f"  {len(rows)} rows · {size:.1f} MB")

    # sanity: FTS actually returns something sensible
    con = sqlite3.connect(DB)
    q = con.execute("""
        SELECT a.name, a.location, a.entity_type FROM agents_fts f
        JOIN agents a ON a.id = f.rowid
        WHERE agents_fts MATCH ? LIMIT 3""", ("pharmacy AND nairobi",)).fetchall()
    print("  smoke test 'pharmacy AND nairobi':", [r[0] for r in q] or "NO RESULTS")
    con.close()


if __name__ == "__main__":
    build()
