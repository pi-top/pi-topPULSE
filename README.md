# pi-topPULSE

Available from the [pi-top website](https://pi-top.com/product/addon).

***Release note***:
Due to the following [Linux kernel issue](https://github.com/raspberrypi/linux/issues/1855), if you are running Linux kernel version 4.9.x, pi-topPULSE may not be fully functional. Until the issue is resolved it is necessary to [downgrade your kernel version](https://github.com/pi-top/pi-topPULSE/wiki/Downgrading-your-kernel-version).

To get started with pi-topPULSE we recommend installing the latest version of pi-topOS, otherwise you can follow one of the alternative methods:

## Recommended: Use pi-topOS

All pi-topPULSE software and libraries are included and configured 'out-of-the-box' as standard on the latest version of pi-topOS (>= 23-06-2017).

Download the latest version of pi-topOS at [https://pi-top.com/get-started](https://pi-top.com/get-started).

If you are running an older version of pi-topOS or running an alternative Raspbian-based disto, then follow the steps below:

## Alternative: Install via apt-get

If you are using a Raspbian-based distro and have their apt repository enabled you can follow either of the below instructions. Non Raspbian-based distros are not officially supported by pi-top but may be possible via a customer installation.

### Install everything

The following commands will install everything you need to use the speaker and interact with the LEDs using Python. It will also reboot your Raspberry Pi so ensure that any open documents have first been saved.

    sudo apt-get update
    sudo apt-get install pt-pulse
    sudo reboot    

### Custom installation

If you prefer to manually install the packages or want to install a specific set of packages see the [advanced installations page](https://github.com/pi-top/pi-topPULSE/wiki/Advanced-Installation-Methods).


# Using pi-topPULSE:

## Alexa Demo

...

## In a Python script

Using `ptpulse` in Python requires root access to function. If you are running a script, make sure that you are running it with root access. You can do this with the "sudo" command:

	sudo python3 my_cool_pulse_script.py


Alternatively, if you are running Python in `IDLE`, please make sure you start LXTerminal and run idle or idle3 with the "sudo" command like so:

	sudo idle3

# Documentation & Support

* Function reference - http://docs.pimoroni.com/ptpulse/
* GPIO Pinout - http://pinout.xyz/pinout/ptpulse
* Get help - http://support.pi-top.com/support/login/
