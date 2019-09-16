import gym
from gym import spaces
import numpy as np
from Simulator import Simulator
import parameters as paras

class BunchingEnv(gym.Env):
    """A bus bunching environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}

    def __init__(self, sim_duration):
        super().__init__()
        # the simulation env
        self._simulator = Simulator(sim_duration)
        # dynamically get the policy agents
        self._agents = []

        # configure spaces
        self.action_space = []
        self.observation_space = []
        for agent in self._agents:
            pass


        # self.action_space = spaces.Box(low=np.array([0, 0]), high=np.array([3, 1]), dtype=np.float16)
        # print(self.action_space.shape)
        
    def step(self, action_n):
        # self._simulator.running_buses
        obs_n = []
        reward_n = []
        info_n = {'n': []}
        # agent is the running trip, not neccessarily the bus; i.e., bus can be used for multiple trips
        
        # set action for each agent, since in the list, shallow copy, directly pass agent as the argument (pointer)
        for i, agent in enumerate(self._agents):
            pass
            # self._set_action(action_n[i], agent, self.action_space[i])

        self._get_obs()

        # loop until the next arrival
        total_arrived_buses = []
        while True:
            sim_end, total_arrived_buses = self._simulator.move_one_step(paras.delta_t, action_n)
            if sim_end or len(total_arrived_buses) >= 1:
                break
        print(len(total_arrived_buses))

        # finally, get the agents for next round
        self._agents = self._simulator.running_buses

    def _get_obs(self):
        obs_n = []
        self._simulator.get_observation()

    # set actions only to the buses that enter the stop
    def _set_action(self, action, agent, action_space):
        pass

    def _get_reward(self, agent):
        # rewards = [0] * len(self.running_buses)
        pass

    def reset(self):
        self._simulator.reset()
        obs_n = []
        # get the running buses as the agents
        self._agents = self._simulator.running_buses
        for agent in self._agents:
            obs_n.append(self._get_obs(agent))
        assert obs_n == [] # at the beginning, no bus is running
        return obs_n

    


if __name__ == "__main__":
    # query for action from each agent's policy
    # create interactive policies for each agent
    # policies = [InteractivePolicy(env,i) for i in range(env.n)]
    env = BunchingEnv(paras.sim_duration)
    # obs_n = env.reset()
    # execution loop
    # while:
        # act_n = []
        # for i, policy in enumerate(policies):
            # act_n.append(policy.action(obs_n[i]))

    for _ in range(8):
        act_n = []
        # for i, policy in enumerate(policies):
            # act_n.append(policy.action(obs_n[i]))
        env.step(act_n)
    env._simulator.plot_time_space()