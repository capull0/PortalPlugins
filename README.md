# PortalPlugins
Python plugins to intercept RFID portals, like Skylanders, Disney Infinity ...

## short description
With this Python scripts together with my modified version of serialusb you can use images as normal RFID figures.

If you place a figure on the portal an image will be created. Via a configuration you can change the mapping.

I will add soon a video and a detailed description

## setup
- go to my fork of https://github.com/capull0/serialusb
- build a usb device like described on the github repository
- my setup: "Raspberry Zero W" connected over the GPIO serial pins with a "atmega32u4 pro micro"
- build and upload the firmware
- build serialusb

## Frontend application soon
i started a Python flask application where you can select and map the images you want to play, which will write the configuration for this plugin
