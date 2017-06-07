# demo.py

from ptpulse import ledmatrix
from ptpulse import microphone
import time

ledmatrix.run_tests()

microphone.record()
time.sleep(3)
microphone.stop()
microphone.save("/tmp/test.wav", True)