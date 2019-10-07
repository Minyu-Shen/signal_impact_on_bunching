
def get_parameters(**kwargs):
    delta_t = 1.0
    sim_duration = int(3600*2)  # 100sec
    dspt_headway = 10 * 60  # min * 60
    sim_bus_no = sim_duration//dspt_headway + 1
    dspt_times = [(x+1)*dspt_headway for x in range(sim_bus_no)]

    # stops
    stop_num = 12
    stop_spacing = 1500 # inter-stop distance
    stop_locs = [(x+1)*stop_spacing for x in range(stop_num)]
    demand_rates = [2.5/60.0] * stop_num
    board_rates = [0.5] * stop_num
    # print('stop locations = {}'.format(stop_locs))

    # signals
    n = 1 # each link has n signals
    signal_num = n*stop_num
    fake_total_signals = [stop_spacing/(n+1) + x*stop_spacing/(n+1) for x in range((n+1)*stop_num)]
    signal_locs = [x for x in fake_total_signals if x not in stop_locs]
    cycle_lengths = [120] * signal_num # sec
    green_ratios = [1.0] * signal_num
    signal_offsets = [0] * signal_num # the green start compared to the previous signal
    examined_signal = int(signal_num / 2) - 1

    # links 
    link_num = stop_num
    link_lengths = [stop_spacing] * link_num
    link_mean_speeds = [30/3.6] * link_num # m/s
    link_cv_speeds = [0.1] * link_num
    link_start_locs = [x*stop_spacing for x in range(link_num)]
    # print('link start locations = {}'.format(link_start_locs))
    
    # create a virtual punctual bus to remove the initial demand impact
    link_mean_times = [length/speed for length, speed in zip(link_lengths, link_mean_speeds)]
    stop_mean_times = [d*dspt_headway for d in demand_rates]
    demand_times = [link_time+stop_time for link_time, stop_time in zip(link_mean_times, stop_mean_times)]
    demand_start_times = [sum(demand_times[:x]) for x in range(1, len(demand_times) + 1)] # accumulating demand_times
    # print(demand_start_times)

    if kwargs:
        cycle_lengths[examined_signal] = kwargs['cycle_length']
        green_ratios[examined_signal] = kwargs['green_ratio']
        signal_offsets[examined_signal] = kwargs['off_set']
    return (delta_t, sim_duration, dspt_times, \
            stop_locs, demand_rates, board_rates, stop_num, demand_start_times, \
                link_mean_speeds, link_cv_speeds, link_lengths, link_start_locs, \
                    cycle_lengths, green_ratios, signal_offsets, signal_locs, examined_signal)

if __name__ == "__main__":
    get_parameters()