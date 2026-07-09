"""Draft personalized outreach copy for a lead.

Three modes are supported:

- "mock"      - template-based, zero dependencies, zero API keys. Runs
                anywhere out of the box, useful for demos and tests.
- "anthropic" - calls Claude via ANTHROPIC_API_KEY.
- "openai"    - calls GPT via OPENAI_API_KEY.

The point of splitting it this way is that the *shape* of a real AI-agent
integration (prompt building, provider swap, env-based config) is all here
and works today, without requiring anyone to hand me a paid API key just to
try the project.
"""

from __future__ import annotations

import os

SUPPORTED_MODES = ("mock", "anthropic", "openai")


def draft_outreach(lead: dict, mode: str = "mock") -> str:
    if mode not in SUPPORTED_MODES:
        raise ValueError(f"Unknown mode '{mode}'. Use one of {SUPPORTED_MODES}.")

    if mode == "mock":
        return _mock_draft(lead)
    if mode == "anthropic":
        return _anthropic_draft(lead)
    return _openai_draft(lead)


def _build_prompt(lead: dict) -> str:
    name = lead.get("contact_name", "there")
    company = lead.get("company_name", "their company")
    role = lead.get("role", "")
    return (
        "Write a short, friendly, non-salesy cold outreach email (max 80 words) "
        f"to {name}, who works as {role or 'a professional'} at {company}. "
        "Mention the company by name, keep the tone casual and human, avoid "
        "buzzwords, and end with a soft, low-pressure call to action."
    )


def _mock_draft(lead: dict) -> str:
    name = lead.get("contact_name", "there")
    company = lead.get("company_name", "your company")
    role = lead.get("role", "")
    return (
        f"Hi {name},\n\n"
        f"Saw that {company} has been investing in {role or 'the team'} lately "
        "- exciting stuff. Wanted to reach out because we help teams like "
        "yours automate the repetitive parts of GTM so people can focus on "
        "the work that actually moves the needle.\n\n"
        "Worth a quick 15-minute chat this week?\n\n"
        "Best,\nAlexandre"
    )


def _anthropic_draft(lead: dict) -> str:
    from anthropic import Anthropic  # imported lazily: optional dependency

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=200,
        messages=[{"role": "user", "content": _build_prompt(lead)}],
    )
    return message.content[0].text


def _openai_draft(lead: dict) -> str:
    from openai import OpenAI  # imported lazily: optional dependency

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=200,
        messages=[{"role": "user", "content": _build_prompt(lead)}],
    )
    return response.choices[0].message.content
