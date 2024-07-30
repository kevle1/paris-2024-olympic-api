from bs4 import BeautifulSoup
import requests
import pycountry


def get_noc_codes() -> dict[str, str]:
    response = requests.get("https://en.wikipedia.org/wiki/List_of_IOC_country_codes")
    soup = BeautifulSoup(response.content, "html.parser")
    noc_table = soup.find("table", {"class": "wikitable"})

    ioc_noc_codes = {}
    for noc in noc_table.find_all("tr")[1:]:
        cols = noc.find_all("td")
        if len(cols) >= 2:
            noc_code = cols[0].text.strip()
            country = cols[1].text.strip()
            ioc_noc_codes[country] = noc_code

    return ioc_noc_codes


def get_country_codes() -> tuple[list[dict[str, str]], dict[str, dict[str, str]]]:
    response = requests.get(
        "https://en.wikipedia.org/wiki/Comparison_of_alphabetic_country_codes"
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
    noc_to_country = {}
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
        noc_to_country[ioc_noc_code] = data

    return codes, noc_to_country


def inject_iso_codes(results: list[dict[str, any]]):
    _, noc_to_country = get_country_codes()

    for result in results:
        country = result["country"]
        ioc_noc_code = country["code"]

        if ioc_noc_code in noc_to_country:
            country["iso_alpha_3"] = noc_to_country[ioc_noc_code]["iso_alpha_3"]
            country["iso_alpha_2"] = noc_to_country[ioc_noc_code]["iso_alpha_2"]

    return results
