from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        outer_layout = BoxLayout(orientation="vertical")
        inner_layout = BoxLayout(
            orientation="horizontal"
            # spacing=50,
            # padding=[50, 20],
        )
        welcome_msg = Label(
            text="[size=50]Welcome to Psi Suite![/size]\n[size=32]Created by ACM Cyber[/size]",
            markup=True,  # Important to enable markup
        )

        # btn_intrude = Button(
        #     text="Intrude",
        #     size_hint=(0.5, None),  # 50% width, fixed height
        #     height=250
        # )

        btn_intrude = Button(
            # background_normal="pink.png",
            # background_down="pink.png",
            background_color=get_color_from_hex("#a40062"),
            size_hint=(0.5, 1),
            text="Intrude",
            font_size=24,
            color=(1, 1, 1, 1),  # white text, RGBA
        )

        btn_race = Button(
            text="Race Condition",
            size_hint=(0.5, 1),
            background_color=get_color_from_hex("#a40062"),
        )

        # center the two buttons
        welcome_msg.halign = "center"
        welcome_msg.valign = "center"

        outer_layout.add_widget(welcome_msg)

        button_row = BoxLayout(
            orientation="horizontal", spacing=20, size_hint=(1, None), height=250
        )
        button_row.add_widget(btn_intrude)
        button_row.add_widget(btn_race)

        # anchors buttons horizontally
        anchor = AnchorLayout(
            anchor_x="center", anchor_y="center", size_hint=(1, None), height=250
        )
        anchor.add_widget(button_row)

        outer_layout.add_widget(anchor)

        btn_intrude.bind(on_press=self.go_to_intruder)
        btn_race.bind(on_press=self.go_to_race)

        self.add_widget(outer_layout)  # Add the layout to the screen

    def go_to_intruder(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "intrude"  # Switch to the Intruder screen

    def go_to_race(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "race"  # Switch to the Intruder screen


class Intruder(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        # Define components
        welcome_msg = Label(text="You've reached the Intruder Section")
        btn_upload = Button(text="Upload File")
        btn_intrude = Button(text="Intrude!")
        btn_home = Button(text="Go back to home")

        # add components to layout
        layout.add_widget(welcome_msg)

        layout.add_widget(btn_upload)
        btn_upload.bind(on_press=self.open_filechooser)

        self.file_display = BoxLayout(
            orientation="vertical", size_hint_y=None, height=500
        )
        layout.add_widget(self.file_display)

        layout.add_widget(btn_intrude)

        layout.add_widget(btn_home)
        btn_home.bind(on_press=self.go_to_home)

        self.add_widget(layout)  # Add the layout to the screen

    def go_to_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "home"  # Switch to the Intruder screen

    def open_filechooser(self, instance):
        layout = BoxLayout(orientation="vertical")

        filechooser = FileChooserListView()
        self.filechooser = filechooser  # Save a reference to access selected file

        btn_select = Button(text="Select", size_hint=(1, 0.1))
        btn_select.bind(on_press=self.on_file_select_button_pressed)

        layout.add_widget(filechooser)
        layout.add_widget(btn_select)

        self.popup = Popup(title="Choose a file", content=layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def on_file_select_button_pressed(self, instance):
        selection = self.filechooser.selection
        if selection:
            file_path = selection[0]
            print(f"Selected file: {file_path}")
            self.popup.dismiss()
            self.display_file(file_path)

    def display_file(self, file_path):
        # Clear the previous file display content
        self.file_display.clear_widgets()

        file_label = Label(text=file_path, size_hint_y=None, height=400)
        self.file_display.add_widget(file_label)


class Race(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        welcome_msg = Label(text="You've reached the Race Condition Section")
        btn_intrude = Button(text="Go back to home")
        layout.add_widget(welcome_msg)
        layout.add_widget(btn_intrude)
        btn_intrude.bind(on_press=self.go_to_home)
        self.add_widget(layout)  # Add the layout to the screen

    def go_to_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "home"  # Switch to the Intruder screen


class MyApp(App):
    def build(self):
        sm = ScreenManager()  # Create a ScreenManager
        sm.add_widget(HomeScreen(name="home"))  # Add HomeScreen
        sm.add_widget(Intruder(name="intrude"))  # Add Intruder screen
        sm.add_widget(Race(name="race"))  # Add race screen
        return sm  # Return the ScreenManager as the root widget


if __name__ == "__main__":
    MyApp().run()
