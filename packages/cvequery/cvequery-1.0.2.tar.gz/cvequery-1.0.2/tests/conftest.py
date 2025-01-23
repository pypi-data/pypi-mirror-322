import pytest
import responses
from typing import Dict, Any

@pytest.fixture
def mock_cve_response() -> Dict[str, Any]:
    """Mock response for single CVE lookup."""
    return {
        "cve_id": "CVE-2023-1234",
        "summary": "Test vulnerability",
        "cvss_v3": 7.5,
        "epss": "0.5",
        "references": ["https://example.com"],
        "published": "2023-01-01T00:00:00"
    }

@pytest.fixture
def mock_cves_response() -> Dict[str, Any]:
    """Mock response for multiple CVEs lookup."""
    return {
        "cves": [
            {
                "cve_id": "CVE-2023-1234",
                "summary": "Test vulnerability 1",
                "cvss_v3": 7.5
            },
            {
                "cve_id": "CVE-2023-5678",
                "summary": "Test vulnerability 2",
                "cvss_v3": 8.5
            }
        ],
        "total": 2
    }

@pytest.fixture
def mock_api_responses(mock_cve_response, mock_cves_response):
    """Set up mock API responses."""
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        # Mock single CVE endpoint
        rsps.add(
            responses.GET,
            "https://cvedb.shodan.io/cve/CVE-2023-1234",
            json=mock_cve_response,
            status=200
        )
        
        # Mock CVEs search endpoint - basic search
        rsps.add(
            responses.GET,
            "https://cvedb.shodan.io/cves",
            json=mock_cves_response,
            status=200,
            match=[
                responses.matchers.query_param_matcher({
                    "product": "test_product",
                    "limit": "100"
                })
            ]
        )
        
        # Mock CVEs search with filters
        rsps.add(
            responses.GET,
            "https://cvedb.shodan.io/cves",
            json=mock_cves_response,
            status=200,
            match=[
                responses.matchers.query_param_matcher({
                    "product": "test_product",
                    "is_kev": "true",
                    "severity": "high",
                    "start_date": "2023-01-01",
                    "limit": "100"
                })
            ]
        )

        # Mock CVEs search for only-cve-ids option
        rsps.add(
            responses.GET,
            "https://cvedb.shodan.io/cves",
            json=mock_cves_response,
            status=200,
            match=[
                responses.matchers.query_param_matcher({
                    "product": "test_product",
                    "limit": "100"
                })
            ]
        )
        yield rsps 