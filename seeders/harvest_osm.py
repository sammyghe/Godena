"""Harvest REAL human businesses/services from OpenStreetMap (free Overpass API).
Only imports entries that carry a real website tag -> no fabricated contacts.
This is the human-services side of the index. Run: python seeders/harvest_osm.py"""
import datetime, json, time, urllib.request, urllib.parse

TODAY = datetime.date.today().isoformat()
from _common import slugify, merge

OVERPASS = "https://overpass-api.de/api/interpreter"

# (city label, country, bbox south,west,north,east)
CITIES = [
    # Kenya first — the most active market, indexed city by city
    ("nairobi",      "kenya",        (-1.37, 36.72, -1.16, 36.95)),
    ("nairobi-west", "kenya",        (-1.34, 36.66, -1.22, 36.76)),
    ("mombasa",      "kenya",        (-4.10, 39.60, -3.95, 39.75)),
    ("kisumu",       "kenya",        (-0.13, 34.71, -0.05, 34.79)),
    ("nakuru",       "kenya",        (-0.32, 36.03, -0.25, 36.11)),
    ("eldoret",      "kenya",        (0.48, 35.24, 0.56, 35.32)),
    ("thika",        "kenya",        (-1.07, 37.05, -1.00, 37.12)),
    ("machakos",     "kenya",        (-1.55, 37.23, -1.48, 37.30)),
    ("nyeri",        "kenya",        (-0.45, 36.91, -0.38, 36.98)),
    # Rest of the region
    ("kampala",      "uganda",       (0.24, 32.50, 0.42, 32.68)),
    ("lagos",        "nigeria",      (6.40, 3.30, 6.65, 3.55)),
    ("kigali",       "rwanda",       (-1.99, 30.02, -1.90, 30.14)),
    ("addis",        "ethiopia",     (8.90, 38.68, 9.05, 38.85)),
    ("accra",        "ghana",        (5.52, -0.28, 5.66, -0.10)),
    ("dar",          "tanzania",     (-6.90, 39.20, -6.75, 39.32)),
    ("johannesburg", "southafrica",  (-26.28, 27.95, -26.10, 28.12)),
]
SLEEP = 12  # Overpass rate-limits hard; be patient between cities

SKILL = {
    # health
    "pharmacy": "healthcare", "hospital": "healthcare", "clinic": "healthcare",
    "doctors": "healthcare", "dentist": "healthcare", "veterinary": "veterinary",
    "laboratory": "healthcare", "optician": "healthcare",
    # money — mobile money and SACCOs matter enormously in Kenya
    "bank": "bank", "atm": "bank", "bureau_de_change": "finance",
    "money_transfer": "mobile_money", "money_lender": "finance",
    # food & hospitality
    "restaurant": "restaurant", "cafe": "restaurant", "fast_food": "restaurant",
    "bar": "restaurant", "bakery": "restaurant", "butcher": "restaurant",
    "hotel": "hotel_lodging", "guest_house": "hotel_lodging", "hostel": "hotel_lodging",
    # transport
    "fuel": "transport", "car_repair": "mechanic", "car_rental": "transport",
    "car_wash": "mechanic", "bus_station": "transport", "taxi": "transport",
    "driving_school": "education",
    # professional
    "lawyer": "legal", "accountant": "accounting", "estate_agent": "real_estate",
    "insurance": "insurance", "employment_agency": "recruitment",
    "travel_agent": "travel_agency", "it": "coding", "company": "startup_support",
    # education & public
    "school": "education", "university": "education", "college": "education",
    "kindergarten": "education", "library": "education",
    "police": "security_services", "post_office": "logistics",
    "courthouse": "legal", "townhall": "ngo_compliance",
    # trades & retail
    "hairdresser": "hair_beauty", "beauty": "hair_beauty", "laundry": "cleaning_services",
    "hardware": "construction", "electronics": "coding", "supermarket": "restaurant",
    "mobile_phone": "coding", "computer": "coding", "tailor": "design",
    "photo": "photography", "copyshop": "digital_printing", "printer": "digital_printing",
}

def q(bbox):
    s, w, n, e = bbox
    b = f"({s},{w},{n},{e})"
    # Accept a website OR a phone — in Kenya most real businesses have a
    # phone long before they have a site, and a phone is a real contact.
    return f"""[out:json][timeout:90];
(
  nwr["amenity"]["name"]["website"]{b};
  nwr["amenity"]["name"]["phone"]{b};
  nwr["amenity"]["name"]["contact:phone"]{b};
  nwr["shop"]["name"]["website"]{b};
  nwr["shop"]["name"]["phone"]{b};
  nwr["office"]["name"]["website"]{b};
  nwr["office"]["name"]["phone"]{b};
  nwr["tourism"~"hotel|guest_house|hostel"]["name"]{b};
  nwr["healthcare"]["name"]{b};
);
out center 400;"""

MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.osm.jp/api/interpreter",
]

def fetch(ql, tries=3):
    """Overpass 429s and 504s constantly. Rotate mirrors and back off."""
    last = None
    for attempt in range(tries):
        for mirror in MIRRORS:
            data = urllib.parse.urlencode({"data": ql}).encode()
            req = urllib.request.Request(mirror, data=data,
                                         headers={"User-Agent": "godena-harvester"})
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    return json.load(r)
            except Exception as e:
                last = e
                continue
        time.sleep(8 * (attempt + 1))
    raise last

def harvest():
    out = []
    for label, country, bbox in CITIES:
        try:
            data = fetch(q(bbox))
        except Exception as ex:
            print(f"  osm {label}: {ex}")
            time.sleep(5)
            continue
        for el in data.get("elements", []):
            t = el.get("tags", {})
            name = t.get("name")
            web   = (t.get("website") or t.get("contact:website") or "").strip()
            phone = (t.get("phone") or t.get("contact:phone") or t.get("contact:mobile") or "").strip()
            if not name or not (web.startswith("http") or phone):
                continue          # must have a REAL contact — never invent one
            cat = (t.get("amenity") or t.get("tourism") or t.get("office")
                   or t.get("shop") or t.get("healthcare") or "")
            skill = SKILL.get(cat, "")
            if not skill:
                continue
            # POINTER, not just facts. osm_id lets us re-resolve this entry
            # forever without re-scraping the whole city — and it means the
            # volatile fields (phone/hours) can be refreshed instead of rotting.
            osm_id = f"{el.get('type','node')}/{el.get('id')}" if el.get("id") else None
            entry = {
                "name": name.replace(" ", "_")[:60],
                "slug": slugify(f"{name}-{label}"),
                "skill_primary": skill,
                "skill_tags": [skill, cat, label, country],
                "location": label, "country": country,
                "source": "osm_scraped",
                "reputation_score": 9 if web else 8,
                "osm_id": osm_id,
                "last_verified": TODAY,
                "verification": "listed",   # listed | licensed | claimed
            }
            if el.get("lat") or (el.get("center") or {}).get("lat"):
                c = el.get("center") or el
                entry["lat"], entry["lon"] = c.get("lat"), c.get("lon")
            if web:
                entry["website"] = web
            if phone:
                entry["phone"] = phone
                digits = "".join(c for c in phone if c.isdigit())
                if len(digits) > 8:
                    entry["whatsapp"] = f"https://wa.me/{digits}"
            out.append(entry)
        print(f"  osm {label}: {len(out)} cumulative")
        time.sleep(SLEEP)
    return out

if __name__ == "__main__":
    cands = harvest()
    added, total = merge(cands)
    print(f"OSM: {len(cands)} real businesses, {added} added, snapshot now {total}")
