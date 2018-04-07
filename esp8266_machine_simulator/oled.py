import ssd1306
from machine import I2C, Pin


class Oled():
    def __init__(self, width, height, sda_pin, scl_pin):
        self.i2c = I2C(sda=Pin(sda_pin), scl=Pin(scl_pin))
        self.width = width
        self.height = height
        self.display = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
        self.display.fill(0)
        self.display.show()

    def show_msg_on_screen(self, msg, y_position, x_position=0, centralize=True, draw_line=False, line_position=12, clear=False):
        if clear:
            self.display.fill(0)
            self.display.show()
        if centralize:
            x = self.calculate_start_x_postion_to_centralize_msg(msg)
        else:
            x = x_position
        if draw_line:
            self.draw_horizontal_line_between_two_points(0, self.width, line_position)
        else:
            pass
        self.display.text(msg, x, y_position)
        self.display.show()

    def clear_oled(self):
        self.display.fill(0)
        self.display.show()

    def calculate_start_x_postion_to_centralize_msg(self, msg):
        msg_length = len(str(msg))
        x_start_position = (self.width - msg_length*8)/2
        return int(x_start_position)

    def draw_horizontal_line_between_two_points(self, x1, x2, y):
        for point in range(x1, x2+1):
            self.display.pixel(point, y, 1)
        self.display.show()

    def show_state(self, state):
        self.show_msg_on_screen('STATE:', x_position=0,
                                y_position=5, centralize=False, clear=False)
        self.show_msg_on_screen(state, x_position=0, centralize=False,
                                y_position=14, draw_line=True, line_position=24, clear=False)

    def show_temp(self, temp):
        self.show_msg_on_screen('T:'+temp, x_position=0,
                                y_position=32, centralize=False, clear=False)

    def show_short_words_oled_64_48(self, *args):
        y_position = 4
        clear = True
        for word in args:
            self.show_msg_on_screen(word, x_position=0, y_position=y_position, centralize=False, clear=clear)
            clear = False
            y_position += 8
