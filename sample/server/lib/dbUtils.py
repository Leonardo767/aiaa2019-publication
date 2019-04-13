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
    cur.close()
    for _, AirportList in Airports.items():
        for i in range(len(AirportList)):
            AirportList[i] = AirportList[i][0]  # unwrap
    # print(Airports)  # debugging
    return Airports


def gatherEntries(database):
    Entries = {}
    cur = database.connection.cursor()
    # find all airport for which we want to list out their entries
    cur.execute("SELECT Airport_id, Name FROM Ports")
    Airport_id_list = cur.fetchall()
    for Airport_id, Name in Airport_id_list:
        select_stmt = "SELECT DISTINCT flight_id FROM Entries WHERE linked_from=%(Airport_id)s"
        cur.execute(select_stmt, {'Airport_id': Airport_id})
        Entries[Name] = list(cur.fetchall())
    # print(Entries)  # debugging
    cur.close()
    for _, EntryList in Entries.items():
        for i in range(len(EntryList)):
            EntryList[i] = EntryList[i][0]  # unwrap
    return Entries


def gather_sim_points(database, object_id):
    cur = database.connection.cursor()
    select_stmt = "SELECT * FROM SimPoints WHERE SimObject_id=%(SimObject_id)s"
    cur.execute(select_stmt, {'SimObject_id': object_id})
    sim_points_data = cur.fetchall()
    # print(sim_points_data)  # debugging
    # save sim_points as [x, y, t]
    sim_points = []
    for sim_point in range(len(sim_points_data)):
        sim_points.append([sim_points_data[sim_point][2],
                           sim_points_data[sim_point][3], sim_points_data[sim_point][4]])
    cur.close()
    return sim_points


def informGeoSelection(database):
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


def informSimSelection(database):
    cur = database.connection.cursor()
    resultValue = cur.execute("SELECT * FROM SimSuites")
    if resultValue > 0:
        SuiteData = cur.fetchall()
        print(SuiteData)
    return SuiteData


def save_settings(database, changed, value, current_card=1):
    cur = database.connection.cursor()
    # NOTE: update_stmt is subject to SQL injection attacks due to using .format()
    update_stmt = "UPDATE settings SET {}='{}' WHERE load_card={}".format(
        changed, value, current_card)
    cur.execute(update_stmt)
    database.connection.commit()
    cur.close()


def extract_selection(database, called, load_card=1, all_settings=False):
    cur = database.connection.cursor()
    if all_settings:
        called = '*'
    select_stmt = "SELECT {} FROM Settings".format(called)
    cur.execute(select_stmt)
    # settings_all used in function, all_settings used as outside parameter
    settings_all = cur.fetchall()
    if all_settings:
        selection = settings_all
    else:
        selection = settings_all[0][0]
    # print('SELECTION:', selection, ' OF ', called)  # debugging
    cur.close()
    return selection


def load_settings(database, load_card=1):
    return


def get_geo_info(database, selection="DFW"):
    cur = database.connection.cursor()
    select_stmt = "SELECT * FROM Geo WHERE GeoName=%(GeoName)s"
    cur.execute(select_stmt, {"GeoName": selection})
    geo_data = cur.fetchall()
    geo_info = {}
    geo_info["dims"] = (geo_data[0][1], geo_data[0][2])
    geo_info["timespan"] = geo_data[0][3]
    # print(geo_info)
    airport_name_list = gatherAirports(database)[selection]
    airport_info = {}
    for airport_name in airport_name_list:
        select_stmt = "SELECT * FROM Ports WHERE Name=%(Name)s"
        cur.execute(select_stmt, {"Name": airport_name})
        airport_data = cur.fetchall()
        airport_info[airport_name] = [
            (airport_data[0][1], airport_data[0][2]), airport_data[0][3]]
    # print(airport_info)
    cur.close()
    return geo_info, airport_info


def get_sim_info(database, selection="sim1"):
    cur = database.connection.cursor()
    select_stmt = "SELECT SimSuite_id FROM SimSuites WHERE Suite_Name=%(Suite_Name)s"
    cur.execute(select_stmt, {"Suite_Name": selection})
    selection_id = cur.fetchall()
    select_stmt = "SELECT * FROM SimObjects WHERE SimSuite_id=%(SimSuite_id)s"
    cur.execute(select_stmt, {"SimSuite_id": selection_id})
    sim_objects = cur.fetchall()
    # print(sim_objects)  # debugging
    sim_info = {}
    sim_info_style = {}
    for sim_object in sim_objects:
        # storing in dict keyed by object names, store an object's path points
        # sim_object = (SimObject_id, SimSuite_id, object_name, object_style)
        sim_info[sim_object[2]] = gather_sim_points(database, sim_object[0])
        # store styling parameter which allows for basic control over visualization
        sim_info_style[sim_object[2]] = sim_object[3]
    # print(sim_info)  # debugging
    # print(sim_info_style)  # debugging
    cur.close()
    print(sim_info)
    return sim_info, sim_info_style
