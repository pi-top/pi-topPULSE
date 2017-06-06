pi-topPULSE Python Library
==========================

This library provides convenience functions for interacting with pi-topPULSE.


Installing
----------

We recommend using Python 3 when possible, therefore installing the pi-topPULSE Python library can be most easily done with `pip3`.

    sudo pip3 install pt-pulse

If you do not have pip3 installed, follow [this tutorial](https://pip.pypa.io/en/stable/installing/) to install it.

If you insist on using Python 2, you can install the library with `pip`:

    sudo pip install pt-pulse

Alternatively, you can run `setup.py`:

    sudo ./setup.py install


Basic Usage
-----------

Just `import pulse`, then all you need is:

* pulse.set_pixel(x, y, red, green, blue) - Set a pixel in the buffer to the specified colour
* pulse.show - Update pi-topPULSE with the current buffer
* pulse.off - Turn off all the pixels in the buffer and update pi-topPULSE

Note: the `show` function will wait on incoming requests if they are being sent less than 20ms after a previous request. To prevent this, pause for 20ms after each show: `time.sleep(0.02)`.
