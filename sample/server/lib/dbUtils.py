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
        Airports[GeoName] = list(cur.fetchall())
    # print(Airports)  # debugging
    cur.close()
    for _, AirportList in Airports.items():
        for i in range(len(AirportList)):
            AirportList[i] = AirportList[i][0]  # unwrap
    return Airports


def gatherEntries(database):
    Entries = {}
    cur = database.connection.cursor()
    # find all airport for which we want to list out their entries
    cur.execute("SELECT Airport_id, Name FROM Ports")
    Airport_id_list = cur.fetchall()
    for Airport_id, Name in Airport_id_list:
        select_stmt = "SELECT DISTINCT flight_id FROM Entries WHERE linked_from = %(Airport_id)s"
        cur.execute(select_stmt, {'Airport_id': Airport_id})
        Entries[Name] = list(cur.fetchall())
    # print(Entries)  # debugging
    cur.close()
    for _, EntryList in Entries.items():
        for i in range(len(EntryList)):
            EntryList[i] = EntryList[i][0]  # unwrap
    return Entries


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
        # gather entries associated with the fetched airport Names
        Entries = gatherEntries(database)
    else:
        AirportData = [['-']*5]  # empty db
        # Entries = [['-']]
    cur.close()
    EntryData = {}
    return EntryData, AirportData, GeoData, Airports, Entries
