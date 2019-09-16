from collections import defaultdict

class Bus(object):
    """Bus Class ..."""
    
    def __init__(self, bus_id, stop_num):
        self.bus_id = bus_id   # int
        self.loc = 0.0
        self.trajectories = defaultdict(float)
        self.is_running = True
        # None means not at the stop
        self.current_stop = None
        self.holding_time = None

        # arrival times at each stop
        self.arr_times = defaultdict(float)
        # previous arrival times at each stops
        self.prev_arr_times = defaultdict(float)

        self.travel_speed_this_link = None

    def get_obs(self):
        pass

if __name__ == "__main__":
    pass
    # 1. 
    # def set_loc(a, bus):
    #     bus.loc = a
    # bus = Bus(15)
    # print(bus.loc)
    # set_loc(100, bus)
    # print(bus.loc)

    # buses = [Bus(15), Bus(20)]
    # print(buses)
    # for bus in buses:
    #     set_loc(100, bus)
    # for bus in buses:
    #     print(bus.loc)

    # 2. 
    # a = [3,4,5]
    # b = [x for x in a if x > 100]
    # assert b == []

    # 3.     