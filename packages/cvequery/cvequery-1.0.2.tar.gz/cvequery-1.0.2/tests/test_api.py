import pytest
from src.constants import BASE_URL
import responses
from src.api import (
    get_cve_data,
    get_cves_data,
    get_cpe_data,
)

@pytest.fixture
def mock_cve_response():
    return {
        "cve_id": "CVE-2023-1234",
        "summary": "Test vulnerability",
        "cvss_v3": 7.5,
        "epss": "0.5"
    }

@pytest.fixture
def mock_cves_response():
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

@responses.activate
def test_get_cve_data(mock_cve_response):
    """Test fetching single CVE data."""
    cve_id = "CVE-2023-1234"
    responses.add(
        responses.GET,
        f"{BASE_URL}/cve/{cve_id}",
        json=mock_cve_response,
        status=200
    )
    
    result = get_cve_data(cve_id)
    assert result == mock_cve_response
    assert result["cve_id"] == cve_id

@responses.activate
def test_get_cves_data(mock_cves_response):
    """Test fetching multiple CVEs with filters."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/cves",
        json=mock_cves_response,
        status=200
    )
    
    result = get_cves_data(
        product="test_product",
        is_kev=True,
        sort_by_epss=True
    )
    
    assert result == mock_cves_response
    assert len(result["cves"]) == 2
    assert result["total"] == 2

@responses.activate
def test_get_cpe_data():
    """Test fetching CPE data."""
    mock_response = {
        "cpes": ["cpe:2.3:a:vendor:product:1.0"],
        "total": 1
    }
    
    responses.add(
        responses.GET,
        f"{BASE_URL}/cpes",
        json=mock_response,
        status=200
    )
    
    result = get_cpe_data("test_product")
    assert result == mock_response
    assert len(result["cpes"]) == 1

@responses.activate
def test_api_error_handling():
    """Test API error handling."""
    # Test connection error
    responses.add(
        responses.GET,
        f"{BASE_URL}/cve/CVE-2023-1234",
        status=404
    )
    
    result = get_cve_data("CVE-2023-1234")
    assert "error" in result
    
    # Test invalid response format
    responses.add(
        responses.GET,
        f"{BASE_URL}/cves",
        json={"invalid": "response"},
        status=200
    )
    
    result = get_cves_data(product="test")
    assert "error" in result

def test_get_cpe_data_with_cpe23_format():
    """Test CPE data fetching with CPE 2.3 format."""
    cpe_string = "cpe:2.3:a:libpng:libpng:0.8"
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{BASE_URL}/cpes",
            json={"cpes": [cpe_string], "total": 1},
            match=[
                responses.matchers.query_param_matcher({
                    "cpe23": cpe_string
                })
            ],
            status=200
        )
        
        result = get_cpe_data(f"cpe23={cpe_string}")
        assert "error" not in result
        assert result["cpes"] == [cpe_string] 