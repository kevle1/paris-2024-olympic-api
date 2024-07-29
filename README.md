# Paris 2024 Olympic Medals API

![paris-2024](https://i.imgur.com/mXgb71e.png)

An **unofficial** API for the Paris 2024 summer olympics medal tally. [Data scraped from Olympic site](https://olympics.com/en/paris-2024/medals)

Hosted at https://api.olympics.kevle.xyz/

Or deploy yourself:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkevle1%2Fparis-2024-olympic-api)

## Usage

GET [/medals](https://api.olympics.kevle.xyz/medals)

Note: Limited to the top 19 countries by default if `all` flag not set [see issue #2](https://github.com/kevle1/paris-2024-olympic-api/issues/2)

Query parameters:

- `country` str (Optional)
  - Query medals for a specific country using an [IOC NOC country code](https://en.wikipedia.org/wiki/List_of_IOC_country_codes#Current_NOCs)
  - Returns an empty list if NOC does not exist or have any medals yet
  - Example [/medals?country=AUS](https://api.olympics.kevle.xyz/medals?country=aus)
  - If country is not returned despite being in the medals tally, try set below flag
- `all` bool (Optional, default false)
  - Returns all results by using a headless browser at the cost of being much slower
  - Examples:
    - [/medals?all=true](https://api.olympics.kevle.xyz/medals?all=true)
    - [/medals?country=esp&all=true](https://api.olympics.kevle.xyzmedals?country=esp&all=true)

### Example Response

```json
{
  "last_updated": "2024-07-28T06:28:31+00:00",
  "results": [
    {
      "country": {
        "code": "AUS",
        "name": "Australia"
      },
      "medals": {
        "bronze": 0,
        "gold": 3,
        "silver": 2,
        "total": 5
      },
      "rank": 1
    },
    {
      "country": {
        "code": "CHN",
        "name": "People's Republic of China"
      },
      "medals": {
        "bronze": 1,
        "gold": 2,
        "silver": 0,
        "total": 3
      },
      "rank": 2
    },
    {
      "country": {
        "code": "USA",
        "name": "United States of America"
      },
      "medals": {
        "bronze": 2,
        "gold": 1,
        "silver": 2,
        "total": 5
      },
      "rank": 3
    },
    {
      "country": {
        "code": "FRA",
        "name": "France"
      },
      "medals": {
        "bronze": 1,
        "gold": 1,
        "silver": 2,
        "total": 4
      },
      "rank": 4
    }
  ]
}
```

## Copyright

All trademarks, data, and other relevant properties are the copyright and property of the International Olympic Committee (IOC).