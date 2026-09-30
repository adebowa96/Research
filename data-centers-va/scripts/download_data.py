#!/usr/bin/env python3
"""Download the public datasets for the Virginia data centers / air pollution /
mental health study into data/raw/.

Standard library only. Run from the data-centers-va folder:

    python3 scripts/download_data.py            # everything
    python3 scripts/download_data.py places acs # just some sources

Each source is independent: a failure is reported and the rest still run.
Sources that need a login or are very large are listed at the end as manual steps.
"""

import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
VA_FIPS = "51"
USER_AGENT = "Mozilla/5.0 (research data download; data-centers-va)"


def fetch(url, dest, data=None, retries=3):
    """Download url to dest, retrying with backoff. Returns the path."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=300) as resp, open(dest, "wb") as out:
                while chunk := resp.read(1 << 20):
                    out.write(chunk)
            print(f"  saved {dest.relative_to(ROOT)} ({dest.stat().st_size / 1e6:.1f} MB)")
            return dest
        except Exception as exc:  # network errors, HTTP errors
            if attempt == retries:
                raise
            wait = 2 ** attempt
            print(f"  attempt {attempt} failed ({exc}); retrying in {wait}s")
            time.sleep(wait)


# --- Outcomes -----------------------------------------------------------------

def places():
    """CDC PLACES census-tract estimates for Virginia (depression, mental distress, and
    a few covariates/negative controls). Dataset cwsq-ngmh = latest tract release."""
    measures = ["DEPRESSION", "MHLTH", "CASTHMA", "COPD", "CSMOKING", "ACCESS2", "LPA", "OBESITY"]
    where = f"stateabbr='VA' AND measureid in({','.join(repr(m) for m in measures)})"
    query = urllib.parse.urlencode({"$where": where, "$limit": 500000})
    fetch(f"https://data.cdc.gov/resource/cwsq-ngmh.csv?{query}", RAW / "places" / "places_tract_va.csv")


# --- Exposure -----------------------------------------------------------------

def deq_permits():
    """Virginia DEQ list of issued data center air permits: saves the page and every
    linked permit document (PDFs hold generator counts and capacity)."""
    page_url = "https://www.deq.virginia.gov/news-info/shortcuts/permits/air/issued-air-permits-for-data-centers"
    page = fetch(page_url, RAW / "deq" / "issued_air_permits_for_data_centers.html")
    html = page.read_text(errors="ignore")
    links = sorted(set(re.findall(r'href="([^"]*(?:showpublisheddocument|\.pdf)[^"]*)"', html, re.I)))
    index = []
    for i, href in enumerate(links, 1):
        url = urllib.parse.urljoin(page_url, href)
        dest = RAW / "deq" / "permits" / f"permit_{i:03d}.pdf"
        try:
            fetch(url, dest)
            index.append({"file": dest.name, "url": url})
        except Exception as exc:
            print(f"  skipped {url}: {exc}")
        time.sleep(0.5)  # be polite to the DEQ server
    (RAW / "deq" / "permits_index.json").write_text(json.dumps(index, indent=2))
    print(f"  {len(index)} of {len(links)} permit documents downloaded")


def osm_datacenters():
    """Data center buildings and sites in Virginia tagged in OpenStreetMap."""
    query = """
    [out:json][timeout:180];
    area["ISO3166-2"="US-VA"]->.va;
    (
      nwr["telecom"="data_center"](area.va);
      nwr["building"="data_center"](area.va);
      nwr["industrial"="data_center"](area.va);
    );
    out center tags;
    """
    body = urllib.parse.urlencode({"data": query}).encode()
    fetch("https://overpass-api.de/api/interpreter", RAW / "osm" / "osm_datacenters_va.json", data=body)


# --- Air pollution ------------------------------------------------------------

def aqs(years=range(2015, 2025)):
    """EPA AQS annual concentration by monitor (national files; filter to State Code 51
    and parameters 88101 PM2.5 / 42602 NO2 during analysis)."""
    for year in years:
        fetch(f"https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_{year}.zip",
              RAW / "aqs" / f"annual_conc_by_monitor_{year}.zip")


# --- Confounders and equity ---------------------------------------------------

ACS_VARS = {
    "B01003_001E": "total_pop",
    "B01002_001E": "median_age",
    "B19013_001E": "median_hh_income",
    "B17001_001E": "poverty_universe",
    "B17001_002E": "below_poverty",
    "B03002_001E": "race_universe",
    "B03002_003E": "nh_white",
    "B03002_004E": "nh_black",
    "B03002_006E": "nh_asian",
    "B03002_012E": "hispanic",
    "B15003_001E": "edu_universe_25plus",
    "B15003_022E": "edu_bachelors",
    "B15003_023E": "edu_masters",
    "B15003_024E": "edu_professional",
    "B15003_025E": "edu_doctorate",
}


def acs(year=2023):
    """ACS 5-year tract estimates for Virginia via the Census API (no key needed)."""
    query = urllib.parse.urlencode({"get": "NAME," + ",".join(ACS_VARS), "for": "tract:*", "in": f"state:{VA_FIPS}"})
    raw = fetch(f"https://api.census.gov/data/{year}/acs/acs5?{query}", RAW / "acs" / f"acs5_{year}_tract_va.json")
    rows = json.loads(raw.read_text())
    header = [ACS_VARS.get(col, col) for col in rows[0]]
    out = RAW / "acs" / f"acs5_{year}_tract_va.csv"
    with open(out, "w") as f:
        f.write(",".join(header) + "\n")
        for row in rows[1:]:
            f.write(",".join(f'"{v}"' if v and "," in v else (v or "") for v in row) + "\n")
    print(f"  wrote {out.relative_to(ROOT)} ({len(rows) - 1} tracts)")


def svi():
    """CDC/ATSDR Social Vulnerability Index 2022, Virginia tracts."""
    fetch("https://svi.cdc.gov/Documents/Data/2022/csv/states/Virginia.csv", RAW / "svi" / "svi_2022_va.csv")


# --- Geography ----------------------------------------------------------------

def tiger(year=2023):
    """Census tract boundaries for Virginia and US primary roads (for traffic proximity)."""
    base = f"https://www2.census.gov/geo/tiger/TIGER{year}"
    fetch(f"{base}/TRACT/tl_{year}_{VA_FIPS}_tract.zip", RAW / "tiger" / f"tl_{year}_{VA_FIPS}_tract.zip")
    fetch(f"{base}/PRIMARYROADS/tl_{year}_us_primaryroads.zip", RAW / "tiger" / f"tl_{year}_us_primaryroads.zip")
    fetch(f"{base}/PRISECROADS/tl_{year}_{VA_FIPS}_prisecroads.zip", RAW / "tiger" / f"tl_{year}_{VA_FIPS}_prisecroads.zip")


SOURCES = {
    "places": places,
    "deq": deq_permits,
    "osm": osm_datacenters,
    "aqs": aqs,
    "acs": acs,
    "svi": svi,
    "tiger": tiger,
}

MANUAL = """
Manual steps (login required or very large files):
  - Satellite PM2.5 (annual, ~1 km): Washington University ACAG, V6.GL North America
    https://sites.wustl.edu/acag/datasets/surface-pm2-5/
  - Satellite NO2 (TROPOMI): NASA Earthdata login required
    https://disc.gsfc.nasa.gov/datasets?keywords=TROPOMI%20NO2
  - PEC data center / generator map layers: email the Piedmont Environmental Council
    https://www.pecva.org/uncategorized/data-centers-diesel-generators-and-air-quality-pec-web-map/
  - Virginia hospital discharge / ED data (longitudinal outcome): data use agreement via
    Virginia Health Information (https://www.vhi.org/)
"""


def main(argv):
    wanted = argv or list(SOURCES)
    unknown = [w for w in wanted if w not in SOURCES]
    if unknown:
        sys.exit(f"unknown source(s): {', '.join(unknown)}; choose from {', '.join(SOURCES)}")
    failed = []
    for name in wanted:
        print(f"[{name}] {SOURCES[name].__doc__.strip().splitlines()[0]}")
        try:
            SOURCES[name]()
        except Exception as exc:
            print(f"  FAILED: {exc}")
            failed.append(name)
    print(MANUAL)
    if failed:
        print(f"Failed sources: {', '.join(failed)} (re-run with: python3 scripts/download_data.py {' '.join(failed)})")
        sys.exit(1)
    print("All automatic sources downloaded.")


if __name__ == "__main__":
    main(sys.argv[1:])
