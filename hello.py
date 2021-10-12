import kivy
kivy.require('2.0.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from kivy.clock import Clock

import os, sys

class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction='right')
        self.carousel = carousel

        #read images
        images = sorted(os.listdir('./images'))
        
        for img in images:
            src = './images/' +img
            image = AsyncImage(source=src, allow_stretch=True)
            carousel.add_widget(image)
        return carousel

    def on_start(self):
        Clock.schedule_interval(self.auto_slide, 10)

    def auto_slide(self,delay):
        pass
        # self.carousel.next_slide()


CarouselApp().run()