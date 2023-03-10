from machine import Pin, PWM, I2C, RTC
import network
from umqtt.simple import MQTTClient

ssid = 'you_network'
password = 'your_psk'
mqtt_server = 'mqtt_broker_ip'
transmitter_id = 0

class Button:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.pressed = False
        self.since_last_press = 0
        self.on_down = None
        self.on_up = None

    def update(self):
        pressed = self.pin.value() > 0
        if pressed != self.pressed:
            self.pressed = pressed
            self.since_last_press = 0
            self.handle_button()
            return True
        if self.since_last_press < 2000:
            self.since_last_press = self.since_last_press + 1
        return False

    def handle_button(self):
        if self.pressed and self.on_down is not None:
            self.on_down()
        if self.pressed is False and self.on_up is not None:
            self.on_up()


def send_mqtt_message(topic, message):
    client = MQTTClient('switch_pico', mqtt_server)
    client.connect()

    client.publish(topic.encode(), message.encode())

    client.disconnect()

def button_1_press():
    send_mqtt_message(f"remote_switch/{transmitter_id}",f"{transmitter_id}:1")
    
def button_2_press():
    send_mqtt_message(f"remote_switch/{transmitter_id}",f"{transmitter_id}:2")
    
def button_3_press():
    send_mqtt_message(f"remote_switch/{transmitter_id}",f"{transmitter_id}:3")
    
def button_4_press():
    send_mqtt_message(f"remote_switch/{transmitter_id}",f"{transmitter_id}:4")

if __name__ == "__main__":
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    
    while not sta_if.isconnected():
        pass

    button1 = Button(18)
    button1.on_up = button_1_press
    button2 = Button(19)
    button2.on_up = button_2_press
    button3 = Button(20)
    button3.on_up = button_3_press
    button4 = Button(21)
    button4.on_up = button_4_press
    buttons = [
        button1,
        button2,
        button3,
        button4
    ]

    while True:
        for button in buttons:
            button.update()

