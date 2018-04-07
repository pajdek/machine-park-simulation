import time
import json


class MachineProcess():
    def __init__(self, machine_id, oled, temp_sensor, mqtt, topic='machine_park/'):
        self.mqtt_client = mqtt
        self.machine_id = machine_id
        self.topic = topic+machine_id
        self.temp_sensor = temp_sensor
        self.oled = oled
        self.try_to_connect_to_mqtt_broker()

    def set_mqtt_client(self):
        self.mqtt_client.connect()
        self.mqtt_client.set_callback(self.mqtt_msg_callback)
        self.mqtt_client.subscribe(self.topic)

    def read_temp(self):
        try:
            temp = self.temp_sensor.read_temp()
        except:
            MachineProcess.show_information_about_problem_with_sensor_on_oled(self.oled)
            raise 
        return temp

    def try_to_connect_to_mqtt_broker(self):
        try:
            self.set_mqtt_client()
        except:
            MachineProcess.show_information_about_problem_with_connection_to_mqtt_broker_on_oled(self.oled)
            raise

    def mqtt_msg_callback(self, topic, msg):
        self.oled.clear_oled()
        state = json.loads(msg)['state']
        temp = self.read_temp()
        print('temp: {temp}, mqtt_topic: {topic}, msg: {msg}'.format(
              temp=temp, topic=topic, msg=state))
        self.oled.show_state(state)
        self.oled.show_temp(temp)
        self.send_current_temp_by_mqtt(temp)
        time.sleep(1)

    def send_current_temp_by_mqtt(self, temp):
        try:
            self.mqtt_client.publish(topic=self.topic + '/temp', msg=temp)
        except:
            MachineProcess.show_information_about_problem_with_sensor_on_oled(self.oled)
            
    def start_machine_process(self):
        print("starting Machine Process")
        self.oled.show_short_words_oled_64_48('ATTACHED', 'TO MQTT', 'BROKER', 'WAITING', 'FOR MSG')

        while True:
            if True:
                self.mqtt_client.wait_msg()
            else:
                self.mqtt_client.check_msg()
                time.sleep(1)
    
    @staticmethod
    def show_information_about_problem_with_sensor_on_oled(oled):
        oled.show_short_words_oled_64_48('Problem', 'With', 'Sensor', 'Check &', 'Restart!')

    @staticmethod
    def show_information_about_problem_with_connection_to_mqtt_broker_on_oled(oled):
        oled.show_short_words_oled_64_48('Problem', 'TurnMQTT', 'BrokerOn', 'AndReset', 'Device!')