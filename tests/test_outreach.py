import pytest

from gtm_agent.outreach import draft_outreach


def test_mock_draft_mentions_company_and_name():
    lead = {"contact_name": "Maria Santos", "company_name": "Notion", "role": "Head of Growth"}
    draft = draft_outreach(lead, mode="mock")

    assert "Maria Santos" in draft
    assert "Notion" in draft


def test_mock_draft_handles_missing_fields():
    draft = draft_outreach({}, mode="mock")
    assert "there" in draft
    assert "your company" in draft


def test_unknown_mode_raises():
    with pytest.raises(ValueError):
        draft_outreach({"contact_name": "X", "company_name": "Y"}, mode="carrier-pigeon")
