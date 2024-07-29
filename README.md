# Paris 2024 Olympic Medals API

![paris-2024](https://i.imgur.com/mXgb71e.png)

An **unofficial** API for the Paris 2024 summer olympics medal tally.

Hosted at https://api.olympics.kevle.xyz/

Or deploy yourself:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkevle1%2Fparis-2024-olympic-api)

## Usage

GET [/medals](https://api.olympics.kevle.xyz/medals)

- Return medals for the top 19 countries from the [**Olympic** site](https://olympics.com/en/paris-2024/medals).
- [Reason for limitation](https://github.com/kevle1/paris-2024-olympic-api/issues/2#issuecomment-2254770288)

Query parameters:

- `country` str (Optional)
  - Query medals for a specific country using an [IOC NOC country code](https://en.wikipedia.org/wiki/List_of_IOC_country_codes#Current_NOCs)
  - Returns an empty list if NOC does not exist or have any medals yet
  - Note: will attempt to fallback to Wikipedia if country not found in the Olympic site results
  - Example [/medals?country=aus](https://api.olympics.kevle.xyz/medals?country=aus)

GET [/medals/all](https://api.olympics.kevle.xyz/medals/all)

- Returns medals for all countries from [the **Wikipedia** Paris 2024 Olympic medal table](https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table#Medal_table)

### Example Response

```json
{
  "last_updated": "2024-07-28T06:28:31+00:00",
  "length": 4,
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
  ],
  "source": "olympics.com"
}
```

## Copyright

All trademarks, data, and other relevant properties are the copyright and property of the International Olympic Committee (IOC).