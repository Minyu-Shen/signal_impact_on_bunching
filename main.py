import seaborn as sns
sns.set(color_codes=True)
from simulator import Simulator
import matplotlib.pyplot as plt
from collections import defaultdict
from parameters import get_parameters
from multiprocessing import Process, Manager
import numpy as np


def get_result(instance_no, delta_t, sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, \
            link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                cycle_lengths, green_ratios, signal_offsets, signal_locs):
    
    simulator = Simulator(sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num,\
            link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                cycle_lengths, green_ratios, signal_offsets, signal_locs)

    stop_headways = defaultdict(lambda: list) # stop_no -> headways
    for stop in range(stop_num):
        stop_headways[stop] = []

    for sim_r in range(instance_no):
        simulator.distribute_initial_buses()
        for t in range(sim_duration):
            is_bunched = simulator.move_one_step(delta_t)
            if is_bunched: break

        for stop in range(stop_num):
            arr_hdws_list = simulator.get_stop_headways(stop)
            stop_headways[stop] += arr_hdws_list

        # if sim_r == instance_no-1:
            # simulator.plot_time_space()
        simulator.reset(dspt_times)
    
    # append to the global variable
    for stop, hdws in stop_headways.items():
        total_hdws_dict[stop] = hdws
    

def get_mean_std(headways):
    return np.around(np.mean(headways), decimals=1), np.around(np.std(headways), decimals=1)

if __name__ == "__main__":
    
    # delta_t, sim_duration, dspt_times, \
    # stop_locs, demand_rates, board_rates, stop_num, \
    # link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
    # cycle_lengths, green_ratios, signal_offsets, signal_locs, examined_signal \
    # = get_parameters(cycle_length=120, green_ratio=0.5, off_set=10)
    # print(green_ratios)
    
    delta_t, sim_duration, dspt_times, \
    stop_locs, demand_rates, board_rates, stop_num, \
    link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
    cycle_lengths, green_ratios, signal_offsets, signal_locs, examined_signal \
    = get_parameters()

    # manager = Manager()
    total_hdws_dict = Manager().dict()
    for stop in range(stop_num):
        total_hdws_dict[stop] = []

    instance_no = 2
    process_num = 1
    batch_no = int(instance_no / process_num)
    processes = []
    for i in range(process_num):
        process = Process(target=get_result, args=(batch_no, delta_t, sim_duration, dspt_times, \
            stop_locs, demand_rates, board_rates, stop_num, \
                link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                    cycle_lengths, green_ratios, signal_offsets, signal_locs, ))
        process.start()
        processes.append(process)
    
    for process in processes:
        process.join()

    # print(total_hdws_dict[0])

    arr_means = []
    arr_stds = []
    for stop in range(stop_num):
        arr_mean, arr_std = get_mean_std(total_hdws_dict[stop])
        arr_stds.append(arr_std)
        arr_means.append(arr_mean)

    fig, ax = plt.subplots()
    plt.plot(arr_means, 'k', linestyle='solid', label='headway mean - no signal')
    plt.plot(arr_stds, 'k', linestyle='dotted', label='headway std - no signal')
    plt.vlines(examined_signal+0.5, 0, max(arr_means), label='signal location')
    ax.set_xlabel('stop no.', fontsize=12)
    ax.set_ylabel('(sec) ', fontsize=12)
    ax.legend()
    plt.show()

















    '''
    instance_no = 1
    # no signal case
    no_signal_arr_means, no_signal_arr_stds = get_result(instance_no, False)
    # plt.plot(no_signal_arr_means, 'k', linestyle='solid', label='headway mean - no signal')
    # plt.plot(no_signal_arr_stds, 'k', linestyle='dotted', label='headway std - no signal')

    # one signal case
    examined_signal = int(signal_num / 2) - 1
    g_r = 0.5
    c_l = 120
    o_s = 20

    colors = ['r','g','b','y']
    for index, c_l in enumerate([80]):
        signal_arr_means, signal_arr_stds = get_result(instance_no, True, green_ratio=g_r, cycle_length=c_l, off_set=o_s, examined_signal=examined_signal)
        mean_lg_label = 'headway mean, cycle = ' + str(c_l) + ' sec'
        std_lg_label = 'headway std, cycle = ' + str(c_l) + ' sec'
        # plt.plot(signal_arr_means, colors[index], linestyle='solid', label=mean_lg_label)
        # plt.plot(signal_arr_stds, colors[index], linestyle='dotted', label=None)

    # legs = []
    # legs.append('stop=' + str(stop) + ', mean=' + str(arr_mean) + ', std=' + str(arr_std))
    # ax.legend(legs, loc=2, handlelength=3, fontsize=11)

    fig, ax = plt.subplots()
    plt.vlines(examined_signal+0.5, 0, max(no_signal_arr_means), label='signal location')
    ax.set_xlabel('stop no.', fontsize=12)
    ax.set_ylabel('(sec) ', fontsize=12)
    ax.legend()
    plt.show()
    '''