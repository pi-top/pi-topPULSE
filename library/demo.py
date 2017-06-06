# demo.py

import ptpulse
import time

led_matrix = ptpulse.ledmatrix
led_matrix.set_all(144,144,144)
led_matrix.show()

mic = ptpulse.microphone
mic.record()
time.sleep(10)
mic.stop()
mic.save("/tmp/test.wav", True)