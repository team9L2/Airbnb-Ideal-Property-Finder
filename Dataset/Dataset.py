import json

import mysql.connector


class Dataset:
    database: mysql.connector.connection.MySQLConnection

    # Constants
    DATABASE_NAME = "AirbnbListings"
    GENERAL_TABLE_NAME = "Listings"
    NEIGHBOURHOOD_TABLE_NAME = "Neighbourhoods"
    CITIES_TABLE_NAME = "CityCosts"

    def __init__(self, credentialsFilePath: str):
        host, username, password = self._getCredentials(credentialsFilePath)
        self._setupConnection(host, username, password)
        self._setupDatabase()

    def _getCredentials(self, credentialsFilePath: str):
        try:
            with open(credentialsFilePath, mode='r') as file:
                data = json.load(file)
                return data["host"], data["username"], data["password"]
        except:
            raise Exception("You are missing " + credentialsFilePath + "or it "
                            "is formatted poorly. Please ask Robert (robert."
                            "ciborowski@mail.utoronto.ca) for help.")

    def _setupConnection(self, host: str, username: str, password: str):
        temporaryDatabase = mysql.connector.connect(
            host=host,
            user=username,
            password=password
        )

        cursor = temporaryDatabase.cursor()

        try:
            cursor.execute("DROP DATABASE " + self.DATABASE_NAME)
        except mysql.connector.errors.DatabaseError as e:
            # The database does not exist. That is okay.
            pass

        cursor.execute("CREATE DATABASE " + self.DATABASE_NAME)

        self.database = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database="AirbnbListings"
        )

    def _setupDatabase(self):
        cursor = self.database.cursor()
        cursor.execute(
            "CREATE TABLE " + self.GENERAL_TABLE_NAME + " (id INT AUTO_INCREMENT PRIMARY"
            " KEY, name VARCHAR(255), host_id VARCHAR(255),"
            " host_name VARCHAR(255), city VARCHAR(255),"
            " neighbourhood VARCHAR(255), latitude FLOAT, longitude FLOAT,"
            " room_type VARCHAR(255), price INT, minimum_nights INT,"
            " number_of_reviews INT, last_review DATE, reviews_per_month FLOAT,"
            " calculated_host_listings_count INT, availability_365 INT)")
        self.database.commit()

        cursor.execute(
            "CREATE TABLE " + self.NEIGHBOURHOOD_TABLE_NAME + " (city "
            "VARCHAR(255), neighbourhood VARCHAR(255), sale_value INT, "
            "PRIMARY KEY (city, neighbourhood))")
        self.database.commit()

        cursor.execute(
            "CREATE TABLE " + self.CITIES_TABLE_NAME + " (id INT AUTO_INCREMENT PRIMARY"
                                                              " KEY, name VARCHAR(255), utilities FLOAT,"
                                                              " tax_rate FLOAT)")
        self.database.commit()
