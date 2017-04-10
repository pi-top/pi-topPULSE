![pi-top Logo](https://pi-top.com/image/loading/pitopLogoBlack.png)

Available from pi-top: https://pi-top.com/product/addon

### Important Notice

Sound works via 3.5mm/analog audio output.

### `ptpulse` Python Library & Examples

Here you'll find everything you need to start lighting up your pi-topPULSE HAT using Python.

Python users should probably ignore most of this repository and just:

**Use pi-topOS ( recommended ):**

pi-topPULSE libraries are included as standard on all new versions of pi-topOS. If you have an old version, or do not wish to run, 

**Install for Python 3:**

```bash
sudo apt-get install python3-pip python3-dev
sudo pip3 install pt-pulse
```

**Install for Python 2:**

```bash
sudo apt-get install python-pip python-dev
sudo pip install pt-pulse
```

Then proceed to [examples](examples).

### Using with idle/idle3:

`ptpulse` needs root access to function. Please make sure you start LXTerminal and run idle or idle3 with the "sudo" command like so:

```bash
sudo idle
```

### Documentation & Support

* Function reference - http://docs.pimoroni.com/ptpulse/
* GPIO Pinout - http://pinout.xyz/pinout/unicorn_hat
* Get help - http://support.pi-top.com/support/login/

### Library designed as a drop-in replacement for Pimoroni's Unicorn Hat library

`ptpulse` fully supports all functions provided by the Unicorn Hat Python library. This means that all code designed for Unicorn Hat can be easily modified to work with `ptpulse`.