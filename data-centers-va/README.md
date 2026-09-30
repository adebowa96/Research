# Data centers, air pollution and mental health in Virginia

Data download for the census-tract study described in the research proposal.

## Get the data

```
python3 scripts/download_data.py            # all automatic sources
python3 scripts/download_data.py places acs # only some
```

Python 3.8+, standard library only. Files land in `data/raw/`, which is not committed.
A failed source is reported and the others still run; re-run just the failed ones.

## Sources

| Key | Dataset | Role | Notes |
|---|---|---|---|
| `places` | [CDC PLACES](https://www.cdc.gov/places/), census tract release (`cwsq-ngmh`), Virginia | Outcome | Depression (`DEPRESSION`), frequent mental distress (`MHLTH`), plus covariates |
| `deq` | [Virginia DEQ issued air permits for data centers](https://www.deq.virginia.gov/news-info/shortcuts/permits/air/issued-air-permits-for-data-centers) | Exposure | Saves the page and every linked permit PDF; generator counts and capacity are inside the PDFs |
| `osm` | OpenStreetMap data center features in Virginia (Overpass API) | Exposure | Locations to cross-check against DEQ permits |
| `aqs` | [EPA AQS](https://aqs.epa.gov/aqsweb/airdata/download_files.html) annual concentration by monitor, 2015–2024 | Air pollution | National files; filter to State Code 51, parameters 88101 (PM2.5) and 42602 (NO2) |
| `acs` | Census ACS 5-year 2023, tract level | Confounders | Income, poverty, race/ethnicity, education, age |
| `svi` | [CDC/ATSDR Social Vulnerability Index 2022](https://www.atsdr.cdc.gov/placeandhealth/svi/data_documentation_download.html) | Equity | Includes uninsured and limited-English shares |
| `tiger` | Census TIGER/Line 2023 tract boundaries and roads | Geography | Tract polygons; primary/secondary roads for traffic proximity |

## Manual downloads

- **Satellite PM2.5**: Washington University [ACAG surface PM2.5](https://sites.wustl.edu/acag/datasets/surface-pm2-5/) (large NetCDF files).
- **Satellite NO2**: TROPOMI via [NASA GES DISC](https://disc.gsfc.nasa.gov/) (free Earthdata login).
- **PEC map layers**: ask the [Piedmont Environmental Council](https://www.pecva.org/uncategorized/data-centers-diesel-generators-and-air-quality-pec-web-map/) for the data behind their generator map.
- **Hospital / ED data** (longitudinal outcome): data use agreement via [Virginia Health Information](https://www.vhi.org/).

## Caveats

- URLs and dataset IDs have not been test-run yet (the build environment could not reach these hosts). If one fails, check the link on the agency page above; agencies occasionally move files.
- PLACES values are model-based estimates, suited to cross-sectional analysis only.
