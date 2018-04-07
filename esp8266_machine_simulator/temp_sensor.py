import machine
import onewire
import time
from ds18x20 import DS18X20


class TempSensor():
    def __init__(self, pin):
        self.sensor_pin = machine.Pin(12)
        self.sensor = DS18X20(onewire.OneWire(self.sensor_pin))
        self.rom = self.sensor.scan()[0]
        self.read_temp()

    def read_temp(self):
        print('Reading temp...')
        self.sensor.convert_temp()
        time.sleep(1)
        temp = self.sensor.read_temp(self.rom)
        return str(temp)[:5]
