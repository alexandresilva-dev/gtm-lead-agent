from unittest.mock import Mock, patch

from gtm_agent.enrich import enrich_company


def test_enrich_company_success():
    fake_response = Mock()
    fake_response.raise_for_status = Mock()
    fake_response.json.return_value = [
        {"name": "Notion Labs", "domain": "notion.so", "logo": "https://logo.clearbit.com/notion.so"}
    ]
    with patch("gtm_agent.enrich.requests.get", return_value=fake_response) as mocked_get:
        result = enrich_company("Notion")

    assert result == {
        "company_name": "Notion Labs",
        "domain": "notion.so",
        "logo": "https://logo.clearbit.com/notion.so",
    }
    mocked_get.assert_called_once()


def test_enrich_company_no_results_falls_back():
    fake_response = Mock()
    fake_response.raise_for_status = Mock()
    fake_response.json.return_value = []
    with patch("gtm_agent.enrich.requests.get", return_value=fake_response):
        result = enrich_company("Some Obscure Company Xyz")

    assert result == {"company_name": "Some Obscure Company Xyz", "domain": "", "logo": ""}


def test_enrich_company_network_error_falls_back():
    import requests

    with patch("gtm_agent.enrich.requests.get", side_effect=requests.RequestException("boom")):
        result = enrich_company("Anything")

    assert result == {"company_name": "Anything", "domain": "", "logo": ""}


def test_enrich_company_empty_name():
    result = enrich_company("")
    assert result == {"company_name": "", "domain": "", "logo": ""}
