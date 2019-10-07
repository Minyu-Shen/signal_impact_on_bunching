import seaborn as sns
sns.set(color_codes=True)
from simulator import Simulator
import matplotlib.pyplot as plt
from collections import defaultdict
from parameters import get_parameters
import numpy as np
import parameters


def get_result(batch_no, delta_t, sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
            link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                cycle_lengths, green_ratios, signal_offsets, signal_locs):
    
    simulator = Simulator(sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
            link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                cycle_lengths, green_ratios, signal_offsets, signal_locs)

    stop_headways = defaultdict(lambda: list) # stop_no -> headways
    for stop in range(stop_num):
        stop_headways[stop] = []

    for sim_r in range(batch_no):
        for t in range(sim_duration):
            is_bunched = simulator.move_one_step(delta_t)
            if is_bunched: break

        for stop in range(stop_num):
            arr_hdws_list = simulator.get_stop_headways(stop)
            stop_headways[stop] += arr_hdws_list

        if sim_r == batch_no-1:
            simulator.plot_time_space()
        simulator.reset(dspt_times)
    
    return stop_headways
    
def get_mean_std(headways):
    return np.around(np.mean(headways), decimals=1), np.around(np.std(headways), decimals=1)


if __name__ == "__main__":
    batch_no = 1
    delta_t, sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
            link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                cycle_lengths, green_ratios, signal_offsets, signal_locs, examined_signal \
                    = get_parameters()

    stop_headways_dict = get_result(batch_no, delta_t, sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
            link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                cycle_lengths, green_ratios, signal_offsets, signal_locs)
    
    arr_means = []
    arr_stds = []
    for stop in range(stop_num):
        arr_mean, arr_std = get_mean_std(stop_headways_dict[stop])
        arr_stds.append(arr_std)
        arr_means.append(arr_mean)
    
    print(arr_means)