"""Command-line entrypoint: read leads -> enrich -> draft outreach -> write CSV."""

from __future__ import annotations

import argparse
import csv

from .enrich import enrich_company
from .outreach import draft_outreach


def run(input_path: str, output_path: str, mode: str) -> list[dict]:
    with open(input_path, newline="", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))

    if not leads:
        raise ValueError(f"No rows found in {input_path}")

    results = []
    for lead in leads:
        enriched = enrich_company(lead.get("company_name", ""))
        lead.update(enriched)
        lead["outreach_draft"] = draft_outreach(lead, mode=mode)
        results.append(lead)
        print(f"Processed {lead.get('contact_name', '?')} @ {lead['company_name']}")

    fieldnames = list(results[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nDone. Wrote {len(results)} enriched leads to {output_path}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Enrich a list of leads and draft personalized outreach emails."
    )
    parser.add_argument("--input", default="data/sample_leads.csv")
    parser.add_argument("--output", default="data/enriched_leads.csv")
    parser.add_argument(
        "--mode",
        choices=["mock", "anthropic", "openai"],
        default="mock",
        help="Draft generation mode. 'mock' needs no API key and no internet for the LLM call.",
    )
    args = parser.parse_args()
    run(args.input, args.output, args.mode)


if __name__ == "__main__":
    main()
