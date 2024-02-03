from kivy.app import App
from kivy.core.window import Window as KivyWindow

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.button import Button

from src.progress_bar_custom import ProgressBarCustom
from src.tabbed_panel_main import TabbedPanelMain


class AppMainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AppMainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.button_click_count = 0

        self.label = Label(
            text="AppMainLayout",
            size_hint=(1, 0.33)
        )
        # self.add_widget(self.label)

        self.test_button = Button(
            # text="test button",
            text="click to increase progress",
            size_hint=(1, 0.33),
            on_release=lambda button_instance: \
                self.handle_test_button_click(button_instance)
        )
        # self.add_widget(self.test_button)

        self.main_tabbed_panel = TabbedPanelMain(size_hint=(1, 0.9))
        self.add_widget(self.main_tabbed_panel)

        self.main_tabbed_panel.get_demo_tab_callbacks() \
            ["increase_progress_button_click_cb"] = \
            lambda: self.handle_test_button_click(None)


        self.progress_bar_container = BoxLayout(
            size_hint=(1, 0.1)
        )
        self.add_widget(self.progress_bar_container)

        self.progress_bar_custom = ProgressBarCustom(size_hint=(1, 1))
        self.progress_bar_container.add_widget(self.progress_bar_custom)
        # self.progress_bar_custom.set_percent_complete(70)
    # *************************************************************
    # end: AppMainLayout.__init__()
    # *************************************************************
    def handle_test_button_click(self, button_instance):
        self.button_click_count += 1
        if self.button_click_count > 4:
            self.button_click_count = 0
        self.progress_bar_custom.set_percent_complete(self.button_click_count * 25)
        # print("The test button was clicked {} times".format(self.button_click_count))
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