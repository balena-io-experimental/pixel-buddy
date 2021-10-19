# second-screen
Create a dedicated second screen to share moments that are meaningful to you.

![](https://raw.githubusercontent.com/balena-io-playground/second-screen/master/images/device1b.jpg)

The second-screen runs on any balena device with a screen, but we provide directions and 3D printing files for our refernce design (above) which we call the "pixel Buddy".

The second-screen pulls images from "sources" and stores them in a folder on the device. An image carousel container displays the images on an attached screen and also deletes the local images at regular intervals to save space and protect privacy.

![](https://raw.githubusercontent.com/balena-io-playground/second-screen/master/images/how-works.png)

## Sources
Initially we have created one source to pull images from [Flowdock](https://www.flowdock.com/), a real-time chat and collaboration tool for organizations. However, we would like to see more sources developed for other platforms and PRs are encouraged!

### Flowdock source
Features:
- Choose one or more flows
- Choose one or more tags or @'s
- Select an update frequency
- Photos shown on display
- #announce messages transformed into images

To use this source, you must set the following device variables:
