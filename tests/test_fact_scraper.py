import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fact_scraper import scrape_facts, generate_html, main

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.text = """
    <html>
        <p>Short text</p>
        <p>This is a properly long fact that should be picked up by our scraper since it's over 50 characters.</p>
    </html>
    """
    return mock

def test_scrape_facts(mock_response):
    with patch("requests.get", return_value=mock_response):
        fact = scrape_facts()
        assert len(fact) > 50
        assert isinstance(fact, str)

def test_generate_html():
    test_fact = "Test fact content"
    html = generate_html(test_fact)
    assert "<!DOCTYPE html>" in html
    assert test_fact in html

def test_main(tmp_path):
    mock_fact = "This is a test fact"
    with patch("fact_scraper.scrape_facts", return_value=mock_fact):
        with patch("fact_scraper.Path") as mock_path:
            mock_path.return_value = tmp_path / "fact.html"
            main()
            assert (tmp_path / "fact.html").exists()
