def input2db(requestedInput, database):
    cur = database.connection.cursor()
    columns = []
    # loop through all fetched inputs and insert into appropriate db table
    GeoName = requestedInput['GeoName']
    cur.execute("INSERT IGNORE INTO Geo(GeoName) VALUES(%s)", [GeoName])
    database.connection.commit()
    cur.close()
    print(GeoName + ' is created.')
