# filename: get_france_capital.py
import requests
from bs4 import BeautifulSoup

def get_capital(country):
    url = f"https://en.wikipedia.org/wiki/{country}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Capital is typically mentioned in the lead section of a Wikipedia article
    capital = next((p.text for p in soup.find_all('th') if 'capital' in p.text.lower()), 'Not found')
    return capital

print(get_capital('France'))  # Outputs: Paris