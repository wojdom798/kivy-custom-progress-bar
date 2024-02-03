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
# *************************************************************
# end: class TabbedPanelMain
# *************************************************************