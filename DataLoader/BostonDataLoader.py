import csv
from datetime import datetime
import re

from DataLoader.DataLoader import DataLoader
from Dataset.Dataset import Dataset

import mysql.connector


class BostonDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def load(self, path: str, dataset: Dataset) -> bool:
        # We will construct two tables (because this dataset is made this way)
        # and then we will join them.
        # Table 1: A, listing_id, price, city_name
        # Table 2: listing_id, name, host_id, host_name, neighbourhood, latitude,
        # longitude, room_type, minimum_nights, number_of_reviews, last_review,
        # reviews_per_month, calculated_host_listings_count, availability_365

        table1Entries = []
        path1 = f"{path}/calendar.csv"

        with open(path1, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            first = True

            for row in reader:
                if first:
                    first = False
                    continue

                if row[3] == "":
                    # We don't want listings without prices. Otherwise, how
                    # can we determine revenue?
                    continue

                entry = [int(row[0]), float(re.sub("[^0-9.]", "", row[3])), "Boston"]
                table1Entries.append(entry)

        table2Entries = []
        path2 = f"{path}/listings.csv"

        with open(path2, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            first = True

            for row in reader:
                if first:
                    first = False
                    continue

                entry = [int(row[0]), row[4], int(row[19])]

                if row[21] != "":
                    entry.append(row[21])
                else:
                    entry.append(None)

                entry += [row[38],
                         float(row[48]), float(row[49]), row[52], int(row[68])]

                if row[76] != "":
                    entry.append(int(row[76]))
                else:
                    entry.append(None)

                if row[78] != "":
                    entry.append(datetime.strptime(row[78], '%Y-%m-%d').date())
                else:
                    entry.append(None)

                if row[94] != "":
                    entry.append(float(row[94]))
                else:
                    entry.append(None)

                if row[93] != "":
                    entry.append(int(row[93]))
                else:
                    entry.append(None)

                if row[74] != "":
                    entry.append(int(row[74]))
                else:
                    entry.append(None)

                table2Entries.append(entry)

        cursor = dataset.database.cursor()

        try:
            cursor.execute(
                "DROP TABLE Table1;")
        except mysql.connector.errors.ProgrammingError as e:
            pass

        try:
            cursor.execute(
                "DROP TABLE Table2;")
        except mysql.connector.errors.ProgrammingError as e:
            pass

        try:
            cursor.execute(
                "CREATE TABLE Table1 (listing_id INT PRIMARY KEY, price FLOAT, city VARCHAR(255));")
        except mysql.connector.errors.ProgrammingError as e:
            print(e)
            return False

        try:
            cursor.execute(
                "CREATE TABLE Table2 (listing_id INT PRIMARY KEY,"
                "name VARCHAR(255), host_id INT, host_name VARCHAR(255),"
            " neighbourhood VARCHAR(255), latitude FLOAT, longitude FLOAT,"
            " room_type VARCHAR(255), minimum_nights INT,"
            " number_of_reviews INT, last_review DATE, reviews_per_month FLOAT,"
            " calculated_host_listings_count INT, availability_365 INT);")
        except mysql.connector.errors.ProgrammingError as e:
            print(e)
            return False

        sql = "INSERT INTO Table1 (listing_id, price, city) VALUES (%s, %s," \
                                                    " %s);"

        for entry in table1Entries:
            try:
                cursor.execute(sql, tuple(entry))
            except mysql.connector.errors.IntegrityError as e:
                # We have a duplicate. That's okay.
                pass

        dataset.database.commit()

        sql = "INSERT INTO Table2 (listing_id, name, host_id, host_name," \
                                                    " neighbourhood, latitude, longitude, room_type," \
                                                    " minimum_nights, number_of_reviews, last_review, reviews_per_month, " \
                                                    " calculated_host_listings_count, availability_365) VALUES (%s, %s," \
                                                    " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        dataset.database.commit()

        for entry in table2Entries:
            try:
                cursor.execute(sql, entry)
            except mysql.connector.errors.IntegrityError as e:
                # We have a duplicate. That's okay.
                pass


        dataset.database.commit()

        sql = (
            f"INSERT INTO {Dataset.GENERAL_TABLE_NAME}"
            + " (name, host_id, host_name,"
            " city, neighbourhood, latitude, longitude, room_type, price,"
            " minimum_nights, number_of_reviews, last_review, reviews_per_month, "
            " calculated_host_listings_count, availability_365) SELECT name, host_id, host_name,"
            " city, neighbourhood, latitude, longitude, room_type, price,"
            " minimum_nights, number_of_reviews, last_review, reviews_per_month, "
            " calculated_host_listings_count, availability_365 FROM (Table1 INNER JOIN Table2 ON Table1.listing_id=Table2.listing_id);"
        )

        cursor.execute(sql)
        dataset.database.commit()

        neighbourhoods = []

        with open(f"{path}/prices.csv", encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            first = True

            for row in reader:
                if first:
                    first = False
                    continue

                neighbourhoods.append([row[0], row[1], float(row[2])])

        sql = (
            f"INSERT INTO {Dataset.NEIGHBOURHOOD_TABLE_NAME}"
            + " (city, neighbourhood, sale_value) VALUES (%s, %s,"
            " %s)"
        )

        cursor = dataset.database.cursor()

        for entry in neighbourhoods:
            try:
                cursor.execute(sql, entry)
            except mysql.connector.errors.IntegrityError as e:
                # We have a duplicate. That's okay.
                pass

        dataset.database.commit()

        with open(f"{path}/other.csv", encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            data = ["Boston"]
            first = True

            for row in reader:
                if first:
                    first = False
                    continue

                data += [float(row[0]), float(row[1])]

        sql = (
            f"INSERT INTO {Dataset.CITIES_TABLE_NAME}" + " (name, utilities,"
            " tax_rate) VALUES (%s, %s,"
            " %s)"
        )

        cursor = dataset.database.cursor()

        try:
            cursor.execute(sql, data)
        except mysql.connector.errors.IntegrityError as e:
            # We have a duplicate?! Uh oh
            return False

        dataset.database.commit()
        return True
