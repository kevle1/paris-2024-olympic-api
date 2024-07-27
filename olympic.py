import requests
from bs4 import BeautifulSoup

url = "https://olympics.com/en/paris-2024/medals"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def get_olympic_medal_tally(ioc_country_code: str = None) -> dict[str, any]:
    response = requests.get(url, timeout=2, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    medal_table = soup.find("div", {"data-test-id": "virtuoso-item-list"})

    results = []
    for row in medal_table.find_all("div", {"data-testid": "noc-row"}):
        spans = row.find_all("span")

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

        if ioc_country_code and country_code.upper() == ioc_country_code.upper():
            return {
                "last_updated": soup.find("time")["datetime"],
                "results": [result],
            }

        results.append(result)

    if ioc_country_code:
        return []

    return {
        "last_updated": soup.find("time")["datetime"],
        "results": results,
    }
