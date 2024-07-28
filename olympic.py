import requests
from bs4 import BeautifulSoup

url = "https://olympics.com/en/paris-2024/medals"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def _calculate_rankings(results: list[dict[str, any]]) -> list[dict[str, any]]:
    """
    We are unable to extract the ranking from the website medal table, so we need to calculate it ourselves.
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


def get_olympic_medal_tally(ioc_noc_code: str = None) -> dict[str, any]:
    response = requests.get(url, timeout=2, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for noc in soup.find_all("div", {"data-testid": "noc-row"}):
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

    if ioc_noc_code:
        for result in ranked_results:
            if result["country"]["code"].lower() == ioc_noc_code.lower():
                return {
                    "last_updated": last_updated,
                    "results": [result],
                }
        return {"last_updated": last_updated, "results": []}

    return {
        "last_updated": last_updated,
        "results": ranked_results,
    }
