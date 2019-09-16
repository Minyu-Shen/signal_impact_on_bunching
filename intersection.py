class Signal(object):
    def __init__(self, signal_id, cycle_length, green_ratio, offset, start_loc):
        # unchangable ...
        self._signal_id = signal_id
        self._cycle_length = cycle_length
        self._green_ratio = green_ratio
        self._offset = offset
        self.start_loc = start_loc
        
        # changable
        self.queue = []

        # stats
        self.arr_times = []
        self.dpt_times = []


    def is_green(self, curr_t):
        if ((curr_t-self._offset) % self._cycle_length) < self._cycle_length*self._green_ratio:
            return True
        else:
            return False
    
    def enter_bus(self, bus, curr_t):
        self.arr_times.append(curr_t)
        self.queue.append(bus)

    def discharge(self, curr_t):
        discharged_buses = []
        if self.is_green(curr_t) and self.queue: # is green and has some buses return
            discharged_buses = self.queue
            for bus in discharged_buses:
                self.dpt_times.append(curr_t)
            self.queue = []
        return discharged_buses
    
    def reset(self):
        self.queue = []
        self.arr_times = []
        self.dpt_times = []