# Airbnb-Ideal-Property-Finder
This program determines the attributes that make a property the most profitable to rent out on Airbnb.
Start the program by running a MySQL server locally and then running start_analysis.py.

## Tools used:
* Python 3
* MySQL
* Matplotlib
* LaTeX (for generating the report PDF)

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

## Requirements for running
* You must have an instance of MySQL running locally on your machine before you launch the program. See https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html
* Please ensure you have Python 3.7 installed.
* Please ensure you have a LaTeX builder installed on your computer for report generation. For Windows, see https://miktex.org/
* Python packages: numpy, matplotlib, mysql-connector

## If I had more data...
If I could obtain more data, I would try to obtain what type of property each listing is (for the purpose of determining which New York tax code it falls under). I would also use utility prices per district to more accurately determine the cost of operating the property.

## Future Features
With more time, here is what I would change:
* clean up the code by seperating functions
* commenting more of the code
* get rid of warnings in console output

