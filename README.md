# AutoSEO-Lab

> A hands-on laboratory for **Technical SEO** and **GEO (Generative Engine Optimization)**,
> engineered with Python automation for B2B industrial domains.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-000000.svg)](https://peps.python.org/pep-0008/)
[![Scope](https://img.shields.io/badge/scope-B2B%20Industrial-orange.svg)]()
[![Status](https://img.shields.io/badge/status-active%20development-yellow.svg)]()

---

## Table of Contents

1. [Overview](#overview)
2. [Why AutoSEO-Lab](#why-autoseo-lab)
3. [System Architecture](#system-architecture)
4. [Project Structure](#project-structure)
5. [Getting Started](#getting-started)
6. [Module Reference](#module-reference)
7. [Usage](#usage)
8. [Security & Credential Hygiene](#security--credential-hygiene)
9. [Roadmap](#roadmap)
10. [License](#license)

---

## Overview

**AutoSEO-Lab** is a modular, open-source toolkit that fuses **Python automation** with
**Technical SEO** and the emerging discipline of **GEO (Generative Engine Optimization)**.
It is purpose-built for **B2B industrial engineering** verticals — domains such as
automotive leveling systems, hydraulic components, and industrial valves — where search
volume is low but purchase intent is exceptionally high.

The repository doubles as:

- **A production-grade SEO toolchain** — pull analytics, sanitize metadata, submit URLs for
  indexing across Google, Bing, Yandex, and Naver.
- **A continuous learning journal** — every script documents a real problem encountered in
  the field and the deterministic Python solution applied to it.

Rather than paying recurring SaaS subscriptions for generic dashboards, AutoSEO-Lab keeps
the entire SEO data pipeline **local, auditable, and scriptable**.

---

## Why AutoSEO-Lab

| Pain Point in B2B SEO | AutoSEO-Lab Response |
|---|---|
| Niche keywords with high intent but thin tooling coverage | Targeted GSC analytics slicing by query, page, country, and device |
| Slow indexation of refreshed product specification pages | Direct submission via Google Indexing API and IndexNow protocol |
| Raw, inconsistent `<title>` and metadata across legacy pages | Deterministic batch sanitization pipeline exporting clean CSV |
| Black-box SaaS reporting | Transparent, version-controlled Python scripts |
| Rise of AI answer engines (GEO) | Structured, machine-readable metadata exports optimized for retrieval |

> **Philosophy:** *Deterministic over magical.* Every transformation is reproducible,
> every export is diff-able, and every credential stays on disk.

---

## System Architecture

```
                ┌─────────────────────────────────────────────────────┐
                │                   RAW INPUT LAYER                    │
                │   Sitemap.xml   ·   URL lists   ·   Raw HTML chunks  │
                └──────────────────────────┬──────────────────────────┘
                                           │
                                           ▼
                ┌─────────────────────────────────────────────────────┐
                │                DATA CLEANSING LAYER                  │
                │  fetch_title_pro.py  →  batch_title_cleaner.py       │
                │           →  seo_metadata_exporter.py  (CSV out)     │
                └──────────────────────────┬──────────────────────────┘
                                           │
                           clean, structured SEO assets
                                           │
                                           ▼
                ┌─────────────────────────────────────────────────────┐
                │              CORE ORCHESTRATION LAYER                │
                │  core_gsc_orchestrator.py  (Search Console analytics)│
                └──────────────────────────┬──────────────────────────┘
                                           │
                                           ▼
                ┌─────────────────────────────────────────────────────┐
                │              INDEX DISTRIBUTION LAYER                │
                │  google_quick_index.py · batch_index.py · index_now  │
                └─────────────────────────────────────────────────────┘
```

Each layer is **independent and composable** — outputs of one stage become inputs of the
next, allowing partial pipeline execution or standalone module use.

---

## Project Structure

```
AutoSEO-Lab/
├── .github/
│   └── workflows/                # CI / automation hooks (reserved)
├── core/                         # Core orchestration & indexing console
│   ├── core_gsc_orchestrator.py  # Google Search Console analytics hub
│   ├── google_quick_index.py     # Google Indexing API client
│   ├── batch_index.py            # Sitemap-driven bulk index submission
│   ├── index_now.py              # IndexNow protocol client (Bing/Yandex/Naver)
│   ├── grant_permission.py       # GSC property permission provisioning
│   ├── verify_service_account.py # Service-account ownership verification
│   ├── sync_traffic.py           # Traffic synchronization helper
│   └── pipeline_to_file.py       # Pipeline → file persistence
├── utils/                        # Data cleansing & extraction toolkit
│   ├── fetch_title_pro.py        # Case-insensitive <title> extraction
│   ├── batch_title_cleaner.py    # Batch normalization pipeline
│   └── seo_metadata_exporter.py  # Metadata → structured CSV exporter
├── docs/                         # Markdown documentation site
│   ├── index.md                  # Landing page (bilingual)
│   ├── python-basics.md          # Python learning journal
│   └── b2b-spec-guide.md         # B2B industrial copywriting guide
├── README.md                     # This document
├── .gitignore                    # Credential & data lock (enforced)
└── LICENSE                       # MIT
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- A Google Cloud project with the following APIs **enabled**:
  - Google Search Console API
  - Google Indexing API
- A verified **Search Console property** for your target domain
- (Optional) An **IndexNow API key** from Bing Webmaster Tools

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/AutoSEO-Lab.git
cd AutoSEO-Lab

# 2. Create and activate an isolated virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows (cmd.exe)

# 3. Install dependencies
pip install google-auth google-auth-oauthlib google-auth-httplib2 \
            google-api-python-client oauth2client httplib2
```

### Credential Provisioning

Place the following files at the **project root**. They are strictly gitignored and must
never be committed.

| File | Purpose | Source |
|---|---|---|
| `credentials.json` | OAuth client / service-account key | Google Cloud Console → APIs & Services → Credentials |
| `service_account_key.json` | Indexing API service account | Google Cloud Console → IAM → Service Accounts |

```bash
# Quick sanity check — confirm credentials are present and ignored
ls credentials.json service_account_key.json
git check-ignore credentials.json   # must echo the filename
```

---

## Module Reference

### Core Orchestration

| Module | Responsibility | Status |
|---|---|---|
| `core/core_gsc_orchestrator.py` | Pull GSC performance data — clicks, impressions, CTR, average position — sliced by query, page, country, device, or date. CLI-driven with CSV export. | ![Active](https://img.shields.io/badge/status-active%20dev-yellow.svg) |
| `core/google_quick_index.py` | Submit single or batched URLs to the Google Indexing API (`URL_UPDATED` / `URL_DELETED`). | ![Active](https://img.shields.io/badge/status-active%20dev-yellow.svg) |
| `core/batch_index.py` | Parse a remote `sitemap.xml` and bulk-push every URL to the Indexing API via `oauth2client`. | ![Stable](https://img.shields.io/badge/status-stable-brightgreen.svg) |
| `core/index_now.py` | Stateless IndexNow protocol client — submit URLs to Bing, Yandex, and Naver with no OAuth overhead. | ![Stable](https://img.shields.io/badge/status-stable-brightgreen.svg) |

### Data Cleansing

| Module | Responsibility | Status |
|---|---|---|
| `utils/fetch_title_pro.py` | Case-insensitive `<title>` extraction with whitespace normalization. Robust against `<TITLE>`, `<Title>`, and mixed-case tag variants. | ![Stable](https://img.shields.io/badge/status-stable-brightgreen.svg) |
| `utils/batch_title_cleaner.py` | Iterative batch sanitization pipeline over a list of raw HTML payloads, with per-record status reporting. | ![Stable](https://img.shields.io/badge/status-stable-brightgreen.svg) |
| `utils/seo_metadata_exporter.py` | Industrial-grade exporter that maps sanitized metadata into a structured CSV audit report (`Task_ID`, `Status`, `Extracted_Meta_Title`). | ![Stable](https://img.shields.io/badge/status-stable-brightgreen.svg) |

---

## Usage

### 1. IndexNow Submission (lightest path — no OAuth)

```bash
# Single URL
python core/index_now.py \
    --url https://henghongrv.com/products/12v-leveling-jacks \
    --key YOUR_INDEXNOW_KEY

# Batch from a URL file
python core/index_now.py --file urls.txt --key YOUR_INDEXNOW_KEY
```

### 2. Sitemap-Driven Bulk Indexing (Google Indexing API)

```bash
python core/batch_index.py
# Reads sitemap.xml, authenticates via credentials.json, pushes every <loc> URL.
```

### 3. Single / Batch URL Submission (Google Indexing API client)

```bash
python core/google_quick_index.py --url https://henghongrv.com/new-page
python core/google_quick_index.py --file urls.txt --type URL_UPDATED --verbose
```

### 4. GSC Performance Analytics

```bash
python core/core_gsc_orchestrator.py \
    --site https://henghongrv.com/ \
    --days 30 \
    --dimension query \
    --export gsc_report.csv
```

### 5. Metadata Cleansing → CSV Export

```bash
python utils/seo_metadata_exporter.py
# Produces seo_audit_report.csv with normalized titles and SUCCESS/FAILED flags.
```

### Expected CSV Output Schema

```csv
Task_ID,Status,Extracted_Meta_Title
SEO-TASK-001,SUCCESS,12V Electric RV Leveling Jacks | High Capacity
SEO-TASK-002,SUCCESS,Heavy-Duty Hydraulic Valve Durability Specs
SEO-TASK-003,SUCCESS,B2B Sourcing Matrix 2026 | Henghong Intelligent
SEO-TASK-004,FAILED,STATUS_ERROR: Missing Meta Title
```

---

## Security & Credential Hygiene

AutoSEO-Lab is engineered under a **zero-leak** policy. The `.gitignore` is configured to
hard-block every sensitive artifact:

- `credentials.json`, `client_secret*.json`, `service_account*.json`, `*_token.json`
- Private keys: `*.pem`, `*.key`, `*.crt`, `*.p12`, `*.pfx`
- Environment files: `.env`, `.env.*`
- Generated data exports: `*.csv`, `*.tsv`, `*.txt`, `*.xlsx`
- Python artifacts: `__pycache__/`, `*.pyc`, `.pytest_cache/`

**Pre-commit verification:**

```bash
# Confirm no secret is staged
git diff --cached --name-only | grep -E "credentials|service_account|\.env|\.pem|\.key"
# Expected: no output
```

> If a credential was committed in a prior commit, remove it from tracking (the file itself
> remains on disk):
> ```bash
> git rm --cached credentials.json
> ```

---

## Roadmap

- [ ] Complete the OAuth 2.0 flow in `core_gsc_orchestrator.py` (replace mock payload)
- [ ] Wire the live Indexing API call in `google_quick_index.py`
- [ ] **GEO module**: structured-data exporter optimized for LLM retrieval (schema.org +
  `llms.txt` generation)
- [ ] Add `requirements.txt` and `pyproject.toml` for reproducible environments
- [ ] GitHub Actions workflow for linting (ruff) and CSV schema validation
- [ ] Multilingual metadata normalization (EN / ZH) for cross-market B2B pages

---

## License

Released under the **MIT License**. See [`LICENSE`](LICENSE) for full terms.

---

<sub>Built for the B2B SEO trenches — deterministic, auditable, and resolutely scriptable.</sub>
