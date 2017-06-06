# demo.py

import ptpulse
from time import sleep 

led_matrix = ptpulse.ledmatrix
led_matrix.set_all(255,255,255)
led_matrix.show()

mic = ptpulse.microphone
mic.record()
time.sleep(5)
mic.stop()