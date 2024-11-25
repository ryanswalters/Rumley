import requests
from bs4 import BeautifulSoup
import random
import time
from pathlib import Path
import html
import logging
from typing import Optional, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MINIMUM_FACT_LENGTH = 50
REFRESH_INTERVAL = 3600
TIMEOUT = 10
DANGEROUS_PATTERNS = ["javascript:", "script"]

def scrape_facts() -> Optional[str]:
    sources = [
        "https://www.factretriever.com/",
        "https://www.thefactsite.com/",
        "https://www.sciencekids.co.nz/sciencefacts.html"
    ]
    facts: List[str] = []
    
    for url in sources:
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            facts.extend([p.text.strip() for p in paragraphs if len(p.text.strip()) > MINIMUM_FACT_LENGTH])
        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            continue
    
    return random.choice(facts) if facts else None

def generate_html(fact: str) -> str:
    escaped_fact = html.escape(fact)
    return f"""<!DOCTYPE html>
    <html>
    <head>
        <title>Random Facts</title>
        <meta http-equiv="refresh" content="{REFRESH_INTERVAL}">
        <style>
            body {{ 
                font-family: Arial;
                background: #f0f2f5;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .fact-container {{
                background: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                max-width: 600px;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="fact-container">
            <p>{escaped_fact}</p>
        </div>
    </body>
    </html>"""

def main() -> None:
    try:
        fact = scrape_facts()
        if fact:
            html_content = generate_html(fact)
            output_path = Path("fact.html")
            output_path.write_text(html_content, encoding="utf-8")
            logger.info(f"Fact saved to {output_path.absolute()}")
        else:
            logger.warning("No facts were retrieved")
    except Exception as e:
        logger.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
