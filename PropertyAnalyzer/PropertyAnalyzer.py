import mysql.connector

from Dataset.Dataset import Dataset


class PropertyAnalyzer:
    def __init__(self):
        pass

    def getHighestYearlyProfitProperties(self, dataset: Dataset, numberOfDaysRented: int):
        cursor = dataset.database.cursor()

        try:
            cursor.execute("DROP TABLE listings_short;")
        except mysql.connector.errors.DatabaseError as e:
            # The database does not exist. That is okay.
            pass

        dataset.database.commit()

        try:
            cursor.execute("DROP TABLE x;")
        except mysql.connector.errors.DatabaseError as e:
            # The database does not exist. That is okay.
            pass

        dataset.database.commit()

        try:
            cursor.execute("DROP TABLE profits;")
        except mysql.connector.errors.DatabaseError as e:
            # The database does not exist. That is okay.
            pass

        dataset.database.commit()

        try:
            cursor.execute("DROP TABLE profits_stats;")
        except mysql.connector.errors.DatabaseError as e:
            # The database does not exist. That is okay.
            pass

        try:
            cursor.execute("DROP TABLE filtered_profits_stats;")
        except mysql.connector.errors.DatabaseError as e:
            # The database does not exist. That is okay.
            pass


        try:
            cursor.execute("DROP TABLE property_to_buy;")
        except mysql.connector.errors.DatabaseError as e:
            # The database does not exist. That is okay.
            pass

        dataset.database.commit()

        cursor.execute("create table listings_short as select id, city, price, neighbourhood from listings;")
        dataset.database.commit()

        cursor.execute("create table x as select listings_short.id, listings_short.city, price, listings_short.neighbourhood, sale_value from listings_short, neighbourhoods where listings_short.city = neighbourhoods.city and listings_short.neighbourhood = neighbourhoods.neighbourhood;")
        dataset.database.commit()

        cursor.execute(
            f"create table profits as select x.id, city, neighbourhood, price * {numberOfDaysRented} - sale_value * tax_rate - utilities as yearly_profit, price from x, CityCosts where x.city = CityCosts.name;"
        )

        dataset.database.commit()

        cursor.execute("create table property_to_buy as select id, city, yearly_profit, price from profits where yearly_profit in (select MAX(yearly_profit) FROM profits);")
        dataset.database.commit()

        cursor.execute("select * from listings where id in (select id from property_to_buy);")
        best_listing = cursor.fetchall()

        cursor.execute("select yearly_profit from property_to_buy;")
        best_listing_profit = cursor.fetchall()

        cursor.execute("create table profits_stats as select city, neighbourhood, avg(yearly_profit) as avg_profit, max(yearly_profit) as max_profit, min(yearly_profit) as min_profit, count(*) as n from profits group by city, neighbourhood;")
        dataset.database.commit()

        cursor.execute("create table filtered_profits_stats as select * from profits_stats where n > 3;")
        dataset.database.commit()

        cursor.execute("select * from profits_stats;")
        listing_stats = cursor.fetchall()

        cursor.execute("select * from profits_stats where avg_profit in (select max(avg_profit) from filtered_profits_stats);")
        best_neighbourhood = cursor.fetchall()

        return best_listing[0], best_listing_profit[0][0], listing_stats, best_neighbourhood[0]

    def getQuickestROIProperties(self, dataset: Dataset, numberOfDaysRented: int):
        # Planned for the future
        pass
