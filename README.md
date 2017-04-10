![pi-top Logo](https://pi-top.com/image/loading/pitopLogoBlack.png)

Available from the [pi-top website](https://pi-top.com/product/addon).

# Getting set up
If you are wanting to get started with pi-topPULSE, you have a few different options:

## Use pi-topOS! (recommended)

pi-topPULSE libraries, as well as automatic audio configuration, are included and configured 'out-of-the-box' as standard on all new versions of pi-topOS. If you have an old version, or do not wish to run pi-topOS, then follow the steps below:

## Install via apt-get (next best option)

If you are using a Raspbian-based operating system (including pi-topOS) that does not currently have pi-topPULSE support, then it is easiest to open a terminal window and run the following command (with two ampersands '&'):

    sudo apt-get update && sudo apt-get install pt-pulse && sudo reboot
    
This will install everything you need to use the speaker and interact with the LEDs using Python!

If you just want to install automatic speaker detection and configuration, run the following:

    sudo apt-get update && sudo apt-get install pt-pulse-speaker && sudo reboot
    
If you just want to install the Python libraries for Python 2 and 3, you have a couple of choices. You can install either using `apt-get` or `pip`.

To install via `apt-get`, run the following:

    sudo apt-get update && sudo apt-get install python-pt-pulse python3-pt-pulse
    
To install via `pip`, run the following:


#### Install for Python 3:

Install `pip`:

	sudo apt-get install python3-pip python3-dev

Install `pt-pulse`:

	sudo pip3 install pt-pulse

#### Install for Python 2:

Install `pip`:

	sudo apt-get install python-pip python-dev

Install `pt-pulse`:

	sudo pip install pt-pulse


## Install manually (but... why?)

For those of you who like to get your hands dirty, or don't want a full installation, we have included some instructions to provide this functionality yourself. Under the hood, this is all that the `pt-pulse` package is doing anyway.

### Configuring your Raspberry Pi for pi-topPULSE's speaker
In order for sound to come out of the pi-topPULSE, the operating system needs to be outputting through the 3.5mm headphone/analog audio output.

As well as ensuring that sound is coming out of the correct input, pi-topPULSE's speaker requires GPIO pin 13 to be set to alternative mode 0 (ALT0) (also known as PWM mode).

If you want to have the automatic detection and configuration functionality (change audio output if necessary, change pin 13 mode) of the `pt-pulse-speaker` package without installing it directly, you can do this yourself. See the [audio](audio) folder for more information on how to do this.

If you're hellbent on doing this yourself, this can be done in a few different ways; if you are using a Raspbian-based operating system (including pi-topOS), then it is easiest to use `wiringpi`.

If `wiringpi` is not installed, run the following command first (with two ampersands '&'):

    sudo apt-get update && sudo apt-get install wiringpi

Once you have `wiringpi` installed, then simply open a terminal window and run:

    gpio -g mode 13 pwm
    
This will configure the pin correctly. This will get reset on a reboot.

### Installing the `ptpulse` Python Library

Download `ptpulse.py` from [here](library). Put this file in `/usr/lib/python2.7/dist-packages/` for Python 2 and `/usr/lib/python3/dist-packages/` for Python 3.


Then proceed to [examples](examples).

# Using pi-topPULSE:

Using `ptpulse` in Python requires root access to function. If you are running a script, make sure that you are running it with root access. You can do this with the "sudo" command:

	sudo python3 my_cool_pulse_script.py


Alternatively, if you are running Python in `IDLE`, please make sure you start LXTerminal and run idle or idle3 with the "sudo" command like so:

	sudo idle3

### Documentation & Support

* Function reference - http://docs.pimoroni.com/ptpulse/
* GPIO Pinout - http://pinout.xyz/pinout/ptpulse
* Get help - http://support.pi-top.com/support/login/