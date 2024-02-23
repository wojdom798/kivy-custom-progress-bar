import threading
import time
from kivy.clock import mainthread as kivy_mainthread

from kivy.app import App
from kivy.core.window import Window as KivyWindow

from kivy.uix.boxlayout import BoxLayout

from src.progress_bar_custom import ProgressBarCustom
from src.tabbed_panel_main import TabbedPanelMain
from src.notifications_tab import NotificationEnum

DEFAULT_STEP_VALUE = 4

class AppMainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(AppMainLayout, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.button_click_count = 0
        self.button_click_step = DEFAULT_STEP_VALUE

        self.comparison_simulation_thread = None
        self.is_comparison_simulation_active = False

        self.main_tabbed_panel = TabbedPanelMain(size_hint=(1, 0.9))
        self.add_widget(self.main_tabbed_panel)

        self.main_tabbed_panel.set_button_demo_default_step_value(DEFAULT_STEP_VALUE)

        self.main_tabbed_panel.get_demo_tab_callbacks() \
            ["increase_progress_button_click_cb"] = \
            lambda: self.handle_increase_progress_button_click()

        self.main_tabbed_panel.get_demo_tab_callbacks() \
            ["set_button_click_step_value_cb"] = \
            lambda new_value: self.update_button_click_step_value(new_value)

        self.main_tabbed_panel.get_demo_tab_callbacks() \
            ["progress_slider_value_change_cb"] = \
            lambda new_value: self.set_progress_bar_value(new_value)

        self.main_tabbed_panel.get_demo_tab_callbacks() \
            ["start_simulation_cb"] =\
                lambda: self.handle_run_comparison_simulation_btn_click()


        self.progress_bar_container = BoxLayout(
            size_hint=(1, 0.1)
        )
        self.add_widget(self.progress_bar_container)

        self.progress_bar_custom = ProgressBarCustom(size_hint=(1, 1))
        self.progress_bar_container.add_widget(self.progress_bar_custom)
    # *************************************************************
    # end: AppMainLayout.__init__()
    # *************************************************************
    def handle_increase_progress_button_click(self):
        self.button_click_count += 1
        if self.button_click_count > self.button_click_step:
            self.button_click_count = 0
        self.progress_bar_custom.set_percent_complete(
            self.button_click_count * (100 / self.button_click_step)
        )
        # print("The test button was clicked {} times".format(self.button_click_count))


    def update_button_click_step_value(self, new_value):
        if new_value:
            self.button_click_count = 0
            self.button_click_step = new_value


    def set_progress_bar_value(self, new_value):
        self.progress_bar_custom.set_percent_complete(new_value)


    def handle_run_comparison_simulation_btn_click(self):
        # NUM_OF_ITEMS_TO_COMPARE = 10000
        NUM_OF_ITEMS_TO_COMPARE = 4000
        REFRESH_RATE_MS = 70

        if not self.is_comparison_simulation_active:
            self.is_comparison_simulation_active = True

            self.comparison_simulation_thread = threading.Thread(
                target=self.run_comparison_simulation,
                args=({
                    "num_of_items": NUM_OF_ITEMS_TO_COMPARE,
                    "progress_update_cb": lambda update_data: \
                        self.update_progressbar_threaded(update_data),
                    "progress_refresh_rate": REFRESH_RATE_MS
                },)
            )
            self.comparison_simulation_thread.start()

            sim_check_thread = threading.Thread(
                target=self.check_comparison_simulation_finished
            )
            sim_check_thread.start()


    def run_comparison_simulation(self, simulation_data):
        self.main_tabbed_panel.get_comparison_sim_update_handlers() \
            ["set_start_simulation_button_enabled"](False)

        self.emit_notification_mainthread({
            "type": NotificationEnum.INFO,
            "title": "Starting Comparison Simulation",
            "message": "Number of items to compare: {}".format(
                simulation_data["num_of_items"]
            )
        })

        try:
            self.simulate_comparisons(
                simulation_data["num_of_items"],
                simulation_data["progress_update_cb"],
                refresh_rate_ms=simulation_data["progress_refresh_rate"]
            )

            self.emit_notification_mainthread({
                "type": NotificationEnum.SUCCESS,
                "title": "Comparison Simulation Finished",
                "message": "The simulation has been performed successfully."
            })

        except Exception as e:
            self.emit_notification_mainthread({
                "type": NotificationEnum.ERROR,
                "title": "Comparison Simulation Error",
                "message": "{}".format(e)
            })
        
    
    def check_comparison_simulation_finished(self):
        while (self.comparison_simulation_thread.is_alive()):
            time.sleep(0.1) # 100 ms
        self.perform_comparison_simulation_cleanup()


    @kivy_mainthread
    def perform_comparison_simulation_cleanup(self):
        self.is_comparison_simulation_active = False
        self.main_tabbed_panel.get_comparison_sim_update_handlers() \
                ["set_start_simulation_button_enabled"](True)


    @kivy_mainthread
    def emit_notification_mainthread(self, notification_data):
        self.main_tabbed_panel.emit_notification(notification_data)


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