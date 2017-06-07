# demo.py

from ptpulse import ledmatrix
from ptpulse import microphone
from ptpulse import configuration
import time

print ("Enabling device...")
configuration.reset_device_state(True)
print ("")

time.sleep(1)

print ("Setting sample rate to 16KHz...")
configuration.set_microphone_sample_rate_to_16khz()

time.sleep(1)

ledmatrix.set_all(255, 0, 0)
ledmatrix.show()

print ("Recording audio for 5s...")
microphone.record()
time.sleep(5)
microphone.stop()
microphone.save("/tmp/test16.wav", True)
print ("Saved to /tmp/test16.wav")
print ("")

ledmatrix.off()
time.sleep(2)

print ("Setting sample rate to 22KHz...")
configuration.set_microphone_sample_rate_to_22khz()

time.sleep(1)

ledmatrix.set_all(255, 0, 0)
ledmatrix.show()

print ("Recording audio for 5s...")
microphone.record()
time.sleep(5)
microphone.stop()
microphone.save("/tmp/test22.wav", True)
print ("Saved to /tmp/test22.wav")
print ("")

ledmatrix.off()

print("Disabling device...")
configuration.reset_device_state(False)
print ("")

