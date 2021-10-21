# second-screen
Create a dedicated display to view shared moments that are meaningful to you.

![](https://raw.githubusercontent.com/balena-io-playground/second-screen/master/images/device1b.jpg)

The second-screen runs on any balena device with a screen, and we provide build instructions and 3D printing files for our reference design (above) which we call the "Pixel Buddy".

The second-screen pulls images from "sources" and stores them in a folder on the device. An image carousel container displays the images on an attached screen and also deletes the local images at regular intervals to save space and protect privacy.

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

Note that we use [Redis](https://redis.io/) to keep track of images to know whether we have processed them already and when they expire. (see the [db_functions.py](https://github.com/balena-io-playground/second-screen/blob/master/flowdock/db_functions.py) script.) In addition, the [text2image.py](https://github.com/balena-io-playground/second-screen/blob/master/flowdock/text2image.py) script uses the [Pillow](https://python-pillow.org/) imaging library to convert text-based messages to images, as well as to nicely center the text on the screen. Finally, [pilmoji](https://github.com/jay3332/pilmoji) is used to render any emojis. 

## The carousel
The carousel is in the "gui" container and is a Python script that displays the images in the shared folder as a slideshow. The script utilizes the [Kivy](https://kivy.org/#home) library for the carousel and to detect taps on the touchscreen. (Although initially, we don't perform any actions with touch events.)
