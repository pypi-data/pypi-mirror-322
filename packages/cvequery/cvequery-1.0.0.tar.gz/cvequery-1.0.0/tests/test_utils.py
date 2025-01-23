import pytest
import json
import os
from datetime import datetime
from src.utils import (
    save_to_json,
    validate_date,
    filter_by_severity,
    sort_by_epss_score,
    create_cache_key,
    colorize_output,
    SEVERITY_MAP,
    get_cvss_severity
)

def test_save_to_json(tmp_path):
    """Test saving data to JSON file."""
    test_data = {"test": "data"}
    filename = tmp_path / "test.json"
    
    save_to_json(test_data, str(filename))
    assert filename.exists()
    
    with open(filename) as f:
        loaded_data = json.load(f)
    assert loaded_data == test_data

def test_validate_date():
    """Test date validation function."""
    assert validate_date("2023-01-01") == True
    assert validate_date("2023-13-01") == False  # Invalid month
    assert validate_date("2023-01-32") == False  # Invalid day
    assert validate_date("invalid-date") == False
    assert validate_date("") == False

def test_filter_by_severity():
    """Test CVE filtering by severity levels."""
    test_data = {
        "cves": [
            {"cve_id": "CVE-2023-1", "cvss_v3": 9.5},  # Critical
            {"cve_id": "CVE-2023-2", "cvss_v3": 7.5},  # High
            {"cve_id": "CVE-2023-3", "cvss_v3": 5.5},  # Medium
            {"cve_id": "CVE-2023-4", "cvss_v3": 2.5},  # Low
            {"cve_id": "CVE-2023-5", "cvss_v3": None}  # No CVSS
        ]
    }
    
    # Test single severity
    result = filter_by_severity(test_data, ["critical"])
    assert len(result["cves"]) == 1
    assert result["cves"][0]["cve_id"] == "CVE-2023-1"
    
    # Test multiple severities
    result = filter_by_severity(test_data, ["high", "critical"])
    assert len(result["cves"]) == 2
    
    # Test with invalid severity
    result = filter_by_severity(test_data, ["invalid"])
    assert len(result["cves"]) == 0
    
    # Test with empty severity list
    result = filter_by_severity(test_data, [])
    assert result == test_data

def test_sort_by_epss_score():
    """Test sorting CVEs by EPSS score."""
    test_data = {
        "cves": [
            {"cve_id": "CVE-2023-1", "epss": "0.5"},
            {"cve_id": "CVE-2023-2", "epss": "0.8"},
            {"cve_id": "CVE-2023-3", "epss": "0.2"},
            {"cve_id": "CVE-2023-4", "epss": None},
            {"cve_id": "CVE-2023-5", "epss": "invalid"}
        ]
    }
    
    result = sort_by_epss_score(test_data)
    sorted_cves = result["cves"]
    
    # Check sorting order
    assert sorted_cves[0]["cve_id"] == "CVE-2023-2"  # 0.8
    assert sorted_cves[1]["cve_id"] == "CVE-2023-1"  # 0.5
    assert sorted_cves[2]["cve_id"] == "CVE-2023-3"  # 0.2
    
    # Invalid/None EPSS scores should be at the end
    assert sorted_cves[-2]["epss"] is None
    assert sorted_cves[-1]["epss"] == "invalid"

def test_create_cache_key():
    """Test cache key creation."""
    key1 = create_cache_key("test", a=1, b=2)
    key2 = create_cache_key("test", b=2, a=1)  # Same params, different order
    key3 = create_cache_key("test", a=1, b=3)  # Different value
    
    assert key1 == key2  # Order shouldn't matter
    assert key1 != key3  # Different values should produce different keys
    assert len(key1) == 32  # MD5 hash length

def test_colorize_output(capsys):
    """Test colorized output formatting."""
    test_data = {
        "cvss": 7.5,
        "summary": "Test vulnerability",
        "epss": 0.5
    }
    
    colorize_output(test_data, ["cvss", "summary"])
    captured = capsys.readouterr()
    
    assert "7.5" in captured.out
    assert "Test vulnerability" in captured.out
    assert "0.5" not in captured.out  # Not in requested fields

def test_filter_by_severity_with_multiple_levels():
    """Test filtering CVEs by multiple severity levels."""
    test_data = {
        "cves": [
            {"cve_id": "CVE-2023-1", "cvss_v3": 9.5},  # Critical
            {"cve_id": "CVE-2023-2", "cvss_v3": 7.5},  # High
            {"cve_id": "CVE-2023-3", "cvss_v3": 5.5},  # Medium
            {"cve_id": "CVE-2023-4", "cvss_v3": 2.5},  # Low
        ]
    }
    
    result = filter_by_severity(test_data, ["high", "critical"])
    assert len(result["cves"]) == 2
    assert result["cves"][0]["cvss_v3"] == 9.5
    assert result["cves"][1]["cvss_v3"] == 7.5

def test_get_cvss_severity():
    """Test CVSS severity level calculation."""
    assert get_cvss_severity(9.8) == "critical"
    assert get_cvss_severity(7.5) == "high"
    assert get_cvss_severity(5.5) == "medium"
    assert get_cvss_severity(2.5) == "low"
    assert get_cvss_severity(0.0) == "none"

def test_filter_by_severity_with_mixed_cvss():
    """Test filtering CVEs with both CVSS v2 and v3 scores."""
    test_data = {
        "cves": [
            {"cve_id": "CVE-2023-1", "cvss_v3": 9.5},  # Critical
            {"cve_id": "CVE-2023-2", "cvss": 7.5},     # High (v2)
            {"cve_id": "CVE-2023-3", "cvss_v3": 5.5},  # Medium
            {"cve_id": "CVE-2023-4", "cvss": None},    # None
        ]
    }
    
    result = filter_by_severity(test_data, ["high", "critical"])
    assert len(result["cves"]) == 2
    assert result["cves"][0]["cvss_v3"] == 9.5
    assert result["cves"][1]["cvss"] == 7.5
