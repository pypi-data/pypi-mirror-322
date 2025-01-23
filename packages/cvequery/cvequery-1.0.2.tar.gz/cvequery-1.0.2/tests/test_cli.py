import pytest
from click.testing import CliRunner
from src.cli import cli
import json
from pathlib import Path

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_api_responses(monkeypatch):
    """Mock API responses for CLI tests."""
    def mock_get_cves(*args, **kwargs):
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
    
    def mock_get_cve(*args, **kwargs):
        return {
            "cve_id": "CVE-2023-1234",
            "summary": "Test vulnerability",
            "cvss_v3": 7.5
        }
    
    # Patch the API functions
    monkeypatch.setattr('src.cli.get_cves_data', mock_get_cves)
    monkeypatch.setattr('src.cli.get_cve_data', mock_get_cve)
    return None

def test_help_command(runner):
    """Test help output."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "CVE Query Tool" in result.output

def test_fields_list_command(runner):
    """Test fields list output."""
    result = runner.invoke(cli, ["--fields-list"])
    assert result.exit_code == 0
    assert "Available fields:" in result.output
    assert "cvss" in result.output
    assert "summary" in result.output

def test_mutually_exclusive_options(runner):
    """Test mutually exclusive options validation."""
    result = runner.invoke(cli, ["-c", "CVE-2023-1234", "-mc", "CVE-2023-5678"])
    assert result.exit_code != 0
    assert "cannot be used with other CVE query options" in result.output

def test_cve_search_with_filters(runner, mock_api_responses):
    """Test CVE search with various filters."""
    result = runner.invoke(cli, [
        "-pcve", "test_product",
        "-k",
        "-s", "high",
        "-sd", "2023-01-01"
    ])
    
    assert result.exit_code == 0
    assert "CVE-2023-1234" in result.output
    assert "Test vulnerability 1" in result.output

def test_single_cve_lookup(runner, mock_api_responses):
    """Test looking up a single CVE."""
    result = runner.invoke(cli, ["-c", "CVE-2023-1234"])
    assert result.exit_code == 0
    assert "CVE-2023-1234" in result.output
    assert "Test vulnerability" in result.output

def test_json_output(runner, tmp_path, mock_api_responses):
    """Test JSON output functionality."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        output_file = Path("output.json")
        result = runner.invoke(cli, [
            "-c", "CVE-2023-1234",
            "-j", str(output_file)
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
        
        data = json.loads(output_file.read_text())
        assert data["cve_id"] == "CVE-2023-1234"
        assert data["summary"] == "Test vulnerability"

def test_invalid_date_format(runner):
    """Test invalid date format handling."""
    result = runner.invoke(cli, [
        "-pcve", "test_product",
        "-sd", "invalid-date"
    ])
    
    assert "Invalid start-date format" in result.output
    assert result.exit_code == 1

def test_only_cve_ids_option(runner, mock_api_responses):
    """Test only-cve-ids output option."""
    result = runner.invoke(cli, [
        "-pcve", "test_product",
        "-oci"
    ])
    
    assert result.exit_code == 0
    assert "CVE-2023-1234" in result.output
    assert "Test vulnerability" not in result.output 