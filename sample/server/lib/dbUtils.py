def input2db_geo(requestedInput, database):
    cur = database.connection.cursor()
    # loop through all fetched inputs and insert into appropriate db table
    insert_stmt = (
        "INSERT INTO Geo (GeoName, DimX, DimY, TimeLength) "
        "VALUES (%s, %s, %s, %s)"
    )
    data = (requestedInput['GeoName'], requestedInput['DimX'],
            requestedInput['DimY'], requestedInput['TimeLength'])
    cur.execute(insert_stmt, data)
    database.connection.commit()
    cur.close()


def gatherAirports(database):
    Airports = {}
    cur = database.connection.cursor()
    # find all geo for which we want to list out their airports
    resultValue = cur.execute("SELECT Geo_id FROM Geo")
    if resultValue > 0:
        geo_id_list = cur.fetchall()
        for geo_id in geo_id_list:
            select_stmt = "SELECT * FROM Ports WHERE geo_id = %(geo_id)s"
            cur.execute(select_stmt, {'geo_id': geo_id})
            Airports[geo_id] = cur.fetchall()
            print(Airports)  # debugging
    else:
        return [['-']]
    return Airports
