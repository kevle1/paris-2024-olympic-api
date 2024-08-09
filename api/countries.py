import json
from bs4 import BeautifulSoup
import requests
import pycountry

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"


def get_noc_codes() -> dict[str, dict[str, str]]:
    response = requests.get(
        "https://olympics.com/OG2024/data/MIS_NOCS~lang=ENG~comp=OG2024.json",
        headers={"User-Agent": USER_AGENT},
    )
    nocs = {}
    for noc in response.json()["nocs"]:
        nocs[noc["code"]] = noc
    return nocs


def get_country_codes() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    response = requests.get(
        "https://en.wikipedia.org/wiki/Comparison_of_alphabetic_country_codes",
        headers={"User-Agent": USER_AGENT},
    )
    soup = BeautifulSoup(response.content, "html.parser")
    noc_table = soup.find("table", {"class": "wikitable"})

    def _parse_wiki_code_cell(cell: str) -> str:
        """
        Empty cells and cells that just contain references should be returned as None
        """
        if not cell.strip():
            return None
        elif cell.startswith("[") or cell.startswith("]"):
            return None
        else:
            return cell.strip()

    codes = []
    for noc in noc_table.find_all("tr")[1:]:
        columns = noc.find_all("td")

        country_name = _parse_wiki_code_cell(columns[1].find("a").text)

        ioc_noc_code = _parse_wiki_code_cell(columns[2].text)
        fifa_code = _parse_wiki_code_cell(columns[3].text)
        iso_alpha_3 = _parse_wiki_code_cell(columns[4].text.strip())

        if iso_alpha_3:
            try:
                country = pycountry.countries.lookup(iso_alpha_3)
            except LookupError:
                country = None

        data = {
            "country_name": country.name if country else country_name,
            "ioc_noc_code": ioc_noc_code,
            "fifa_code": fifa_code,
            "iso_alpha_3": iso_alpha_3,
            "iso_alpha_2": country.alpha_2 if country else None,
        }
        codes.append(data)

    return codes


def load_country_codes():
    with open("countries.json") as f:
        return json.load(f)


def inject_iso_codes(results: list[dict[str, any]]):
    codes = load_country_codes()
    noc_to_country = {code["ioc_noc_code"]: code for code in codes}

    for result in results:
        country = result["country"]
        ioc_noc_code = country["code"]

        if ioc_noc_code in noc_to_country:
            country["iso_alpha_3"] = noc_to_country[ioc_noc_code]["iso_alpha_3"]
            country["iso_alpha_2"] = noc_to_country[ioc_noc_code]["iso_alpha_2"]

    return results
