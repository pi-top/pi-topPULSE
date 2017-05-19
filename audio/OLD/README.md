# pt-pulse-speaker

**NOTE**: Tested on Raspbian. Other operating systems: Your mileage may vary.

This folder contains all of the source files for automatic detection and configuration functionality. 

If you are wanting to get started with pi-topPULSE, you have a few different options:

## Use pi-topOS! (recommended)

pi-topPULSE libraries, as well as automatic audio configuration, are included and configured 'out-of-the-box' as standard on all new versions of pi-topOS. If you have an old version, or do not wish to run pi-topOS, then follow the steps below:

## Install via apt-get (next best option)

If you are using a Raspbian-based operating system (including pi-topOS) that does not currently have pi-topPULSE support, then it is easiest to open a terminal window and run the following command (with two ampersands '&'):

    sudo apt-get update && sudo apt-get install pt-pulse && sudo reboot
    
This will install everything you need to use the speaker and interact with the LEDs using Python!

If you just want to install automatic speaker detection and configuration, run the following:

    sudo apt-get update && sudo apt-get install pt-pulse-speaker && sudo reboot

## Install pt-pulse-speaker manually (full functionality)
Copy all files from `opt/pt-pulse` to `/opt/pt-pulse/` on your Raspberry Pi. Copy `pt-pulse-detect.service` to `/usr/systemd/system/`, and run:

	sudo systemctl enable pt-pulse-detect.service
	sudo reboot

## Minimal installation
* Output audio through the 3.5mm headphone/analog audio output.
* Set GPIO pin 13 to alternative mode 0 (ALT0) (also known as PWM mode).