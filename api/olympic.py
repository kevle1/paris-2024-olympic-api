from bs4 import BeautifulSoup
import requests

from datetime import datetime

from api.countries import get_noc_codes, inject_iso_codes

OLYMPICS_DATA_URL = (
    "https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json"
)
PARALYMPICS_DATA_URL = (
    "https://olympics.com/PG2024/data/CIS_MedalNOCs~lang=ENG~comp=PG2024.json"
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

    return _build_response(last_updated, results, source, ioc_noc_code=ioc_noc_code)


def get_paralympic_medal_tally(
    ioc_noc_code: str = None,
) -> dict[str, any]:
    return _build_response(*_get_paralympic_data_results(), ioc_noc_code=ioc_noc_code)


def _build_response(
    last_updated: str,
    results: list[dict[str, any]],
    source: str,
    ioc_noc_code: str = None,
) -> dict[str, any]:
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
    ranked_results = _parse_olympic_api_results(response.json())

    return datetime.now().isoformat(), ranked_results, OLYMPICS_DATA_URL


def _get_paralympic_data_results():
    response = requests.get(PARALYMPICS_DATA_URL, headers={"User-Agent": USER_AGENT})
    ranked_results = _parse_olympic_api_results(response.json())

    return datetime.now().isoformat(), ranked_results, PARALYMPICS_DATA_URL


def _parse_olympic_api_results(
    data: dict[str, any]
) -> tuple[str, list[dict[str, any]], str]:
    noc_codes = get_noc_codes()
    nocs = {}
    for item in data["medalNOC"]:
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
    return sorted(results, key=lambda x: x["rank"])


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

    ranked_results = _calculate_rankings(results)

    return datetime.now().isoformat(), ranked_results, "olympics.com"


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
