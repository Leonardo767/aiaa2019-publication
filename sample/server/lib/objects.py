# Define classes
# ====================================


class Geo:
    def __init__(self, region_name=None, airports=None, dimensions=(1, 1), time=24*60*60):
        self.region_name = region_name
        if airports is not None:
            self.airports = airports  # lists of Airport objects
        else:
            self.airports = []
        self.dim_x, self.dim_y = dimensions
        self.time = self.parse_time(time)  # time in seconds
        # diagnostics:
        self.covered = 0  # percentage of geo surveyed per day

    @staticmethod
    def parse_time(time):
        return time


class Port:
    def __init__(self, name=None, loc=(0, 0), tolerance=60, entries=None):
        self.name = name  # identifier
        self.x, self.y = loc
        self.tolerance = tolerance
        if entries is not None:
            self.entries = entries  # lists of Airport objects
        else:
            self.entries = []

    def __repr__(self):
        return 'Port ' + str(self.name) + ' at ' + str(self.x) + ', ' + str(self.y)



class PortEntry:
    def __init__(self, flight=None, time=None, entry_type='dep', linked_from=None, linked_to=None):
        self.flight = flight  # identifier
        self.time = time
        self.entry_type = entry_type
        self.linked_from = linked_from
        self.linked_to = linked_to

    def __repr__(self):
        return 'Flight ' + self.flight + ' from ' + str(self.linked_from) + ' to ' + str(self.linked_to) + ' at ' + str(self.time)
