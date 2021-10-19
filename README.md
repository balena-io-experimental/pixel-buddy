# second-screen
Create a dedicated second screen to share moments that are meaningful to you.

![](https://raw.githubusercontent.com/balena-io-playground/second-screen/master/images/device1b.jpg)

The second-screen runs on any balena device with a screen, but we provide directions and 3D printing files for our refernce design (above) which we call the "pixel Buddy".

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

`FLOWDOCK_TOKEN` - In Flowdock, click your user name in the upper left, select "account" and then "API tokens". Copy your personal API token and add it as a value to this device variable

The following variables are optional:

`TAGS` - A comma delimited list of tags. If any of the listed tags appear in a message in selected flows, your device will display them.

`FLOWS` - A comma delimited list of flows in which to look for the tags listed above.

`NO_EXPIRY_TAGS` - A comma delimted list of tags which will not auto expire and be deleted from the device.

`FLUSH` - A boolean ("true" or "false") value that determines whether images will be automatically deleted from the device when the flowdock service starts. This is useful when you alter the configuration of the device, and need old images removed.

`CURSOR` - A boolean ("true" or "false") value that determines if a cursor is shown on the screen.
