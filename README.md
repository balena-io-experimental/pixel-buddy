# pixel-buddy
Create a dedicated display to view shared moments that are meaningful to you.

![](https://raw.githubusercontent.com/balena-io-playground/second-screen/master/images/device1b.jpg)

The Pixel Buddy runs on any balena device with a screen, and we provide build instructions and 3D printing files for our reference design pictured above.

The Pixel Buddy pulls images from "sources" and stores them in a folder on the device. An image carousel container displays the images on an attached screen and also deletes the local images at regular intervals to save space and protect privacy.

![](https://raw.githubusercontent.com/balena-io-playground/second-screen/master/images/how-works.png)

## Sources
Initially we have created one source to pull images from [Flowdock](https://www.flowdock.com/), a real-time chat and collaboration tool for organizations. However, we would like to see more sources developed for other platforms and PRs are welcome!

### Flowdock source
Features:
- Choose one or more flows
- Choose one or more tags or @'s
- Select an update frequency
- Photos shown on display
- #announce messages transformed into images

To use this source, you must set the following device variable:

`FLOWDOCK_TOKEN` - In Flowdock, click your user name in the upper left, select "account" and then "API tokens". Copy your personal API token and add it as a value to this device variable.

The following variables are optional:

`TAGS` - A comma delimited list of tags. If any of the listed tags appear in a message in selected flows, your device will display them.

`FLOWS` - A comma delimited list of flows in which to look for the tags listed above.

`NO_EXPIRY_TAGS` - A comma delimted list of tags which will not auto expire and be deleted from the device.

`FLUSH` - A boolean ("true" or "false") value that determines whether images will be automatically deleted from the device when the flowdock service starts. This is useful when you alter the configuration of the device, and need old images removed.

`CURSOR` - A boolean ("true" or "false") value that determines if a cursor is shown on the screen.

Note that we use [Redis](https://redis.io/) to keep track of images to know whether we have processed them already and when they expire. (see the [db_functions.py](https://github.com/balena-io-playground/second-screen/blob/master/flowdock/db_functions.py) script.) In addition, the [text2image.py](https://github.com/balena-io-playground/second-screen/blob/master/flowdock/text2image.py) script uses the [Pillow](https://python-pillow.org/) imaging library to convert text-based messages to images, as well as to nicely center the text on the screen. Finally, [pilmoji](https://github.com/jay3332/pilmoji) is used to render any emojis contained in a message. 

## The carousel
The carousel is in the "gui" container and is a Python script that displays the images in the shared folder as a slideshow. The script utilizes the [Kivy](https://kivy.org/#home) library for the carousel and to detect taps on the touchscreen. (Although initially, we don't perform any actions with touch events.)

The [xserver block](https://github.com/balenablocks/xserver) runs an [X server](https://en.wikipedia.org/wiki/X_Window_System) which provides a display output for our carousel. The carousel communicates with the X server via a Unix socket. (The `x11:/tmp/.X11-unix` mapped volume in both container's docker-compose entry.)

## Reference design
Although this project runs on any balena device with a screen, the optimal experience for the Pixel Buddy utilizes a 4 inch square [HyperPixel display](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251444307) along with a Raspberry Pi 3A+ in a custom printed case. Below is the parts list and instructions for this design:

### Parts list
- [Pimoroni HyperPixel 4.0 Square Touch Display](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251444307) also available [here](https://www.adafruit.com/product/4499)
- [Raspberry Pi 3A+](https://www.raspberrypi.com/products/raspberry-pi-3-model-a-plus/)
- A MicroSD card and power supply for the Pi
- Custom printed case using a standard consumer 3D printer or printing service (files are in the [STL](https://github.com/balena-io-playground/second-screen/tree/master/stl) folder)
- Seven (7) M3 steel hex socket head cap bolt screws 10mm in length (such as [these](https://www.amazon.com/Fullerkreg-Socket-Stainless-Machine-Quantity/dp/B07CK3RSN3))

### Assembly instructions
(coming soon!)

### Software setup
You can use the button below to deploy this software to your device. If you don't already have a free [balenaCloud account](https://dashboard.balena-cloud.com/signup), you will be prompted to set one up first.

(button coming soon!)

Alternatively, you can clone this repo, create a new fleet, and push it to your device using the [balena CLI](https://www.balena.io/docs/reference/balena-cli/). This method is recommended if you want to potentially modify the project or do further development.

In either case, once you have clicked the deploy button (which will walk you through creating a fleet) or pushed the project using the CLI, next click the "Add device" button in your fleet. Choose the Raspberry Pi 3 (NOT 64 bit) and remember to enter your WiFi credentials since the Pi 3A+ does not have ethernet capability. Download the OS image file, burn it to a microSD card using [balena Etcher](https://www.balena.io/etcher/), insert the card into the Pi and then power it on.

The Pi will begin downloading the application but we need to set a few [device configuration variables](https://www.balena.io/docs/learn/manage/configuration/) before your display will show any images: (these are for the HyperPixel display only)

| Variable Name | Variable Value |
| ------------ | ----------- |
| RESIN_HOST_CONFIG_display_default_lcd | 1 |
| RESIN_HOST_CONFIG_dpi_group | 2 |
| RESIN_HOST_CONFIG_dpi_mode | 87 |
| RESIN_HOST_CONFIG_dpi_output_format | 0x5f026 |
| RESIN_HOST_CONFIG_dpi_timings | 720 0 20 20 40 720 0 15 15 15 0 0 0 60 0 36720000 4 |
| RESIN_HOST_CONFIG_enable_dpi_lcd | 1 |
| RESIN_HOST_CONFIG_framebuffer_height | 720 |
| RESIN_HOST_CONFIG_framebuffer_width | 720 |
| RESIN_HOST_CONFIG_overscan_bottom | 0 |
| RESIN_HOST_CONFIG_overscan_left | 0 |
| RESIN_HOST_CONFIG_overscan_right | 0 |
| RESIN_HOST_CONFIG_overscan_top | 0 |

After you enter these values, your containers will restart and soon your device should start displaying any images (if available.)

A few things to note about the HyperPixel display: Due to the way it interacts with the serial port, the device may not boot in development mode when attached to the display. In addition, the HyperPixel uses "basically all" of the GPIO pins, making them unavailable for HATs or other uses. There is however an alternate I2C interface on the back of the HyperPixel.
