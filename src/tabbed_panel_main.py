from kivy.uix.tabbedpanel import TabbedPanel

from .demo_tab import DemoTab
from .notifications_tab import NotificationsTab

class TabbedPanelMain(TabbedPanel):
    def __init__(self, **kwargs):
        super(TabbedPanelMain, self).__init__(**kwargs)
        self.do_default_tab = False

        self.demo_tab = DemoTab()
        self.add_widget(self.demo_tab)

        self.notifications_tab = NotificationsTab()
        self.add_widget(self.notifications_tab)
    # *************************************************************
    # end: TabbedPanelMain.__init__()
    # *************************************************************
    def get_demo_tab_callbacks(self):
        return self.demo_tab.get_callbacks()

    def get_comparison_sim_update_handlers(self):
        return self.demo_tab.get_comparison_sim_update_handlers()

    def emit_notification(self, notification_data):
        self.notifications_tab.emit_notification(notification_data)

    def set_button_demo_default_step_value(self, value):
        self.demo_tab.set_button_demo_default_step_value(value)
# *************************************************************
# end: class TabbedPanelMain
# *************************************************************