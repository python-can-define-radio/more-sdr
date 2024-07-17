from guizero import App, TextBox, PushButton
import random
import time
from pcdr.unstable.flow import OsmoSingleFreqTransmitter


def add_1():
    message.value += " 1"
    transmitter = OsmoSingleFreqTransmitter("hackrf=0", 2.455e9)
    transmitter.start()
    transmitter.set_if_gain(37)
    time.sleep(0.5)
    transmitter.stop_and_wait()

def add_0():
    message.value += " 0"
    transmitter = OsmoSingleFreqTransmitter("hackrf=0", 2.456e9)
    transmitter.start()
    transmitter.set_if_gain(37)
    time.sleep(0.5)
    transmitter.stop_and_wait()


app = App(title="Hello world")
onebutton = PushButton(app, text="1", command=add_1)
zerobutton = PushButton(app, text="0", command=add_0)
message = TextBox(app, text="... ", height=20, width=30, multiline=True)
app.display()

