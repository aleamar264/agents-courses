import urllib.parse
import httpx
from bs4 import BeautifulSoup
import os
import urllib


url = "https://docs.llamaindex.ai/en/stable/"
output_directory = "./llamaindex_examples/llamaindex-docs/"
os.makedirs(output_directory, exist_ok=True)

# Fetch the page
response = httpx.get(url)
print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all the links to .html files
links = soup.find_all("a", href=True)


# This way only get the links of the first page, is not recursive
for link in links:
    href = link["href"]
    # if href.endswith(".html"):
    #     print(href)
    #     if not href.startswith("http"):
    href = urllib.parse.urljoin(url, href)
    print(f"downloading {href}")
    file_response = httpx.get(href)

    base_name =  os.path.basename(href)
    if base_name is None or base_name == "":
        base_name = "home"
    file_name = os.path.join(output_directory, base_name+".html")
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(file_response.text)
