# inputs: waypoint db, geo db
# outputs: path objects (for plotting and manipulating)


# Input databases:
# ----------------------------
class Geo:
    def __init__(self, airports=[], time=24*60*60):
        self.time = time  # time in seconds
        self.airports = airports  # lists of Airport objects
        # diagnostics:
        self.covered = 0  # percentage of geo surveyed per day


class Port:
    def __init__(self, name=None, loc=(0, 0), capacity=10, tolerance=60, entries=[]):
        self.name = name
        self.x, self.y = loc
        self.capacity = capacity
        self.tolerance = tolerance
        self._process_entries(entries)

    def _process_entries(self, entries):
        entries = sorted(entries, key=lambda x: x.time)  # sort entries by time
        flights = {}  # dictionary of flights
        for i in entries:
            flight_number = i.flight
            if flight_number not in flights:
                flights[flight_number] = True
            if len(flights) > self.capacity:
                print('Port at capacity.')
                break
        self.entries = entries


class PortEntry:  # an entry into an airport schedule
    def __init__(self, flight=None, time=None, entry_type='dep', linked_to=None):
        self.flight = flight
        self.time = self.parse_time(time)
        self.entry_type = entry_type
        self.linked = linked_to  # Port object

    @staticmethod
    def parse_time(time):
        # work in progress... parses time input into something we can play with
        # maybe turns form input into seconds elapsed?
        return time


# Generated classes:
# ----------------------------
# find all the unique flights and store them in a dictionary
class Path:
    def __init__(self, name=None, geo=None, resolution=100):
        self.name = name  # signifies which flight number this is
        self.geo = geo  # geo object will be processed to form paths
        self._find_endpoints()  # creates list of (x, y, t) endpoints
        # interpolates endpoints to create nodes
        self._create_nodes(resolution)

    def _find_endpoints(self):
        # crawl for all mentions of this flight number
        mentions = []
        for port in self.geo:
            for entry in port.entries:
                if entry.flight == self.name:
                    mentions.append((port.x, port.y, entry.time))
        self.endpoints = sorted(mentions, key=lambda x: x[2])  # sort by time
        first_seen = self.endpoints[0]
        last_seen = self.endpoints[-1]
        first_endpoint = (first_seen[0], first_seen[1], 0)
        last_endpoint = (last_seen[0], last_seen[1], self.geo.time)
        self.endpoints = first_endpoint + self.endpoints + \
            last_endpoint  # this ensures that path is of geo.time height

    def _create_nodes(self, resolution):
        # work in progress...
        return self.name
