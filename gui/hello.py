import kivy
kivy.require('2.0.0') 
from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.clock import Clock

import gc
import os

AUTO_SLIDE_DURATION = 10
imagePath = os.getenv("IMAGE_PATH") or '/data/my_data'
images = []
pointer = 0

class CarouselApp(App):
    def build(self):
        carousel = Carousel(direction='right',loop = True,scroll_timeout=0)
        self.carousel = carousel
        return carousel

    def build_carousel(self, initialLoad):
        global pointer
        self.carousel.clear_widgets()
        gc.collect()
        #read images
        images = sorted(os.listdir(imagePath))
        src = imagePath +'/' +images[pointer]
        image = Image(source=src, allow_stretch=True, nocache=True)
        self.carousel.add_widget(image)

        if not initialLoad:
            if pointer == (len(images)-1):
                pointer = 0
            else:
                pointer = (pointer + 1)
            
            src = imagePath +'/' +images[pointer]
            image = Image(source=src, allow_stretch=True, nocache=True)
            self.carousel.add_widget(image)

            self.carousel.load_next()   

    def on_start(self):
        self.build_carousel(True)
        Clock.schedule_interval(self.build_carousel_on_timer,AUTO_SLIDE_DURATION)

    def build_carousel_on_timer(self,delay):
        self.build_carousel(False)

    

CarouselApp().run()