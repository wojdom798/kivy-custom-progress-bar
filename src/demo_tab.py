from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

class DemoTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(DemoTab, self).__init__(**kwargs)
        self.text = "Demo"

        self.callbacks = {
            "increase_progress_button_click_cb": None
        }

        self.main_container = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 1)
        )
        self.add_widget(self.main_container)

        self.increase_progress_button = Button(
            text="click to increase progress",
            size=(190, 50),
            size_hint=(None, None),
            on_release=lambda button_instance: \
                self.handle_increase_progress_button_click(button_instance)
        )
        self.main_container.add_widget(self.increase_progress_button)
    # *************************************************************
    # end: DemoTab.__init__()
    # *************************************************************
    def handle_increase_progress_button_click(self, button_instance):
        if "increase_progress_button_click_cb" in self.callbacks:
            self.callbacks["increase_progress_button_click_cb"]()

    def get_callbacks(self):
        return self.callbacks
# *************************************************************
# end: class DemoTab
# *************************************************************