import numpy as np
from collections import defaultdict

class Stop:
    def __init__(self, stop_id, loc, demand_rate, board_rate):
        """Init method.

        init method for Link 

        Args:
        loc: bus stop loc
        demand_rate: pax arrival rate, pax/sec
        board_rate: pax boarding rate, pax/sec
        next_link: next link object

        Returns:
            
        """

        # unchangable ...
        self.stop_id = stop_id
        self._loc = loc
        self._demand_rate = demand_rate
        self._board_rate = board_rate
        self._next_link = None

        # changable ...
        self._pax_queue = 0
        self._bus_list = []
        # self.last_bus_arr = defaultdict(lambda: 0.0) # bus_id -> arrival time
        self.last_bus_arr = 0.0

        # stats
        self.arr_times = []
        self.dpt_times = []

    def __call__(self, next_link):
        self._next_link = next_link

    def enter_bus(self, bus, curr_time):
        # print(self.stop_id, bus)
        bus.loc = self._loc
        if self.last_bus_arr != 0.0: # at least one bus has ever reached this stop
            bus.prev_arr_times[self.stop_id] = self.last_bus_arr
        else:
            bus.prev_arr_times[self.stop_id] = 0.0
        
        self.last_bus_arr = curr_time
        self._bus_list.append(bus)
        if len(self._bus_list) >= 2: # bunched!
            return True
        self.arr_times.append(curr_time)
        # if self.stop_id == 4:
        #     print(self.arr_times)


    def operation(self, delta_t, curr_time):
        self._pax_arrive()
        self._boarding(delta_t)
        self._leaving(curr_time)

    def _pax_arrive(self):
        self._pax_queue += np.random.poisson(self._demand_rate)

    def _boarding(self, delta_t):
        for bus in self._bus_list:
            self._pax_queue -= self._board_rate*delta_t

    def _leaving(self, curr_time):
        for bus in self._bus_list:
            if self._pax_queue <= 0:
                if self._next_link:
                    self._next_link.enter_bus(bus, 0)
                else: # finished
                    bus.is_running = False
                self._bus_list = []
            else: # still serving, record the "constant" trajectory
                bus.trajectories[curr_time] = bus.loc


    def reset(self):
        self._bus_list = []
        self._pax_queue = 0
        # stats
        self.arr_times = []
        self.dpt_times = []
        self.last_bus_arr = 0.0