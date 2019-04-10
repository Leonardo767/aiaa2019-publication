import objects

# Module functions
# ====================================


# build geo
def build_geo(geo_data):
    geo_object = objects.Geo(
        geo_data[0], geo_data[1], geo_data[2], geo_data[3])
    return geo_object


# build airports
def build_port(port_data):
    port_object = objects.Port(
        port_data[0], port_data[1], port_data[2], port_data[3])
    return port_object


# build entries
def build_entry(entry_data):
    entry_object = objects.PortEntry(
        entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
    return entry_object


# convert airport entries into pointers to entry objects
def convert_entry_list(port, available_entries):
    entry_list = port.entries
    new_entry_list = []
    for flight_id in entry_list:
        relevant_entries = []
        for potential_entry in available_entries[flight_id]:
            if potential_entry.linked_from == port.name:
                relevant_entries.append(potential_entry)
        new_entry_list += relevant_entries
    port.entries = new_entry_list
    return port


# bring builders together
def build_all(data, geo_selection):
    """
    :param data: all databases
    :param geo_selection: specific region selected
    :return geo object, list of airport objects containing entry objects:

    Assumptions:
    -there are no outbound flights (note: this can be emulated by creating a port at the exit point in geo bounds)
    """

    # find selection
    # default geo if specified geo cannot be found
    geo_selected = build_geo(data[0][0])
    for i in range(len(data[0])):
        if data[0][i][0] == geo_selection:
            geo_selected = build_geo(data[0][i])
    # find airports in geo selected
    region_airports = geo_selected.airports
    airport_all = data[1]
    airport_used = []
    # only use airports contained within geo
    for airport_db in airport_all:
        if airport_db[0] in region_airports:
            airport_used.append(build_port(airport_db))
    # only use entries contained in airports
    flights = {}  # tally up the flights listed in used airports
    for airport in airport_used:
        for i in airport.entries:
            if i not in flights:
                flights[i] = 1
            else:
                flights[i] += 1
    entries_all = data[2]
    entries_used = {}  # dictionary with flight as key
    for entry_db in entries_all:
        if entry_db[0] in flights:
            if entry_db[0] not in entries_used:
                entries_used[entry_db[0]] = [build_entry(entry_db)]
            else:
                entries_used[entry_db[0]].append(build_entry(entry_db))
    # fix the airport entries to contain pointers to entry class objects
    # for i in airports: i.entries = [list of entry classes]  # reassign list of classes
    for i in range(len(airport_used)):
        airport_used[i] = convert_entry_list(airport_used[i], entries_used)
    # geo.airports = [list of airport classes]  # reassign list of classes
    geo_selected.airports = airport_used

    return geo_selected, airport_used, flights


# Define dummy data
# ====================================
# geo:
# [airports, dimensions, time]
db_dfw = ['dfw', ['A', 'B'], (5, 5), 3600*24]
db_love = ['love', ['C'], (2, 2), 3600*24]
db_geo = [db_dfw, db_love]


# entries (logs in the airport schedule)
# [flight number, time, departure/arrival, linking to]
a_1 = ['1', '08:00:00', 'dep', 'A', 'B']
a_2 = ['2', '10:00:00', 'dep', 'A', 'B']
a_3 = ['1', '18:10:00', 'arv', 'A', 'B']
a_4 = ['2', '21:10:00', 'arv', 'A', 'B']
b_1 = ['1', '08:10:00', 'arv', 'B', 'A']
b_2 = ['2', '10:10:00', 'arv', 'B', 'A']
b_3 = ['1', '18:00:00', 'dep', 'B', 'A']
b_4 = ['2', '21:00:00', 'dep', 'B', 'A']
c_1 = ['3', '08:10:00', 'arv', 'C', 'C']
c_2 = ['3', '10:10:00', 'dep', 'C', 'C']
c_3 = ['3', '18:00:00', 'arv', 'C', 'C']
c_4 = ['3', '21:00:00', 'dep', 'C', 'C']
# not exactly used, but is useful for creating paths
db_entries = [a_1, a_2, a_3, a_4, b_1, b_2, b_3, b_4, c_1, c_2, c_3, c_4]


# port (aka a fixed way-point):
# [name, location, tolerance, entries]
db_a = ['A', (1, 3), 0, ['1', '2']]
db_b = ['B', (3, 4), 0, ['1', '2']]
db_c = ['C', (7, 8), 0, ['3']]
db_ports = [db_a, db_b, db_c]

db_all = [db_geo, db_ports, db_entries]  # ordered by decreasing scale


# Instantiate Objects (test)
# ====================================
geo, ports, flight_count = build_all(db_all, 'dfw')

print('Region Name:', geo)
print('Airports:', geo.airports)

print('\nPorts per flight:', flight_count)
print('Ports used:\n[')
for i in geo.airports:
    print(i, ': ', i.entries)
print(']\n')
