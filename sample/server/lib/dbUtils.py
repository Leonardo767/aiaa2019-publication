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
    cur.execute("SELECT Geo_id, GeoName FROM Geo")
    geo_id_list = cur.fetchall()
    for Geo_id, GeoName in geo_id_list:
        select_stmt = "SELECT Name FROM Ports WHERE geo_id = %(geo_id)s"
        cur.execute(select_stmt, {'geo_id': Geo_id})
        Airports[GeoName] = cur.fetchall()
    print(Airports)  # debugging
    return Airports


def informSelection(database):
    cur = database.connection.cursor()
    resultValue = cur.execute("SELECT * FROM Geo")
    if resultValue > 0:
        # GeoData fetched from db to inform selection
        GeoData = cur.fetchall()
        # gather airports associated with the fetched GeoNames
        Airports = gatherAirports(database)
    else:
        GeoData = [['-']*5]  # empty db
        Airports = [['-']]
    resultValue = cur.execute("SELECT * FROM Ports")
    if resultValue > 0:
        # AirportData fetched from db to inform selection
        AirportData = cur.fetchall()
        # gather entries associated with the fetched GeoNames
        # Entries = gatherAirports(database)
    else:
        AirportData = [['-']*5]  # empty db
        # Entries = [['-']]
    cur.close()
    EntryData = {}
    Entries = {}
    return EntryData, AirportData, GeoData, Airports, Entries
