"""Lead enrichment via a public, keyless API.

Uses Clearbit's Company Autocomplete endpoint (no auth required) to resolve
a company name into a canonical name, domain and logo. This is the kind of
lightweight, no-friction API integration a GTM engineer wires up constantly:
turn a messy free-text field into structured data other tools can use.
"""

from __future__ import annotations

import requests

CLEARBIT_AUTOCOMPLETE_URL = "https://autocomplete.clearbit.com/v1/companies/suggest"


def enrich_company(name: str, timeout: float = 5.0) -> dict:
    """Look up a company by name and return enrichment fields.

    Falls back to the raw name (and empty fields) on any network error or
    if the company isn't found, so a batch job never crashes on one bad
    lookup.
    """
    fallback = {"company_name": name, "domain": "", "logo": ""}

    if not name or not name.strip():
        return fallback

    try:
        response = requests.get(
            CLEARBIT_AUTOCOMPLETE_URL, params={"query": name}, timeout=timeout
        )
        response.raise_for_status()
        results = response.json()
    except (requests.RequestException, ValueError):
        return fallback

    if not results:
        return fallback

    top = results[0]
    return {
        "company_name": top.get("name") or name,
        "domain": top.get("domain", ""),
        "logo": top.get("logo", ""),
    }
