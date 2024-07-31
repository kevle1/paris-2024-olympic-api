from bs4 import BeautifulSoup
import requests

from datetime import datetime

from countries import get_noc_codes, inject_iso_codes

OLYMPICS_DATA_URL = (
    "https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json"
)
OLYMPICS_SITE_URL = "https://olympics.com/en/paris-2024/medals"
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"


def get_olympic_medal_tally(
    ioc_noc_code: str = None,
) -> dict[str, any]:
    try:
        last_updated, results, source = _get_olympic_data_results()
    except Exception as e:
        print(
            f"Error fetching data from olympics.com data: {e}, falling back to scraping"
        )
        soup = _get_soup(OLYMPICS_SITE_URL)
        last_updated, results, source = _parse_olympic_soup_medal_tally(soup)

    if ioc_noc_code:
        result = _get_result_for_noc(results, ioc_noc_code)
        if result:
            results = [result]
        else:
            results = []

    if results:
        results = inject_iso_codes(results)

    return {
        "last_updated": last_updated,
        "source": source,
        "length": len(results),
        "results": results,
    }


def _get_result_for_noc(
    results: list[dict[str, any]], ioc_noc_code: str
) -> dict[str, any]:
    for result in results:
        if result["country"]["code"].lower() == ioc_noc_code.lower():
            return result
    return None


def _get_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    return BeautifulSoup(response.text, "html.parser")


def _get_olympic_data_results():
    response = requests.get(OLYMPICS_DATA_URL, headers={"User-Agent": USER_AGENT})
    noc_codes = get_noc_codes()

    nocs = {}
    for item in response.json()["medalNOC"]:
        if item["gender"] == "TOT" and item["sport"] == "GLO":
            noc = item["org"]
            if noc not in nocs:
                nocs[item["org"]] = {
                    "gold": 0,
                    "silver": 0,
                    "bronze": 0,
                    "rank": item["rank"],
                }
            nocs[noc]["gold"] += item["gold"]
            nocs[noc]["silver"] += item["silver"]
            nocs[noc]["bronze"] += item["bronze"]

    results = []
    for noc, medals in nocs.items():
        gold = medals["gold"]
        silver = medals["silver"]
        bronze = medals["bronze"]

        country_data = {
            "country": {
                "code": noc,
                "name": noc_codes.get(noc, {}).get("description", None),
            },
            "medals": {
                "bronze": bronze,
                "gold": gold,
                "silver": silver,
                "total": bronze + gold + silver,
            },
            "rank": medals["rank"],
        }

        results.append(country_data)
    ranked_results = sorted(results, key=lambda x: x["rank"])

    return datetime.now().isoformat(), ranked_results, OLYMPICS_DATA_URL


def _parse_wikipedia_soup_medal_tally(
    soup: BeautifulSoup,
) -> tuple[str, list[dict[str, any]], str]:
    ioc_noc_codes = get_noc_codes()
    table = soup.find("caption", text="2024 Summer Olympics medal table").find_parent(
        "table"
    )
    results = []
    noc_rows = table.find("tbody").find_all("tr")

    for noc in noc_rows[1:-1]:
        cells = noc.find_all(["td", "th"])
        country_name = noc.find("a").text

        offset = 0
        # some countries share a merged cell for the rank and country name
        # causing the medal count to be at a different index
        if len(cells) == 5:
            offset = 1

        gold = int(cells[2 - offset].text)
        silver = int(cells[3 - offset].text)
        bronze = int(cells[4 - offset].text)

        country_data = {
            "country": {
                "code": ioc_noc_codes.get(country_name),
                "name": country_name,
            },
            "medals": {
                "bronze": bronze,
                "gold": gold,
                "silver": silver,
                "total": bronze + gold + silver,
            },
        }

        results.append(country_data)

    ranked_results = _calculate_rankings(results)
    return datetime.now().isoformat(), ranked_results, "wikipedia.org"


def _parse_olympic_soup_medal_tally(
    soup: BeautifulSoup,
) -> tuple[str, list[dict[str, any]], str]:
    noc_rows = soup.find_all("div", {"data-testid": "noc-row"})
    results = []

    for noc in noc_rows:
        spans = noc.find_all("span")

        country_code = spans[1].text
        country_name = spans[2].text

        gold = spans[3].text
        silver = spans[4].text
        bronze = spans[5].text
        total = spans[6].text

        result = {
            "country": {
                "code": country_code,
                "name": country_name,
            },
            "medals": {
                "gold": int(gold),
                "silver": int(silver),
                "bronze": int(bronze),
                "total": int(total),
            },
        }

        results.append(result)

    last_updated = soup.find("time")["datetime"]
    ranked_results = _calculate_rankings(results)

    return last_updated, ranked_results, "olympics.com"


def _calculate_rankings(results: list[dict[str, any]]) -> list[dict[str, any]]:
    """
    We are unable to extract the ranking from the website medal tally, so we need to calculate it ourselves.
    Following convention outlined in https://en.wikipedia.org/wiki/Olympic_medal_table
    """
    results.sort(
        key=lambda x: (
            x["medals"]["gold"],
            x["medals"]["silver"],
            x["medals"]["bronze"],
            x["country"]["code"],
        ),
        reverse=True,
    )

    rank = 1
    for i in range(len(results)):
        if i > 0:
            # if medal counts are equal, rank is the same
            if (
                results[i]["medals"]["gold"] == results[i - 1]["medals"]["gold"]
                and results[i]["medals"]["silver"] == results[i - 1]["medals"]["silver"]
                and results[i]["medals"]["bronze"] == results[i - 1]["medals"]["bronze"]
            ):
                results[i]["rank"] = results[i - 1]["rank"]
            else:
                results[i]["rank"] = rank
        else:
            results[i]["rank"] = rank

        rank += 1

    # countries with same rank should be sorted by IOC country code
    results.sort(key=lambda x: (x["rank"], x["country"]["code"]))

    return results
