import random
import simpy
import datetime
MACHINE_STATES = {
    1: {'state': "RUN", 'min_time': 1, 'max_time': 60, 'state_id': 1, 'possible_next_states': [2, 3, 4, 5]},
    2: {'state': "STOP", 'min_time': 1, 'max_time': 50, 'state_id': 2, 'possible_next_states': [5]},
    3: {'state': "MAINTENANCE", 'min_time': 3, 'max_time': 18, 'state_id': 3, 'possible_next_states': [1, 2, 5]},
    4: {'state': "FAILURE", 'min_time': 2, 'max_time': 5, 'state_id': 4, 'possible_next_states': [1]},
    5: {'state': "CHANGEOVER", 'min_time': 1, 'max_time': 10, 'state_id': 5, 'possible_next_states': [1]},
}
INTERVAL = 20
START_STATE_ID = 5
DATA_TIME_FORMAT = '%Y-%m-%d %H:%M'
START_SIMULATION = '2017-11-10 10:10'
STOP_SIMULATION = '2017-11-23 10:10'
data_time_start_simulation = datetime.datetime.strptime(START_SIMULATION, DATA_TIME_FORMAT)
data_time_stop_simulation = datetime.datetime.strptime(STOP_SIMULATION, DATA_TIME_FORMAT)
duration = data_time_stop_simulation - data_time_start_simulation
print(data_time_start_simulation + datetime.timedelta(minutes=60))
SIMULATION_TIME = duration.total_seconds()/60


class MachineProcess(object):
    """
    This is class used to simulate single machine process
    """
    def __init__(self, env, machine_id):
        """
        :param env: Environment from simpy package
        :param machine_id: This is uniq machine ID
        """
        self.env = env
        self.machine_id = machine_id
        self.action = env.process(self.run())
        self.machine_state = None

    def run(self):
        while True:
            self.rand_machine_state()
            print('Start state: {state_name} for machine {machine_id} at {time}'.format(
                state_name=self.machine_state['state'], machine_id=self.machine_id, time=(data_time_start_simulation+datetime.timedelta(minutes=self.env.now))))
            state_duration = self.get_state_duration(self.machine_state)
            yield self.env.timeout(state_duration)

    def rand_machine_state(self):
        """
        Method used to random machine state
        This method sets machine_state param
        """
        if self.machine_state:
            state_id = random.choice(self.machine_state['possible_next_states'])
            self.machine_state = MACHINE_STATES[state_id]
        else:
            self.machine_state = MACHINE_STATES[START_STATE_ID]

    @staticmethod
    def get_state_duration(machine_state):
        """
        The method used to randomize machine_state duration
        :param machine_state: machine_state dict
        :return: The random int number which is used for machine_state duration
        """
        return random.randint(machine_state['min_time'], machine_state['max_time'])*INTERVAL


env = simpy.Environment()
machines = []
for i in range(1, 5):
    machines.append(MachineProcess(env, i))

for machine in machines:
    try:
        machine.env.run(until=SIMULATION_TIME)
    except ValueError:
        print("end of simualtion for machine %s" % machine.machine_id)