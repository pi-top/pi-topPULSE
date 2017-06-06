import signal
from serial import Serial
from tempfile import mkstemp
from threading import Thread

_debug = False
_continue_writing = False
_update_rate = 0.1

#######################
# INTERNAL OPERATIONS #
#######################

def _debug_print(message):
    """
    INTERNAL.
    """

    if _debug == True:
        print (message)    


def _signal_handler(signal, frame):
    """
    INTERNAL.
    """

    stop()
    print("\nQuitting...")
    sys.exit(0)
    

def _thread_method():
    """
    INTERNAL.
    """

    _record_audio()


def _record_audio():

    temp_file = mkstemp()

	ser = Serial(
		port = '/dev/serial0',
		timeout = 1,
		baudrate = 250000,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS
	)

	if ser.isOpen():
		print("Start recording")
		
		start_time = int(time.time())

		with open(temp_file, 'wb') as file:
			_debug_print("WRITING: initial header information")
			file.write(init_header_information())

			if ser.inWaiting():
				_debug_print("Flushing input and starting from scratch")
				ser.flushInput()

			_debug_print("WRITING: wave data")

			while _continue_writing:
				
				while not ser.inWaiting():
					time.sleep(0.001)
				
				audio_output = ser.read(ser.inWaiting())
				file.write(audio_output)

		ser.close()
		update_header_information()
		print("Finished Recording.")

	else:
		print("Serial port failed to open")




#######################
# EXTERNAL OPERATIONS #
#######################

def record():
    """
    Start recording on the pi-topPULSE microphone
    """

    _thread_running = True
    _continue_writing = True
    _recording_thread.start()



def stop():
    """Stops recording audio"""

    global _thread_running
    global _auto_refresh_timer

    _recording_thread.join()
    _thread_running = False
    

##################
# INITIALISATION #
##################

_signal = signal.signal(signal.SIGINT, _signal_handler)
_recording_thread = Thread(_thread_method)
