from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.core.image import Image as CoreImage

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        outer_layout = BoxLayout(orientation='vertical')
        inner_layout = BoxLayout(orientation='horizontal')
        welcome_msg = Label(
            text="[size=50]Welcome to Psi Suite![/size]\n[size=32]Created by ACM Cyber[/size]",
            markup=True  # Important to enable markup
        )
       
        btn_intrude = Button(
            #background_normal="./flag.png",  # <-- Use background_normal for image
            #background_down="./flag.png",    # optional, when pressed
            text="Intrude",
            size_hint=(None, None),
            width=600, height=250
        )
    
            
        btn_race = Button(
            text="Race Condition",
            size_hint=(None, None), width=600, height=250
        )

        # center the two buttons
        welcome_msg.halign = 'center'
        welcome_msg.valign = 'center'
        
        outer_layout.add_widget(welcome_msg)

        inner_layout.add_widget(btn_intrude)
        inner_layout.add_widget(btn_race)
        btn_intrude.bind(on_press=self.go_to_intruder)
        btn_race.bind(on_press=self.go_to_race)

        outer_layout.add_widget(inner_layout)
        inner_layout.halign = 'center'
        inner_layout.valign = 'center'

        self.add_widget(outer_layout)  # Add the layout to the screen
    
    def go_to_intruder(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'intrude'  # Switch to the Intruder screen

    def go_to_race(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'race'  # Switch to the Intruder screen

class Intruder(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        welcome_msg = Label(text="You've reached the Intruder Section")
        btn_intrude = Button(text="Go back to home")
        layout.add_widget(welcome_msg)
        layout.add_widget(btn_intrude)
        btn_intrude.bind(on_press=self.go_to_home)
        self.add_widget(layout)  # Add the layout to the screen

    def go_to_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'  # Switch to the Intruder screen

class Race(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        welcome_msg = Label(text="You've reached the Race Condition Section")
        btn_intrude = Button(text="Go back to home")
        layout.add_widget(welcome_msg)
        layout.add_widget(btn_intrude)
        btn_intrude.bind(on_press=self.go_to_home)
        self.add_widget(layout)  # Add the layout to the screen

    def go_to_home(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'  # Switch to the Intruder screen

class MyApp(App):
    def build(self):
        sm = ScreenManager()  # Create a ScreenManager
        sm.add_widget(HomeScreen(name='home'))  # Add HomeScreen
        sm.add_widget(Intruder(name='intrude'))  # Add Intruder screen
        sm.add_widget(Race(name='race'))  # Add race screen
        return sm  # Return the ScreenManager as the root widget

if __name__ == "__main__":
    MyApp().run()
