import seaborn as sns
from simulator import Simulator
import matplotlib.pyplot as plt
from collections import defaultdict
import parameters as paras


def get_result(instance_no, has_signal, **kwargs):
    if has_signal:
        ### for examination
        examined_signal = kwargs['examined_signal']
        paras.green_ratios[examined_signal] = kwargs['green_ratio']
        paras.cycle_lengths[examined_signal] = kwargs['cycle_length']
        paras.signal_offsets[examined_signal] = kwargs['off_set']

    simulator = Simulator(paras.sim_duration, paras.dspt_times, \
        paras.stop_locs, paras.demand_rates, paras.board_rates, paras.stop_num,\
            paras.link_mean_speeds, paras.link_cv_speeds, paras.link_lengths, paras.link_start_locs, \
                paras.cycle_lengths, paras.green_ratios,paras.signal_offsets, paras.signal_locs)

    stop_headways = defaultdict(lambda: list) # stop_no -> headways
    for stop in range(paras.stop_num):
        stop_headways[stop] = []

    for sim_r in range(instance_no):
        simulator.distribute_initial_buses()
        for t in range(paras.sim_duration):
            is_bunched = simulator.move_one_step(paras.delta_t)
            if is_bunched: break

        for stop in range(paras.stop_num):
            arr_hdws_list = simulator.get_stop_headways(stop)
            stop_headways[stop] += arr_hdws_list

        if sim_r == instance_no-1:
            simulator.plot_time_space()
        simulator.reset(paras.dspt_times)

    arr_means = []
    arr_stds = []
    for stop in range(paras.stop_num):
        arr_mean, arr_std = simulator.get_mean_std(stop_headways[stop])
        arr_stds.append(arr_std)
        arr_means.append(arr_mean)
    return arr_means, arr_stds


if __name__ == "__main__":
    sns.set(color_codes=True)
    fig, ax = plt.subplots()

    examined_signal = int(paras.signal_num / 2) - 5
    g_r = 0.5
    c_l = 120
    o_s = 0
    instance_no = 2
    # no_signal_arr_means, no_signal_arr_stds = get_result(instance_no, False)
    # plt.plot(no_signal_arr_means, 'k', linestyle='solid', label='headway mean - no signal')
    # plt.plot(no_signal_arr_stds, 'k', linestyle='dotted', label='headway std - no signal')

    colors = ['r','g','b','y']
    for index, c_l in enumerate([80,160,240]):
        signal_arr_means, signal_arr_stds = get_result(instance_no, True, green_ratio=g_r, cycle_length=c_l, off_set=o_s, examined_signal=examined_signal)
        mean_lg_label = 'headway mean, cycle = ' + str(c_l) + ' sec'
        std_lg_label = 'headway std, cycle = ' + str(c_l) + ' sec'
        plt.plot(signal_arr_means, colors[index], linestyle='solid', label=mean_lg_label)
        plt.plot(signal_arr_stds, colors[index], linestyle='dotted', label=None)

    # legs = []
    # legs.append('stop=' + str(stop) + ', mean=' + str(arr_mean) + ', std=' + str(arr_std))
    # ax.legend(legs, loc=2, handlelength=3, fontsize=11)

    
    plt.vlines(examined_signal+0.5, 0, max(no_signal_arr_means), label='signal location')

    ax.set_xlabel('stop no.', fontsize=12)
    ax.set_ylabel('(sec) ', fontsize=12)
    ax.legend()
    plt.show()