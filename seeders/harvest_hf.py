"""Harvest real AI agents/tools from the Hugging Face Hub (keyless public API).
Top Spaces by likes -> agents with real https://huggingface.co/spaces/... URLs.
Run: python seeders/harvest_hf.py [limit]"""
import json, sys, urllib.request
from _common import slugify, merge

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "godena-harvester"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

SKILL_HINTS = {
    "image": "design", "diffusion": "design", "art": "design", "logo": "design",
    "video": "media_production", "audio": "media_production", "music": "media_production",
    "voice": "media_production", "speech": "media_production", "tts": "media_production",
    "translate": "translation", "translation": "translation",
    "chat": "coding", "agent": "coding", "code": "coding", "llm": "coding",
    "research": "coding", "search": "coding", "rag": "coding",
}

def skill_for(text):
    t = (text or "").lower()
    for k, v in SKILL_HINTS.items():
        if k in t:
            return v
    return "coding"

def harvest(limit=400):
    out = []
    data = fetch(f"https://huggingface.co/api/spaces?sort=likes&direction=-1&limit={limit}")
    for s in data:
        sid = s.get("id") or ""
        if "/" not in sid:
            continue
        author, sp = sid.split("/", 1)
        likes = int(s.get("likes") or 0)
        if likes < 5:
            continue
        name = sp.replace("-", " ").replace("_", " ").strip().title().replace(" ", "_")[:60]
        tags = [str(t).lower() for t in (s.get("tags") or [])][:6]
        out.append({
            "name": name,
            "slug": slugify(sid),
            "skill_primary": skill_for(sp + " " + " ".join(tags)),
            "skill_tags": ["ai", "huggingface", "tool"] + [w for w in sp.lower().replace("-", " ").replace("_", " ").split() if len(w) > 2][:4] + tags[:2],
            "website": f"https://huggingface.co/spaces/{sid}",
            "source": "huggingface_v3",
            "reputation_score": min(6 + likes // 50, 12),
        })
    return out

if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    cands = harvest(lim)
    added, total = merge(cands)
    print(f"HF: {len(cands)} candidates, {added} added, snapshot now {total}")
