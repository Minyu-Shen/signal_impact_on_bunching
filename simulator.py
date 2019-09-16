import numpy as np
from bus import Bus
from stop import Stop
from link import Link
from intersection import Signal
from collections import defaultdict
from copy import deepcopy
import matplotlib.pyplot as plt

class Simulator(object):
    def __init__(self, sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, \
            link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                cycle_lengths, green_ratios, signal_offsets, signal_locs):


        self._stop_locs = stop_locs
        self._demand_rates = demand_rates
        self._board_rates = board_rates
        self._link_mean_speeds = link_mean_speeds
        self._link_cv_speeds = link_cv_speeds
        self._link_lengths = link_lengths
        self._link_start_locs = link_start_locs
        self._cycle_lengths = cycle_lengths
        self._green_ratios = green_ratios
        self._signal_offsets = signal_offsets
        self._signal_locs = signal_locs
        self._stop_num = stop_num
        

        # current simulation time
        self._curr_time = 0.0
        # counting the total bus for creating bus id
        self._total_bus = 0
        # total buses for stats
        self._total_bus_list = []
        # total simulation time
        self._sim_duration = sim_duration
        # dispatch plans
        self._dspt_times = deepcopy(dspt_times)
        

        # unchangable ...
        ### init stops
        self._stop_list = []
        for index, (loc, demand_rate, self._board_rates) in \
                enumerate(zip(self._stop_locs, self._demand_rates, self._board_rates)):
            stop = Stop(index, loc, demand_rate, self._board_rates)
            self._stop_list.append(stop)
        ### init links
        self._link_list = []
        for index, (mean_speed, cv_speed, length, start_loc) in \
                enumerate(zip(self._link_mean_speeds, self._link_cv_speeds, self._link_lengths, self._link_start_locs)):
            link = Link(index, mean_speed, cv_speed, length, start_loc)
            self._link_list.append(link)
        ### init signals
        self._signal_list = []
        for index, (cycle_length, green_ratio, offset, start_loc) in \
                enumerate(zip(self._cycle_lengths, self._green_ratios, self._signal_offsets, self._signal_locs)):
            signal = Signal(index, cycle_length, green_ratio, offset, start_loc)
            self._signal_list.append(signal)

        ### connect links and signals
        for index, signal in enumerate(self._signal_list):
            for link_no, link in enumerate(self._link_list):
                if signal.start_loc > link._start_loc and signal.start_loc < link._end_loc:
                    link.add_signal(signal)
                    break

        ### connect stops and links
        for index, link in enumerate(self._link_list):
            link(self._stop_list[index])
        for index, stop in enumerate(self._stop_list):
            if index != self._stop_num-1:
                stop(self._link_list[index+1])


    def distribute_initial_buses(self):
        m = 2
        n = self._stop_num // m
        for bs in range(n-1):
            enter_link_no = (bs+1) * m
            bus = Bus(self._total_bus, self._stop_num)
            self._total_bus += 1
            self._link_list[enter_link_no].enter_bus(bus, 0)
            self._total_bus_list.append(bus)

    def dispatch(self):
        if self._dspt_times:
            if self._curr_time >= self._dspt_times[0]:
                bus = Bus(self._total_bus, self._stop_num)
                self._total_bus += 1
                self._link_list[0].enter_bus(bus, 0)
                self._dspt_times.remove(self._dspt_times[0])
                self._total_bus_list.append(bus)

    def move_one_step(self, delta_t):
        # check if dispatch bus into the first link
        self.dispatch()
        # if any bus has arrived at the stop, stop->arrived buses
        total_arrived_buses = defaultdict(lambda: list)
        if self._curr_time <= self._sim_duration:
            # do the link and stop operations sequentially
            for index, (link, stop) in enumerate(zip(self._link_list, self._stop_list)):
                # buses will enter the next stops, record the arrive time
                stop_arrived_buses, is_bunched = link.forward(delta_t, self._curr_time)
                if is_bunched:
                    return True
                for bus in stop_arrived_buses:
                    bus.arr_times[index] = self._curr_time
                stop.operation(delta_t, self._curr_time)
                if stop_arrived_buses:
                    total_arrived_buses[index] = stop_arrived_buses
            
            self._curr_time += delta_t
        
        return False
        

    def plot_time_space(self):
        # plot stops
        for stop_loc in self._stop_locs:
            plt.hlines(stop_loc, 0, self._sim_duration, linestyles='dashed', linewidth=1.0)
        # plot signals
        for index, signal_loc in enumerate(self._signal_locs):
            offset = self._signal_offsets[index]
            C = self._cycle_lengths[index]
            G = self._green_ratios[index] * self._cycle_lengths[index]
            R = C-G
            for i in range(self._sim_duration // C):
                # plot green period
                plt.hlines(signal_loc, offset+i*C, offset+i*C+G, linewidth=1.0, colors='g')
                # plot red period
                plt.hlines(signal_loc, offset+i*C+G, offset+(i+1)*C, linewidth=1.0, colors='r')


        for bus in self._total_bus_list:
            t, x = zip(*bus.trajectories.items())
            plt.plot(t, x)
        plt.show()

    def get_signal_headways(self, signal_id):
        signal = self._signal_list[signal_id]
        arr_times = np.asarray(signal.arr_times)
        dpt_times = np.asarray(signal.dpt_times)
        return np.diff(np.sort(arr_times)), np.diff(np.sort(dpt_times))

    def get_stop_headways(self, stop_id):
        stop = self._stop_list[stop_id]
        arr_times = np.asarray(stop.arr_times)
        return list(np.diff(np.sort(arr_times)))

    def reset(self, dspt_times):
        self._curr_time = 0.0
        self._total_bus = 0
        self._total_bus_list = []
        self._dspt_times = deepcopy(dspt_times)
        for link, stop, signal in zip(self._link_list, self._stop_list, self._signal_list):
            link.reset()
            stop.reset()
            signal.reset()

    def get_mean_std(self, headways):
        return np.around(np.mean(headways), decimals=1), np.around(np.std(headways), decimals=1)

if __name__ == "__main__":
    pass
    
    

    
