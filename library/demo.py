# demo.py

from ptpulse import ledmatrix
from ptpulse import microphone
from ptpulse import configuration
import time

print ("Enabling device...")
configuration.reset_device_state(True)
print ("")

time.sleep(1)

print ("Setting sample rate to 22KHz...")
configuration.set_microphone_sample_rate_to_22khz()

time.sleep(1)

print ("Recording audio for 5s...")
ledmatrix.set_all(255, 0, 0)
ledmatrix.show()
microphone.record()
time.sleep(5)
microphone.stop()
microphone.save("/tmp/test22-1.wav", True)
print ("Saved to /tmp/test22-1.wav")
print ("")

ledmatrix.off()
time.sleep(1)

print ("Setting sample rate to 16KHz...")
configuration.set_microphone_sample_rate_to_16khz()

time.sleep(1)

print ("Recording audio for 5s...")
ledmatrix.set_all(255, 0, 0)
ledmatrix.show()
microphone.record()
time.sleep(5)
microphone.stop()
microphone.save("/tmp/test16.wav", True)
print ("Saved to /tmp/test16.wav")
print ("")

ledmatrix.off()
time.sleep(1)

print ("Setting sample rate to 22KHz...")
configuration.set_microphone_sample_rate_to_22khz()

time.sleep(1)

print ("Recording audio for 5s...")
ledmatrix.set_all(255, 0, 0)
ledmatrix.show()
microphone.record()
time.sleep(5)
microphone.stop()
microphone.save("/tmp/test22-2.wav", True)
print ("Saved to /tmp/test22-2.wav")
print ("")

ledmatrix.off()

time.sleep(1)

print("Disabling device...")
configuration.reset_device_state(False)
print ("")

