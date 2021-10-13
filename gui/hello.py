import kivy
kivy.require('2.0.0') 

from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.clock import Clock

import os

AUTO_SLIDE_DURATION = 10
REBUILD_DURATION = 60
imagePath = os.getenv("IMAGE_PATH") or '/data/my_data'

class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction='right',loop = True)
        self.carousel = carousel
        return carousel

    def on_start(self):
        Clock.schedule_interval(self.auto_slide, AUTO_SLIDE_DURATION)
        Clock.schedule_interval(self.build_carousel, REBUILD_DURATION)

    def auto_slide(self,delay):
        self.carousel.load_next()

    def build_carousel(self,delay):
        self.carousel.clear_widgets()
        #read images
        images = sorted(os.listdir(imagePath))
        for img in images:
            src = imagePath +'/' +img
            image = Image(source=src, allow_stretch=True, nocache=True)
            self.carousel.add_widget(image)

CarouselApp().run()