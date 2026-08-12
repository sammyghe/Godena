"""Pre-render a static page for every REAL service in the index.

Why: the sitemap advertises 1 URL for a 10,000-row index, so none of the data
is discoverable by Google or by AI crawlers. Each page carries JSON-LD
(LocalBusiness) so search engines and LLMs can read the entry directly.

Only `entity_type == "service"` is rendered — real businesses are the unique,
defensible data. The scraped AI tail is not worth indexing and would look like
spam to a crawler.

Run: python seeders/build_pages.py
"""
import html
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAP = os.path.join(ROOT, "data", "agents_snapshot.json")
OUT = os.path.join(ROOT, "docs", "a")
SITE = "https://sammyghe.github.io/Godena"

PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}/a/{slug}/">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}/a/{slug}/"><meta property="og:image" content="{site}/og.png">
<script type="application/ld+json">{jsonld}</script>
<style>
:root{{--bg:#0b0f14;--card:#121924;--line:#1f2b3a;--text:#e8eef5;--mut:#8fa3b8;--green:#25d366}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;line-height:1.6}}
.w{{max-width:680px;margin:0 auto;padding:28px 18px 70px}}
a{{color:var(--green);text-decoration:none}} .mut{{color:var(--mut)}}
h1{{font-size:1.7rem;margin:6px 0}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;margin:18px 0}}
.badge{{display:inline-block;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:4px 12px;font-size:.82rem;color:var(--mut);margin:3px 4px 3px 0}}
.cta{{display:inline-block;background:var(--green);color:#04210f;font-weight:700;padding:11px 18px;border-radius:12px;margin-top:8px}}
footer{{margin-top:40px;font-size:.85rem;color:var(--mut)}}
</style></head><body><div class="w">
<p class="mut"><a href="{site}/">← Godena</a></p>
<h1>{name}</h1>
<p class="mut">{kind}{where}</p>
<div>{tags}</div>
<div class="card">
{contact}
{unverified}
</div>
<p><a class="cta" href="{site}/?q={q}">Search Godena for more like this</a></p>
<footer>
Listed on <a href="{site}/">Godena</a> — an open index of real services and AI agents.
Free, open source, no commission. Is this listing wrong or yours?
<a href="https://github.com/sammyghe/Godena/issues">Tell us</a>.
</footer>
</div></body></html>
"""


def esc(s):
    return html.escape(str(s or ""), quote=True)


def build():
    with open(SNAP, encoding="utf-8") as f:
        data = json.load(f)
    services = [a for a in data if a.get("entity_type") == "service"]
    print(f"{len(data)} total · rendering {len(services)} real services")

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    urls = []
    for a in services:
        slug = a.get("slug")
        if not slug:
            continue
        name = (a.get("name") or slug).replace("_", " ").replace("-", " ").strip()
        city = (a.get("location") or "").title()
        country = (a.get("country") or "").title()
        where = f" · {city}, {country}" if city and country not in ("", "Global", "Unknown") else ""
        kind = (a.get("skill_primary") or "service").replace("_", " ").title()
        site_url = a.get("website") or ""
        phone = a.get("phone") or ""
        wa = a.get("whatsapp") or ""

        rows = []
        if site_url:
            rows.append(f'<p>🌐 <a href="{esc(site_url)}" rel="noopener nofollow">{esc(site_url[:70])}</a></p>')
        if phone:
            rows.append(f'<p>📞 <a href="tel:{esc(phone)}">{esc(phone)}</a></p>')
        if wa:
            rows.append(f'<p>💬 <a href="{esc(wa)}" rel="noopener nofollow">WhatsApp</a></p>')
        if not rows:
            rows.append('<p class="mut">No public contact on file.</p>')

        # Honest about evidence — no invented authority
        rated = int(a.get("interactions_count") or 0)
        unver = ('<p class="mut" style="margin-top:10px;font-size:.86rem">'
                 'Listed from public data · no ratings yet — unverified.</p>') if not rated else ""

        desc = f"{name} — {kind}{where}. Contact details and details on Godena."
        jsonld = json.dumps({
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": name,
            "url": f"{SITE}/a/{slug}/",
            **({"telephone": phone} if phone else {}),
            **({"sameAs": [site_url]} if site_url else {}),
            **({"address": {"@type": "PostalAddress", "addressLocality": city,
                            "addressCountry": country}} if city else {}),
        }, ensure_ascii=False)

        tags = "".join(
            f'<span class="badge">{esc(str(t).replace("_", " "))}</span>'
            for t in (a.get("skill_tags") or [])[:6] if t
        )

        page = PAGE.format(
            title=esc(f"{name} — {kind}{where} | Godena"),
            desc=esc(desc), site=SITE, slug=esc(slug), name=esc(name),
            kind=esc(kind), where=esc(where), tags=tags,
            contact="\n".join(rows), unverified=unver,
            jsonld=jsonld,
            q=esc((a.get("skill_primary") or "").replace("_", "+")),
        )
        d = os.path.join(OUT, slug)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        urls.append(f"{SITE}/a/{slug}/")

    # real sitemap (chunked — 50k URL limit per file, we stay well under)
    sm = os.path.join(ROOT, "docs", "sitemap.xml")
    with open(sm, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        f.write(f"  <url><loc>{SITE}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>\n")
        for u in urls:
            f.write(f"  <url><loc>{u}</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n")
        f.write("</urlset>\n")

    print(f"rendered {len(urls)} pages · sitemap now lists {len(urls)+1} URLs")


if __name__ == "__main__":
    build()
