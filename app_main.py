import threading
import time
from kivy.clock import mainthread as kivy_mainthread

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

        self.main_tabbed_panel.get_demo_tab_callbacks() \
            ["progress_slider_value_change_cb"] = \
            lambda new_value: self.set_progress_bar_value(new_value)

        self.main_tabbed_panel.get_demo_tab_callbacks() \
            ["start_simulation_cb"] = lambda: self.run_comparison_simulation()


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


    def set_progress_bar_value(self, new_value):
        self.progress_bar_custom.set_percent_complete(new_value)


    def run_comparison_simulation(self):
        NUM_OF_ITEMS_TO_COMPARE = 10000
        REFRESH_RATE_MS = 70

        comparison_simulation_thread = threading.Thread(
            target=self.simulate_comparisons,
            args=(
                NUM_OF_ITEMS_TO_COMPARE,
                lambda update_data: self.update_progressbar_threaded(update_data),
                REFRESH_RATE_MS
            )
        )
        comparison_simulation_thread.start()


    @kivy_mainthread
    def update_progressbar_threaded(self, update_data):
        percent_complete = \
            (update_data["current_progress"] / update_data["total_progress"]) * 100
        self.progress_bar_custom.set_percent_complete(percent_complete)


    def simulate_comparisons(self, num_of_items, on_progress_update, refresh_rate_ms=120):
        if not (type(num_of_items) == int):
            raise TypeError("\'num_of_items\' must be an integer.")

        if num_of_items < 2:
            raise ValueError("\'num_of_items\' must be greater than 2.")

        if not callable(on_progress_update):
            raise TypeError("\'on_progress_update\' must be a function reference.")

        if not (type(refresh_rate_ms) == int):
            raise TypeError("\'refresh_rate_ms\' must be an integer.")

        if refresh_rate_ms <= 0:
            raise ValueError("\'refresh_rate_ms\' must be greater than 0.")

        # n = num_of_items - 1
        # total_progress = ((1 + n) / 2) * n
        current_progress = 0
        total_progress = ((num_of_items) / 2) * (num_of_items - 1)
        
        previous_update_timestamp = time.time() * 1000 # milliseconds
        for i in range(0, num_of_items):
            for j in range(i+1, num_of_items):
                current_progress += 1
                timestamp_now = time.time() * 1000 # milliseconds
                if timestamp_now - previous_update_timestamp >= refresh_rate_ms:
                    previous_update_timestamp = timestamp_now
                    on_progress_update({
                        "current_progress": current_progress,
                        "total_progress": total_progress
                    })
        on_progress_update({
            "current_progress": current_progress,
            "total_progress": total_progress
        })
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