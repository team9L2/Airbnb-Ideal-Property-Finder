# Airbnb-Ideal-Property-Finder
This program determines the attributes that make a property the most profitable to rent out on Airbnb.

## Tools used:
* Python 3
* MySQL
* Matplotlib

## Detailed Introduction
This program allows a user to select multiple cities and the number of days in the year the user will rent out their property for. The program will then compare existing Airbnb listings and determine which neighbourhood provides the best profit. The profit formula is as follows:

profit = price * days_available - sale_value * tax_rate - utilities

where price is the price of the listing, days_available is the number of days for which the listing is rented out, sale_value is the value of the property (equal to the average value of its neighbourhood), tax_rate is the annual property tax (equal to the average tax rate for a residence in the city) and utilities is the cost of utilities (electricity, heating, water and garbage).

## Datasets:
You can add your own datasets for a city into the program. However, two datasets are included:
### New York
* Main: https://www.kaggle.com/dgomonov/new-york-city-airbnb-open-data#AB_NYC_2019.csv
* Neighbourhood pricing: https://www.yourlawyer.com/library/nyc-housing-prices-by-borough-and-neighborhood/
* Utilities pricing: https://patch.com/new-york/larchmont/here-s-how-much-utilities-cost-new-york-residents
* Property tax rates: https://www1.nyc.gov/site/finance/taxes/property-tax-rates.page
### Boston
* Main: https://www.kaggle.com/airbnb/boston#listings.csv
* Neighbourhood pricing: https://www.neighborhoodscout.com/ma/boston
* Utilities pricing: https://smartasset.com/mortgage/the-cost-of-living-in-boston
* Property tax rates: https://www.boston.gov/departments/assessing/how-we-tax-your-property

## Output
The program outputs a report PDF, which outlines the findings of the program. All plots used in the pdf can be found in the figures folder.

## MySQL
You must have an instance of MySQL running locally on your machine before you launch the program. See https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html
