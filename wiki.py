from bs4 import BeautifulSoup
import requests
from olympic import _parse_wiki_code_cell


response = requests.get(
    "https://en.wikipedia.org/wiki/Comparison_of_alphabetic_country_codes"
)
soup = BeautifulSoup(response.content, "html.parser")
noc_table = soup.find("table", {"class": "wikitable"})

codes = []
country_to_noc = {}
for noc in noc_table.find_all("tr")[1:]:
    columns = noc.find_all("td")

    country = _parse_wiki_code_cell(columns[1].find("a").text)

    ioc_noc_code = _parse_wiki_code_cell(columns[2].text)
    fifa_code = _parse_wiki_code_cell(columns[3].text)
    iso_alpha_3 = _parse_wiki_code_cell(columns[4].text.strip())

    codes.append(
        {
            "country": country,
            "ioc_noc_code": ioc_noc_code,
            "fifa_code": fifa_code,
            "iso_alpha_3": iso_alpha_3,
        }
    )

    country_to_noc[country] = ioc_noc_code

print(codes)
