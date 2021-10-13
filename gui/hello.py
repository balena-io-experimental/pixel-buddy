import kivy
kivy.require('2.0.0') 
from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import gc
import os

AUTO_SLIDE_DURATION = 10
imagePath = os.getenv("IMAGE_PATH") or '/data/my_data'
images = []
pointer = 0

# A carousel component to show images slideshow
class SlideShow(Carousel):
    def build_carousel(self, initialLoad):
        global pointer
        self.clear_widgets()
        gc.collect()
        #read images
        images = sorted(os.listdir(imagePath))
        src = imagePath +'/' +images[pointer]
        image = Image(source=src, allow_stretch=True, nocache=True)
        self.add_widget(image)


        if not initialLoad:
            if pointer == (len(images)-1):
                pointer = 0
            else:
                pointer = (pointer + 1)
            
            src = imagePath +'/' +images[pointer]
            image = Image(source=src, allow_stretch=True, nocache=True)
            self.add_widget(image)

            self.load_next()

# main app 
class MainApp(App):
    def build(self):
        global images
        global pointer
        # create carousel 95% vertical space
        carousel = SlideShow(direction='right',loop = True,scroll_timeout=0,size_hint=(1,0.95))
        self.carousel = carousel

        # create label
        caption = Label(text='balenaSecondScreen',size_hint=(1,0.05))
        self.caption = caption

        # layout -> root widget
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.carousel)
        layout.add_widget(self.caption)
        return layout

    def on_start(self):
        self.carousel.build_carousel(True)

        # ToDo: 
        # set caption

        Clock.schedule_interval(self.build_carousel_on_timer,AUTO_SLIDE_DURATION)

    def build_carousel_on_timer(self,delay):
        self.carousel.build_carousel(False)
        # ToDo: 
        # update caption



    

MainApp().run()