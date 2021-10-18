import kivy
kivy.require('2.0.0') 
from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

import os

AUTO_SLIDE_DURATION = 10

# A carousel component to show images slideshow
class SlideShow(ScreenManager):
    def __init__(self, *args, images=list(), **kwargs):
        super(ScreenManager, self).__init__(*args, **kwargs)
        for image in images:
            screen = Screen(name=os.path.basename(image))
            screen.add_widget(Image(source=image, allow_stretch=True, nocache=True))
            self.add_widget(screen)

class MainApp(App):
    def build(self):
        image_path = os.getenv("IMAGE_PATH") or '/data/my_data'
        images = [os.path.join(image_path, name) for name in sorted(os.listdir(image_path))]

        # create carousel 95% vertical space
        self.slideshow = SlideShow(images=images, transition=SlideTransition())

        # create label
        self.caption = Label(
                text=self.slideshow.current,
                size_hint=(1,0.05),
                font_size='25sp',
                text_size=(500, None),
                halign='center')

        # discard the message ID and join the remaining parts with a space
        def set_caption(obj, screen_name):
            self.caption.text = ' '.join(screen_name.split('_')[1:])
        self.slideshow.bind(current=set_caption)

        # layout -> root widget
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.slideshow)
        layout.add_widget(self.caption)
        return layout

    def on_start(self):
        def advance_slide(*args):
            self.slideshow.current = self.slideshow.next()

        Clock.schedule_interval(advance_slide, AUTO_SLIDE_DURATION)

MainApp().run()
