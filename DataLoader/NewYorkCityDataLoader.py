from datetime import date, datetime

from DataLoader.DataLoader import DataLoader
from Dataset.Dataset import Dataset
import csv
import mysql.connector

class NewYorkCityDataLoader(DataLoader):
    def __init__(self):
        super().__init__()

    def load(self, path: str, dataset: Dataset) -> bool:
        toInsert = []

        with open(f"{path}/AB_NYC_2019.csv", encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            count = 0
            first = True

            for row in reader:
                if first:
                    first = False
                    continue

                # "neighbourhood_group" is not part of our schema, but city is,
                # so we replace it.
                row[4] = "New York City"

                # Convert to the correct types:
                row[2] = int(row[2])
                row[6] = float(row[6])
                row[7] = float(row[7])
                row[9] = int(row[9])
                row[10] = int(row[10])
                row[11] = int(row[11])

                if row[12] != "":
                    row[12] = datetime.strptime(row[12], '%Y-%m-%d').date()
                else:
                    row[12] = None

                row[13] = float(row[13]) if row[13] != "" else None
                row[14] = int(row[14]) if row[14] != "" else None
                row[15] = int(row[15]) if row[15] != "" else None
                # drop "id" because our table has an auto_increment id
                row.pop(0)

                count += 1
                toInsert.append(row)

        sql = (
            f"INSERT INTO {Dataset.GENERAL_TABLE_NAME}"
            + " (name, host_id, host_name,"
            " city, neighbourhood, latitude, longitude, room_type, price,"
            " minimum_nights, number_of_reviews, last_review, reviews_per_month, "
            " calculated_host_listings_count, availability_365) VALUES (%s, %s,"
            " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        cursor = dataset.database.cursor()

        for entry in toInsert:
            try:
                cursor.execute(sql, entry)
            except mysql.connector.errors.IntegrityError as e:
                # We have a duplicate. That's okay.
                pass

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
            data = ["New York City"]
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
