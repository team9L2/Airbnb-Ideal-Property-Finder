import mysql.connector

def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="kolachampagne",
        database="mydatabase"
    )

    print(mydb)

    mycursor = mydb.cursor()

    try:
        mycursor.execute("CREATE DATABASE mydatabase")
    except mysql.connector.errors.DatabaseError as e:
        print(e)

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        print(x)

    try:
        mycursor.execute(
            "DROP TABLE customers")
    except mysql.connector.errors.ProgrammingError as e:
        print(e)

    # mycursor.execute("SHOW TABLES")
    #
    # for x in mycursor:
    #     print(x)

    try:
        mycursor.execute(
            "CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
    except mysql.connector.errors.ProgrammingError as e:
        print(e)

    try:
        mycursor.execute(
            "ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
    except mysql.connector.errors.ProgrammingError as e:
        print(e)

    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = ("John", "Highway 21")
    mycursor.execute(sql, val)

    mydb.commit()

    mycursor.execute("SELECT * FROM customers")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

    sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
    val = [
        ('Peter', 'Lowstreet 4'),
        ('Amy', 'Apple st 652'),
        ('Hannah', 'Mountain 21'),
        ('Michael', 'Valley 345'),
        ('Sandy', 'Ocean blvd 2'),
        ('Betty', 'Green Grass 1'),
        ('Richard', 'Sky st 331'),
        ('Susan', 'One way 98'),
        ('Vicky', 'Yellow Garden 2'),
        ('Ben', 'Park Lane 38'),
        ('William', 'Central st 954'),
        ('Chuck', 'Main Road 989'),
        ('Viola', 'Sideway 1633')
    ]

    mycursor.executemany(sql, val)

    mydb.commit()

if __name__ == "__main__":
    main()
