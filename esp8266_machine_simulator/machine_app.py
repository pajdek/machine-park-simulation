from oled import Oled
from temp_sensor import TempSensor
from machine_process import MachineProcess
from umqtt.simple import MQTTClient

oled = Oled(64, 48, 4, 5)
try:
    temp_sensor = TempSensor(12)
except:
    MachineProcess.show_information_about_problem_with_sensor_on_oled(oled)
    raise

mqtt_client = MQTTClient('machine_1', '192.168.1.133')

machine_process = MachineProcess(machine_id='machine_1', oled=oled, temp_sensor=temp_sensor, mqtt=mqtt_client)


def start():
    machine_process.start_machine_process()
