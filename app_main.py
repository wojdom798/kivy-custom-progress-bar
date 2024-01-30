from kivy.app import App
from kivy.core.window import Window as KivyWindow

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.button import Button


class AppMainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AppMainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.button_click_count = 0

        self.label = Label(
            text="AppMainLayout",
            size_hint=(1, 0.5)
        )
        self.add_widget(self.label)

        self.test_button = Button(
            text="test button",
            size_hint=(1, 0.5),
            on_release=lambda button_instance: \
                self.handle_test_button_click(button_instance)
        )
        self.add_widget(self.test_button)
    # *************************************************************
    # end: AppMainLayout.__init__()
    # *************************************************************
    def handle_test_button_click(self, button_instance):
        self.button_click_count += 1
        print("The test button was clicked {} times".format(self.button_click_count))
# *************************************************************
# end: class AppMainLayout
# *************************************************************


class MyApp(App):
    def build(self):
        self.title = "Kivy Custom Progress Bar"
        KivyWindow.size = (900, 500)
        return AppMainLayout()


if __name__ == "__main__":
    MyApp().run()