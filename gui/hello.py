import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.clock import Clock

import os

AUTO_SLIDE_DURATION = 10

class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction='right',loop = True)
        self.carousel = carousel

        #read images
        images = sorted(os.listdir('./images'))
        
        for img in images:
            src = './images/' +img
            image = AsyncImage(source=src, allow_stretch=True)
            carousel.add_widget(image)
        return carousel

    def on_start(self):
        Clock.schedule_interval(self.auto_slide, AUTO_SLIDE_DURATION)

    def auto_slide(self,delay):
        self.carousel.load_next()



CarouselApp().run()