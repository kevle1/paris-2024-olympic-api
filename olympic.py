from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


url = "https://olympics.com/en/paris-2024/medals"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"


def get_olympic_medal_tally(
    fetch_all: bool = False, ioc_noc_code: str = None
) -> dict[str, any]:
    if fetch_all:
        soup = _get_soup_with_selenium()
    else:
        response = requests.get(url, headers={"User-Agent": user_agent})
        soup = BeautifulSoup(response.text, "html.parser")

    return _parse_soup_medal_tally(soup, ioc_noc_code)


def _get_soup_with_selenium() -> BeautifulSoup:
    """
    The Olympic medals site is lazy loading NOCs so we use Selenium
    to get the full page with all countries loaded.
    """
    chrome_options = Options()

    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument(f"user-agent={user_agent}")
    # Hack to get all countries on one page
    chrome_options.add_argument("--window-size=50,2500")

    driver = webdriver.Chrome(
        options=chrome_options,
        service=ChromeService(ChromeDriverManager().install()),
    )

    driver.get(url)

    try:
        # The time element is at the bottom of the table so we use it to assert the full table is loaded
        WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.TAG_NAME, "time"))
        )
    except TimeoutException:
        raise ("Failed to load all results, could not fully load table")

    page = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup("".join(page), "html.parser")
    driver.quit()

    return soup


def _parse_soup_medal_tally(
    soup: BeautifulSoup, ioc_noc_code: str = None
) -> dict[str, any]:
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

    if ioc_noc_code:
        for result in ranked_results:
            if result["country"]["code"].lower() == ioc_noc_code.lower():
                return {
                    "last_updated": last_updated,
                    "length": 1,
                    "results": [result],
                }
        return {"last_updated": last_updated, "length": 0, "results": []}

    return {
        "last_updated": last_updated,
        "length": len(ranked_results),
        "results": ranked_results,
    }


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
