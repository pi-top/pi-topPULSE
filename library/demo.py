# demo.py

import ptpulse
import time

led_matrix = ptpulse.ledmatrix
led_matrix.run_tests()

mic = ptpulse.microphone
mic.record()
time.sleep(10)
mic.stop()
mic.save("/tmp/test.wav", True)