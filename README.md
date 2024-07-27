# Paris 2024 Olympic Medals API

![paris-2024](https://i.imgur.com/mXgb71e.png)

An **unofficial** API for the Paris 2024 summer olympics medal tally. [Data source](https://olympics.com/en/paris-2024/medals)

Hosted at https://api.olympics.kevle.xyz/

Or deploy yourself:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkevle1%2Fparis-2024-olympic-api)

## Usage

GET [/medals](https://api.olympics.kevle.xyz/medals)

- `country` (Optional)
  - Query medals for a specific country using an [alpha 3 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#Current_codes)
  - Returns empty list if country does not exist or have any medals yet

### Example Response

```json
{
  "last_updated": "2024-07-27T11:25:10+00:00",
  "results": [
    {
      "country": {
        "code": "KOR",
        "name": "Republic of Korea"
      },
      "medals": {
        "bronze": 0,
        "gold": 0,
        "silver": 1,
        "total": 1
      }
    },
    {
      "country": {
        "code": "GBR",
        "name": "Great Britain"
      },
      "medals": {
        "bronze": 1,
        "gold": 0,
        "silver": 0,
        "total": 1
      }
    },
    {
      "country": {
        "code": "KAZ",
        "name": "Kazakhstan"
      },
      "medals": {
        "bronze": 1,
        "gold": 0,
        "silver": 0,
        "total": 1
      }
    }
  ]
}
```

## Copyright

All trademarks, data, and other relevant properties are the copyright and property of the International Olympic Committee (IOC).