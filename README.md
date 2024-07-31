# Paris 2024 Olympic Medals API

![paris-2024](https://i.imgur.com/mXgb71e.png)

An **unofficial** API for the Paris 2024 summer olympics medal tally.

Hosted at https://api.olympics.kevle.xyz/

Or deploy yourself:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fkevle1%2Fparis-2024-olympic-api)

## Usage

### GET [/medals](https://api.olympics.kevle.xyz/medals)

- Returns medals for countries using the [**Olympic** data endpoint](https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json).

#### Query parameters:

- `country` str (Optional)
  - Query medals for a specific country using an [IOC NOC country code](https://en.wikipedia.org/wiki/List_of_IOC_country_codes#Current_NOCs)
  - Returns an empty list if NOC does not exist or have any medals yet
  - Example [/medals?country=aus](https://api.olympics.kevle.xyz/medals?country=aus)

#### Example Response

```json
{
  "last_updated": "2024-07-28T06:28:31+00:00",
  "length": 4,
  "results": [
    {
      "country": {
        "code": "AUS",
        "iso_alpha_2": "AU",
        "iso_alpha_3": "AUS",
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
        "iso_alpha_2": "CN",
        "iso_alpha_3": "CHN",
        "name": "China"
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
        "iso_alpha_2": "US",
        "iso_alpha_3": "USA",
        "name": "United States"
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
        "iso_alpha_2": "FR",
        "iso_alpha_3": "FRA",
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