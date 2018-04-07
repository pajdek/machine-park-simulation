import paho.mqtt.client as mqtt


class MqttHandler():
    def __init__(self, client_id):
        self.mqtt_client = mqtt.Client(client_id=client_id)
        try:
            self.mqtt_client.connect(host='192.168.1.133')
        except TimeoutError:
            print("It is impossible to get connection to MQTT broker, please run it, then start simulation")
            raise ConnectionError('MQTT broker is unreachable')

    def publish_msg(self, topic, msg):
            self.mqtt_client.publish(topic=topic, payload=msg, qos=0, retain=False)
