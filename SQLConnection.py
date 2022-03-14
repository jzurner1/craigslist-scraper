import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="personal"
)

mycursor = db.cursor()


# --------------- MANIPULATING ---------------

# if you look up a car, it will show the first match's id in the table. If no matches, returns -1
def findIDInTable(table, columns, values):
    arguments = []
    for i in range(len(columns)):
        arguments.append("=")
    raw = searchCars(table, columns, arguments, values)
    try:
        return raw[0][0]
    except:
        return -1

# add a car to the table after you know the information
# only adds the car if there is no matching car
# PUT QUOTES AROUND STRINGS (title, location, link)
def addCar(title, price, mileage, isManual, location, link, datePosted):
    # sql = "insert into cars(title, price, mileage, isManual, location) values(%s, %d, %d, %d, %s)"
    # val = (title, price, mileage, isManual, location, link)
    sql2 = "insert into cars(title, price, mileage, isManual, location, datePosted) values("+title+", "+str(price)+", "+str(mileage)+", "+str(isManual)+", "+location+", "+datePosted+")"

    isPresent = findIDInTable("cars", ["title", "price", "mileage", "isManual", "location"], [title, price, mileage, isManual, location])
    if isPresent == -1:
        mycursor.execute(sql2)
        db.commit()
    else:
        print("Already in table at ID number " + str(isPresent))

# --------------- RETRIEVING ---------------

# returns data that matches the query in a table
# data like (cars ["mileage", "title"], [">=", "includes"], [100001, "'corvette'"]) PUT QUOTES AROUND STRINGS
def searchCars(table, columns, argument, data):
    query = "select * from " + table + " where "

    for i in range(len(columns)):

        # such as "mileage > 100"
        if argument[i] != "includes":
            # print(columns[i], argument[i], data[i])
            query += columns[i] + argument[i] + str(data[i])
            if i != len(columns) - 1:
                query += " and "

        # such as "title includes corvette"
        elif argument[i] == "includes":
            query += columns[i] + " like '%" + data[i] + "%'"
            if i != len(columns) - 1:
                query += " and "

    # print(query)
    mycursor.execute(query)

    returnVals = []

    for x in mycursor:
        returnVals.append(x)
    return returnVals


print(addCar("'test5'", 123, 1234, 1, "'test3'", "''", "'1/2'"))
