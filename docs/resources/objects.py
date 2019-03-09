# fixed objects
# ========================================================
class Geo:
    def __init__(self, dims=(10,10), time=24*60*60):
        self.time = time  # time in seconds
        self.xlen = dims[0]
        self.ylen = dims[1]
        self.covered = 0  # percentage of geo surveyed per day
        self.airports = []  # lists of Airport objects


class Port:
    def __init__(self, capacity=10, init_drones=[]):
        self.fleet = [None]*capacity  # list of Drone Objects
        self.capacity = capacity
        self.add_drones(init_drones)

    def add_drones(self, drone_list):
        if not type(drone_list) == list:  # if input is a single drone object
            drone_list = [drone_list]
        slot = 0  # next empty slot
        while self.fleet[slot] is not None:
            slot += 1
            if slot >= self.capacity:
                print('Cannot add drone. Port at capacity.')  # we should add str rep of drone/port classes later
                return
        for i in drone_list:
            if slot >= self.capacity:
                print('Cannot add drone. Port at capacity.')  # we should add str rep of drone/port classes later
                return
            self.fleet[slot] = i  # adding drone to next empty slot
            slot += 1


# moving objects
# ========================================================
class Drone:
    def __init__(self, paths=[]):
        self.paths = paths  # list of Path objects (we should start out with 1 path per drone)


class Sheep:
    def __init__(self, id=None, simpath=None):
        self.id = id  # identifier
        self.simpath = simpath  # path object


# path types
# ========================================================
class Path:
    def __init__(self, owner=None, startPoint=(0,0,0), endPoint=(0,0,0)):
        self.owner = owner  # drone which owner is associated to
        self.nodes = self._create_nodes(startPoint, endPoint, nodes=100)

    def _create_nodes(self, sP, eP, nodes=100):
        # incomplete, but I plan to use this private function to create the mutable nodes for optimization
        nodes = 100
        return nodes


class SimPath:
    def __init__(self, owner=None, base_behavior=[], variability=0):
        self.owner = owner
        self.base_behavior = base_behavior  # 3 x T path matrix
        self.variability = variability  # standard deviation from base behavior


# abstract groups
# ========================================================
class Fleet:
    def __init__(self, drones=[]):
        self.drones = drones  # list of Drone objects


class Flock:
    def __init__(self, pops=[]):
        self.pops = pops  # list of Subject objects
