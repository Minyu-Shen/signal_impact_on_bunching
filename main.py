import seaborn as sns
sns.set(color_codes=True)
from simulator import Simulator
import matplotlib.pyplot as plt
from collections import defaultdict
from parameters import get_parameters
from multiprocessing import Process, Manager
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

        # if sim_r == batch_no-1:
            # simulator.plot_time_space()
        simulator.reset(dspt_times)
    
    # append to the global variable
    for stop, hdws in stop_headways.items():
        total_hdws_dict[stop] = hdws
    
def get_mean_std(headways):
    return np.around(np.mean(headways), decimals=1), np.around(np.std(headways), decimals=1)

def one_instance(**kwargs):
    if kwargs:
        c_l = kwargs['c_l']
        g_r = kwargs['g_r']
        o_s = kwargs['o_s']
        delta_t, sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
        link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
        cycle_lengths, green_ratios, signal_offsets, signal_locs, examined_signal \
        = get_parameters(cycle_length=c_l, green_ratio=g_r, off_set=o_s)
    else:
        delta_t, sim_duration, dspt_times, \
        stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
        link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
        cycle_lengths, green_ratios, signal_offsets, signal_locs, examined_signal \
        = get_parameters()
    
    for stop in range(stop_num):
        total_hdws_dict[stop] = []

    processes = []
    for i in range(process_num):
        process = Process(target=get_result, args=(batch_no, delta_t, sim_duration, dspt_times, \
            stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
                link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                    cycle_lengths, green_ratios, signal_offsets, signal_locs, ))
        process.start()
        processes.append(process)
    
    for process in processes:
        process.join()

    arr_means = []
    arr_stds = []
    for stop in range(stop_num):
        arr_mean, arr_std = get_mean_std(total_hdws_dict[stop])
        arr_stds.append(arr_std)
        arr_means.append(arr_mean)
    return arr_means, arr_stds

if __name__ == "__main__":
    
    ###### for plotting time-space diagram
    # delta_t, sim_duration, dspt_times, \
    # stop_locs, demand_rates, board_rates, stop_num, \
    # link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
    # cycle_lengths, green_ratios, signal_offsets, signal_locs, examined_signal \
    # = get_parameters(cycle_length=120, green_ratio=0.6, off_set=0)
    
    # print(green_ratios)

    # get_result(2, delta_t, sim_duration, dspt_times, \
    # stop_locs, demand_rates, board_rates, stop_num, \
    # link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
    # cycle_lengths, green_ratios, signal_offsets, signal_locs)


    instance_no = 20
    process_num = 2
    batch_no = int(instance_no / process_num)


    ##### signal_cases ##### 
    # c_ls = [80,160,240]
    c_ls = [160]
    o_ss = [0,30,60]
    # o_ss = [30]
    # g_rs = [0.3,0.5,0.7]
    g_rs = [0.5]
    total_hdws_dict = Manager().dict()
    signal_mean_factors = defaultdict(lambda: list)
    signal_std_factors = defaultdict(lambda: list)
    for c_l in c_ls:
        for o_s in o_ss:
            for g_r in g_rs:
                if len(c_ls) > 1: factor=c_l
                if len(o_ss) > 1: factor=o_s
                arr_means, arr_stds = one_instance(c_l=c_l, g_r=g_r, o_s=o_s)
                signal_mean_factors[factor] = arr_means
                signal_std_factors[factor] = arr_stds


    ##### no_signal_cases #####
    no_sig_means, no_sig_stds = one_instance()
    
    ### plotting
    fig, ax = plt.subplots()
    plt.plot(no_sig_means, 'k', linestyle='solid', label='headway mean - no signal')
    plt.plot(no_sig_stds, 'k', linestyle='dotted', label='headway std - no signal')

    colors = ['r','g','b','y']
    for index, factor in enumerate(o_ss): # change!!!
        plt.plot(signal_mean_factors[factor], colors[index], linestyle='solid', label=None)
        plt.plot(signal_std_factors[factor], colors[index], linestyle='dotted', label='os=' + str(factor)) #change!!

    plt.vlines(5-0.5, 0, max(signal_mean_factors[o_ss[0]]), label='signal location') # change!!
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
        

    # legs = []
    # legs.append('stop=' + str(stop) + ', mean=' + str(arr_mean) + ', std=' + str(arr_std))
    # ax.legend(legs, loc=2, handlelength=3, fontsize=11)

    '''