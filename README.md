# Paris 2024 Olympic Medals API

![paris-2024](https://i.imgur.com/mXgb71e.png)

An **unofficial** API for the Paris 2024 summer olympics medal tally. [Data source](https://olympics.com/en/paris-2024/medals)

Hosted at https://api.olympics.kevle.xyz/

Or deploy yourself:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkevle1%2Fparis-2024-olympic-api)

## Usage

GET [/medals](https://api.olympics.kevle.xyz/medals)

Query parameters:

- `country` (Optional)
  - Query medals for a specific country using an [IOC NOC code](https://en.wikipedia.org/wiki/List_of_IOC_country_codes#Current_NOCs)
  - Returns an empty list if NOC does not exist or have any medals yet

### Example Response

```json
{
  "last_updated": "2024-07-27T14:13:22+00:00",
  "results": [
    {
      "country": {
        "code": "CHN",
        "name": "People's Republic of China"
      },
      "medals": {
        "bronze": 0,
        "gold": 2,
        "silver": 0,
        "total": 2
      },
      "rank": 1
    },
    {
      "country": {
        "code": "AUS",
        "name": "Australia"
      },
      "medals": {
        "bronze": 0,
        "gold": 1,
        "silver": 0,
        "total": 1
      },
      "rank": 2
    },
    {
      "country": {
        "code": "GBR",
        "name": "Great Britain"
      },
      "medals": {
        "bronze": 1,
        "gold": 0,
        "silver": 1,
        "total": 2
      },
      "rank": 3
    }
  ]
}
```

## Copyright

All trademarks, data, and other relevant properties are the copyright and property of the International Olympic Committee (IOC).