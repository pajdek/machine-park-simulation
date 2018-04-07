import random
import simpy
import datetime
import json
from mqtt_handler import MqttHandler


MACHINE_STATES = {
    1: {'state': "RUN", 'min_time': 1, 'max_time': 60, 'state_id': 1, 'possible_next_states': [2, 3, 4, 5]},
    2: {'state': "STOP", 'min_time': 1, 'max_time': 50, 'state_id': 2, 'possible_next_states': [5]},
    3: {'state': "MAINT", 'min_time': 3, 'max_time': 18, 'state_id': 3, 'possible_next_states': [1, 2, 5]},
    4: {'state': "FAILURE", 'min_time': 2, 'max_time': 5, 'state_id': 4, 'possible_next_states': [1]},
    5: {'state': "HANDOVER", 'min_time': 1, 'max_time': 10, 'state_id': 5, 'possible_next_states': [1]},
}

NUMBER_OF_MACHINES = 3
INTERVAL = 1
START_STATE_ID = 5
DATA_TIME_FORMAT = '%Y-%m-%d %H:%M'
START_SIMULATION = '2017-11-10 10:10'
STOP_SIMULATION = '2017-11-23 10:10'
data_time_start_simulation = datetime.datetime.strptime(START_SIMULATION, DATA_TIME_FORMAT)
data_time_stop_simulation = datetime.datetime.strptime(STOP_SIMULATION, DATA_TIME_FORMAT)
duration = data_time_stop_simulation - data_time_start_simulation
print(data_time_start_simulation + datetime.timedelta(minutes=60))
SIMULATION_TIME = duration.total_seconds() / 60


class MachineProcess(object):
    """
    This is class used to simulate single machine process
    """

    def __init__(self, machine_id, start_simulation_date, stop_simulation_date, mqtt_handler):
        """
        :param env: Environment from simpy package
        :param machine_id: This is uniq machine ID
        """
        self.machine_id = "machine_" + str(machine_id)
        self.machine_state = None
        self.mqtt_handler = mqtt_handler
        self.start_simulation_date = start_simulation_date
        self.stop_simulation_date = stop_simulation_date
        self.sim_env = simpy.rt.RealtimeEnvironment()
        self.sim_env.process(self.machine_process())
        self.simulation_time = ((self.stop_simulation_date - self.start_simulation_date).total_seconds()) / 60
        print(self.simulation_time)

    def run_simulation(self):
        self.sim_env.run(until=self.simulation_time)

    def machine_process(self):
        while True:
            self.rand_machine_state()
            self.print_information_about_current_machine_state()
            current_state_duration = self.get_state_duration(self.machine_state)
            self.publish_current_machine_state_by_mqtt_protocol()
            yield self.sim_env.timeout(current_state_duration)

    def print_information_about_current_machine_state(self):
        print('Start state: {state_name} for machine {machine_id} at {time}'.format(
            state_name=self.machine_state['state'], machine_id=self.machine_id,
            time=self.get_current_simulation_date_time()))

    def get_current_simulation_date_time(self):
        return self.start_simulation_date + datetime.timedelta(minutes=self.sim_env.now)

    def preper_mqtt_json_payload_with_machine_state(self):
        """
        Method used for preparing json_payload about machine current state
        for mQTT protocol
        """
        mqtt_payload = json.dumps({"state": self.machine_state['state'],
                                   "state_start": str(self.get_current_simulation_date_time())})
        return mqtt_payload

    def publish_current_machine_state_by_mqtt_protocol(self):
        """
        Method used for publishing machine current state by mqtt protocol
        """
        self.mqtt_handler.publish_msg(topic="machine_park/{machine_id}".format(machine_id=self.machine_id),
                                      msg=self.preper_mqtt_json_payload_with_machine_state())

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
        return random.randint(machine_state['min_time'], machine_state['max_time'])


machine_1 = MachineProcess(1, data_time_start_simulation, data_time_stop_simulation)
machine_1.run_simulation()
