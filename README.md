# GTM Lead Agent

A small end-to-end tool that takes a raw list of leads, enriches each company via a public API, and drafts a personalized outreach email for every contact, optionally using an LLM (Claude or GPT) instead of a template.

I built this after reading a job posting for a "Working Student, GTM Engineering" role that asked for exactly three things: scripting in Python/TypeScript, integrating tools via APIs, and prototyping AI powered workflows. This project is a compact demonstration of all three working together, not three separate toy examples.

## How it works

Enrichment, in gtm_agent/enrich.py, looks up each company name through Clearbit's public Autocomplete endpoint, which needs no auth, to get a canonical name, domain and logo. Any network failure or unmatched company falls back to the original name instead of crashing the batch.

Outreach drafting, in gtm_agent/outreach.py, generates a short, personalized email per lead. Three interchangeable modes are supported: mock (template based, no dependencies, no API key, works instantly), anthropic (calls Claude via ANTHROPIC_API_KEY), and openai (calls GPT via OPENAI_API_KEY).

The CLI, in gtm_agent/cli.py, wires it together: reads a CSV, writes an enriched CSV.

## Running it

Install dependencies with pip install -r requirements.txt.

Zero setup, no API keys required: python -m gtm_agent.cli --input data/sample_leads.csv --output data/enriched_leads.csv --mode mock

With a real LLM (requires the anthropic or openai package plus an API key): pip install anthropic, then export ANTHROPIC_API_KEY=sk-..., then python -m gtm_agent.cli --mode anthropic

## Tests

Install pytest and run it: pip install pytest, then pytest.

Seven tests cover the enrichment fallback logic (success, no match, network error, empty input) and the outreach drafting (mock output content, missing fields, invalid mode).

## Why this shape

Real GTM and growth engineering work is rarely "write one clever script", it is usually gluing together a data source, an external API, and increasingly an LLM step, in a way that keeps working when one piece fails. That is why the enrichment step degrades gracefully instead of throwing, and why the outreach step supports a free, local mode alongside the real API calls: the project runs and is reviewable by anyone, immediately, without needing my API keys.

## Next steps

Possible extensions include swapping the CSV input and output for a Google Sheets or HubSpot/Notion API integration, adding a second enrichment source such as company size or funding stage, and turning the CLI into a small scheduled job (cron or GitHub Actions) that processes new leads automatically.
