import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

response = requests.get(
    "https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json",
    headers={"User-Agent": USER_AGENT},
)

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
        print(nocs[noc])

# sort by rank
sorted_nocs = sorted(nocs.items(), key=lambda x: x[1]["rank"])

print(sorted_nocs)
