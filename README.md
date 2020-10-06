# Uttar Pradesh Fiscal Data Backend

A data scraping pipeline was setup to mine relevant data and sources from the Uttar Pradesh fiscal data portal, [Koshvani](http://koshvani.up.nic.in/).

## Table of Contents

[Platform]()

[Tools]()

[Setup]()

[Challenges]()

[Contributions](https://github.com/CivicDataLab/up-fiscal-data-backend#contributions)

[Repo Structure](https://github.com/CivicDataLab/up-fiscal-data-backend#repo-structure)

## Platform

**Platfrom Name** : Koshvani web -- A Gateway to Finance Activities in the State of Uttar Pradesh
**Platform URL** : http://koshvani.up.nic.in/

A more detailed analysis of the platform and in-scope data can be found [here](https://github.com/CivicDataLab/up-fiscal-data/blob/master/01-data-scoping/budget-portal.md).

## Tool

Though the data on the Koshvani platform is available in structured format to us and analyse, scraping it through traditional methods was turning out to be a challenge.

Keeping in mind the platform structure and behaviour, a [decision](https://github.com/CivicDataLab/up-fiscal-data/blob/master/00-docs/decisions/003-selnium.md) was undertaken to select [Selenium](https://www.selenium.dev/) as the mode of data mining and storing. The Selenium framework allows to automate browser actions to extract in-scope datasets.

## Setup

Instructions for setting up the data pipeline.

`<<TBD>>`

## Challenges

During the data scraping exercise, the following challenges were faced during mining of the data. The respective resolutions for those challeges are also documented here.

| Challenge | Resolution |
|---|---|
|   |   |
|   |   |
|   |   |

## Contributions

You can refer to the [contributing guidelines](https://github.com/CivicDataLab/up-fiscal-data-backend/blob/master/contribute/CONTRIBUTING.md) and understand how to contribute.

## Repo Structure

```
root
└── contribute/
    └── CODE-OF-CONDUCT.md
    └── CONTRIBUTING.md
└── LICENSE.md
└── README.md
```
