delta_t = 1.0
sim_duration = int(3600*2)  # 100sec
dspt_headway = 10 * 60  # min * 60
sim_bus_no = sim_duration//dspt_headway + 1
dspt_times = [x*dspt_headway for x in range(sim_bus_no)]

# stops
stop_num = 12
stop_spacing = 1500 # inter-stop distance
stop_locs = [(x+1)*stop_spacing for x in range(stop_num)]
demand_rates = [3.5/60.0] * stop_num
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
# print('signal locations = {}'.format(signal_locs))
# signal_offsets = [x*10 for x in range(signal_num)]


# links 
link_num = stop_num
link_lengths = [stop_spacing] * link_num
link_mean_speeds = [30/3.6] * link_num # m/s
link_cv_speeds = [0.1] * link_num
link_start_locs = [x*stop_spacing for x in range(link_num)]
# print('link start locations = {}'.format(link_start_locs))

