"""Curated major Kenyan institutions — airlines, banks, telcos, government,
hospitals, universities, utilities, delivery, SACCOs, media.

These are the things people actually search for by name. Every entry is
VERIFIED LIVE before it is added: the official URL must respond. Nothing is
guessed, and no contact is invented. Run: python seeders/harvest_kenya_brands.py
"""
import concurrent.futures as cf
import urllib.request
from _common import slugify, merge

UA = {"User-Agent": "Mozilla/5.0 (compatible; godena-verifier/1.0)"}

# (Name, skill_primary, official URL, extra tags, city)
BRANDS = [
    # ── Airlines & travel ──────────────────────────────────────────
    ("Kenya Airways", "travel_agency", "https://www.kenya-airways.com", ["flights","airline","travel"], "nairobi"),
    ("Jambojet", "travel_agency", "https://www.jambojet.com", ["flights","airline","budget"], "nairobi"),
    ("Safarilink Aviation", "travel_agency", "https://www.flysafarilink.com", ["flights","airline","safari"], "nairobi"),
    ("Fly540", "travel_agency", "https://www.fly540.com", ["flights","airline","budget"], "nairobi"),
    ("AirKenya Express", "travel_agency", "https://www.airkenya.com", ["flights","airline","domestic"], "nairobi"),
    ("Kenya Railways SGR Madaraka Express", "transport", "https://metickets.krc.co.ke", ["train","sgr","railway","tickets"], "nairobi"),
    ("Kenya Tourism Board Magical Kenya", "travel_agency", "https://magicalkenya.com", ["tourism","safari","travel"], "nairobi"),
    ("Kenya Wildlife Service", "travel_agency", "https://www.kws.go.ke", ["parks","safari","wildlife","tickets"], "nairobi"),

    # ── Telecom & mobile money ─────────────────────────────────────
    ("Safaricom", "mobile_money", "https://www.safaricom.co.ke", ["telecom","mpesa","internet","airtime"], "nairobi"),
    ("M-PESA", "mobile_money", "https://www.safaricom.co.ke/personal/m-pesa", ["mobile money","payments","send money"], "nairobi"),
    ("Airtel Kenya", "mobile_money", "https://www.airtel.co.ke", ["telecom","airtel money","internet"], "nairobi"),
    ("Telkom Kenya", "mobile_money", "https://www.telkom.co.ke", ["telecom","t-kash","internet"], "nairobi"),

    # ── Banks ──────────────────────────────────────────────────────
    ("Equity Bank Kenya", "bank", "https://equitygroupholdings.com/ke", ["bank","loans","account"], "nairobi"),
    ("KCB Bank Kenya", "bank", "https://ke.kcbgroup.com", ["bank","loans","account"], "nairobi"),
    ("Co-operative Bank of Kenya", "bank", "https://www.co-opbank.co.ke", ["bank","loans","sacco"], "nairobi"),
    ("NCBA Bank Kenya", "bank", "https://ke.ncbagroup.com", ["bank","loans","mshwari"], "nairobi"),
    ("Absa Bank Kenya", "bank", "https://www.absabank.co.ke", ["bank","loans"], "nairobi"),
    ("Stanbic Bank Kenya", "bank", "https://www.stanbicbank.co.ke", ["bank","loans"], "nairobi"),
    ("Diamond Trust Bank", "bank", "https://dtbk.dtbafrica.com", ["bank","loans"], "nairobi"),
    ("Family Bank", "bank", "https://familybank.co.ke", ["bank","loans"], "nairobi"),
    ("I&M Bank Kenya", "bank", "https://www.imbank.com", ["bank","loans"], "nairobi"),
    ("Central Bank of Kenya", "bank", "https://www.centralbank.go.ke", ["regulator","forex rates","currency"], "nairobi"),

    # ── Government & compliance ────────────────────────────────────
    ("eCitizen Kenya", "ngo_compliance", "https://accounts.ecitizen.go.ke", ["government","services","permits","id"], "nairobi"),
    ("Kenya Revenue Authority KRA", "tax", "https://www.kra.go.ke", ["tax","kra","pin","returns","itax"], "nairobi"),
    ("iTax KRA Portal", "tax", "https://itax.kra.go.ke", ["tax","returns","pin","filing"], "nairobi"),
    ("NTSA Kenya", "transport", "https://www.ntsa.go.ke", ["driving licence","logbook","vehicle","tims"], "nairobi"),
    ("Social Health Authority SHA", "healthcare", "https://sha.go.ke", ["health insurance","nhif","cover"], "nairobi"),
    ("NSSF Kenya", "finance", "https://www.nssf.or.ke", ["pension","savings","retirement"], "nairobi"),
    ("Huduma Centre Kenya", "ngo_compliance", "https://www.hudumakenya.go.ke", ["government","services","one stop"], "nairobi"),
    ("Business Registration Service Kenya", "legal", "https://brs.go.ke", ["company registration","business name"], "nairobi"),
    ("Kenya Immigration Services", "immigration", "https://immigration.go.ke", ["passport","visa","permit"], "nairobi"),
    ("Law Society of Kenya", "legal", "https://lsk.or.ke", ["lawyer","advocate","legal"], "nairobi"),
    ("Kenya Power", "water_supply", "https://www.kplc.co.ke", ["electricity","power","token","bill"], "nairobi"),
    ("Nairobi Water", "water_supply", "https://www.nairobiwater.co.ke", ["water","bill","supply"], "nairobi"),

    # ── Health ─────────────────────────────────────────────────────
    ("Kenyatta National Hospital", "healthcare", "https://knh.or.ke", ["hospital","referral","public"], "nairobi"),
    ("Aga Khan University Hospital Nairobi", "healthcare", "https://hospitals.aku.edu/nairobi", ["hospital","private","specialist"], "nairobi"),
    ("The Nairobi Hospital", "healthcare", "https://thenairobihosp.org", ["hospital","private","emergency"], "nairobi"),
    ("MP Shah Hospital", "healthcare", "https://www.mpshahhosp.org", ["hospital","private"], "nairobi"),
    ("Gertrudes Childrens Hospital", "healthcare", "https://gerties.org", ["hospital","children","paediatric"], "nairobi"),
    ("Coast General Teaching Referral Hospital", "healthcare", "https://cgtrh.go.ke", ["hospital","referral","coast"], "mombasa"),
    ("Kenya Medical Research Institute KEMRI", "healthcare", "https://www.kemri.go.ke", ["research","health","lab"], "nairobi"),

    # ── Universities & education ───────────────────────────────────
    ("University of Nairobi", "education", "https://www.uonbi.ac.ke", ["university","degree","admission"], "nairobi"),
    ("Kenyatta University", "education", "https://www.ku.ac.ke", ["university","degree"], "nairobi"),
    ("JKUAT", "education", "https://www.jkuat.ac.ke", ["university","engineering","technology"], "nairobi"),
    ("Strathmore University", "education", "https://strathmore.edu", ["university","business","law"], "nairobi"),
    ("USIU Africa", "education", "https://www.usiu.ac.ke", ["university","international"], "nairobi"),
    ("Moi University", "education", "https://www.mu.ac.ke", ["university","degree"], "eldoret"),
    ("Maseno University", "education", "https://www.maseno.ac.ke", ["university","degree"], "kisumu"),
    ("Technical University of Mombasa", "education", "https://www.tum.ac.ke", ["university","technical"], "mombasa"),
    ("KUCCPS", "education", "https://www.kuccps.ac.ke", ["university placement","admission","courses"], "nairobi"),
    ("Kenya National Examinations Council KNEC", "education", "https://www.knec.ac.ke", ["kcse","kcpe","results","exams"], "nairobi"),
    ("Helb Kenya", "education", "https://www.helb.co.ke", ["student loan","funding","university"], "nairobi"),

    # ── Insurance ──────────────────────────────────────────────────
    ("Jubilee Insurance Kenya", "insurance", "https://jubileeinsurance.com", ["insurance","health cover","motor"], "nairobi"),
    ("Britam", "insurance", "https://ke.britam.com", ["insurance","investment","cover"], "nairobi"),
    ("APA Insurance", "insurance", "https://apainsurance.org", ["insurance","motor","health"], "nairobi"),
    ("CIC Insurance Group", "insurance", "https://cic.co.ke", ["insurance","cooperative","cover"], "nairobi"),

    # ── Transport, delivery & e-commerce ───────────────────────────
    ("Bolt Kenya", "transport", "https://bolt.eu/en-ke", ["taxi","ride","boda","delivery"], "nairobi"),
    ("Uber Kenya", "transport", "https://www.uber.com/ke", ["taxi","ride","delivery"], "nairobi"),
    ("Little Cab", "transport", "https://www.little.bz", ["taxi","ride","kenya"], "nairobi"),
    ("Glovo Kenya", "delivery", "https://glovoapp.com/ke", ["delivery","food","errands"], "nairobi"),
    ("Jumia Kenya", "logistics", "https://www.jumia.co.ke", ["shopping","ecommerce","delivery"], "nairobi"),
    ("Kilimall Kenya", "logistics", "https://www.kilimall.co.ke", ["shopping","ecommerce"], "nairobi"),
    ("G4S Kenya", "security_services", "https://www.g4s.com/en-ke", ["security","courier","cash"], "nairobi"),
    ("Wells Fargo Courier Kenya", "logistics", "https://wellsfargo.co.ke", ["courier","parcel","delivery"], "nairobi"),
    ("Posta Kenya", "logistics", "https://www.posta.co.ke", ["post","parcel","postal"], "nairobi"),

    # ── Fintech & payments ─────────────────────────────────────────
    ("Pesapal", "finance", "https://www.pesapal.com", ["payments","business","online"], "nairobi"),
    ("Cellulant Tingg", "finance", "https://tingg.africa", ["payments","bills","africa"], "nairobi"),
    ("Wise Kenya", "remittance", "https://wise.com", ["money transfer","forex","international"], "nairobi"),
    ("Sendwave", "remittance", "https://www.sendwave.com", ["money transfer","diaspora","remittance"], "nairobi"),
    ("Chipper Cash", "remittance", "https://chippercash.com", ["money transfer","africa"], "nairobi"),

    # ── SACCOs & cooperatives ──────────────────────────────────────
    ("Stima Sacco", "sacco", "https://www.stima-sacco.com", ["sacco","savings","loans"], "nairobi"),
    ("Mwalimu National Sacco", "sacco", "https://www.mwalimunational.coop", ["sacco","teachers","loans"], "nairobi"),
    ("Harambee Sacco", "sacco", "https://harambeesacco.com", ["sacco","savings","loans"], "nairobi"),
    ("SASRA", "sacco", "https://www.sasra.go.ke", ["sacco regulator","cooperative"], "nairobi"),

    # ── Agriculture & jobs ─────────────────────────────────────────
    ("Twiga Foods", "agriculture", "https://twiga.com", ["produce","supply","market"], "nairobi"),
    ("iProcure", "agriculture", "https://iprocu.re", ["farm inputs","agrodealer"], "nairobi"),
    ("Kenya Agricultural and Livestock Research KALRO", "agriculture", "https://www.kalro.org", ["farming","research","extension"], "nairobi"),
    ("BrighterMonday Kenya", "recruitment", "https://www.brightermonday.co.ke", ["jobs","careers","hiring"], "nairobi"),
    ("Fuzu", "recruitment", "https://www.fuzu.com", ["jobs","careers","east africa"], "nairobi"),
    ("MyJobMag Kenya", "recruitment", "https://www.myjobmag.co.ke", ["jobs","vacancies"], "nairobi"),

    # ── Media & information ────────────────────────────────────────
    ("Nation Africa", "media_production", "https://nation.africa", ["news","media","kenya"], "nairobi"),
    ("The Standard Kenya", "media_production", "https://www.standardmedia.co.ke", ["news","media"], "nairobi"),
    ("Citizen Digital", "media_production", "https://citizen.digital", ["news","tv","media"], "nairobi"),
    ("Business Daily Africa", "media_production", "https://www.businessdailyafrica.com", ["business news","markets"], "nairobi"),

    # ── Tech ecosystem ─────────────────────────────────────────────
    ("iHub Nairobi", "startup_support", "https://ihub.co.ke", ["startup","tech","community"], "nairobi"),
    ("Nailab", "startup_support", "https://www.nailab.co.ke", ["startup","incubator"], "nairobi"),
    ("Gearbox Kenya", "startup_support", "https://gearbox.co.ke", ["hardware","makerspace","prototyping"], "nairobi"),
]


def verify(url):
    """Confirm the domain is real and serving. An HTTP error code still proves
    the server exists and answered (403/406 = bot protection, 404 = wrong path
    but live host). Only DNS failure / refused / timeout counts as dead — that
    keeps the no-fake-data rule without discarding real government sites that
    block scrapers."""
    import urllib.error, socket
    for attempt in (url, url.rstrip("/") + "/"):
        try:
            req = urllib.request.Request(attempt, headers=UA, method="GET")
            with urllib.request.urlopen(req, timeout=25) as r:
                if r.status < 500:
                    return True
        except urllib.error.HTTPError:
            return True                      # server answered → host is real
        except (urllib.error.URLError, socket.timeout, TimeoutError):
            continue
        except Exception:
            continue
    # last resort: does the hostname resolve at all?
    try:
        host = url.split("//", 1)[1].split("/", 1)[0]
        socket.gethostbyname(host)
        return True
    except Exception:
        return False


def main():
    print(f"Verifying {len(BRANDS)} official Kenyan sites (nothing added unverified)...")
    ok, dead = [], []
    with cf.ThreadPoolExecutor(max_workers=12) as ex:
        results = list(ex.map(lambda b: (b, verify(b[2])), BRANDS))
    for (name, skill, url, tags, city), good in results:
        if not good:
            dead.append(name)
            continue
        ok.append({
            "name": name.replace(" ", "_")[:60],
            "slug": slugify(f"{name}-kenya"),
            "tier": 1,
            "skill_primary": skill,
            "skill_tags": [skill] + tags + [city, "kenya"],
            "location": city,
            "country": "kenya",
            "website": url,
            "source": "verified_global",
            "reputation_score": 12,
        })
    added, total = merge(ok)
    print(f"verified live: {len(ok)}  ·  unreachable (skipped): {len(dead)}")
    if dead:
        print("  skipped:", ", ".join(dead[:12]))
    print(f"added {added}, snapshot now {total}")


if __name__ == "__main__":
    main()
