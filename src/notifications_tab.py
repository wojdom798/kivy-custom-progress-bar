from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.label import Label

class NotificationsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(NotificationsTab, self).__init__(**kwargs)
        self.text = "Notifications"

        self.temporary_label = Label(
            text="[size=20]Notifications Tab is not implemented yet.[/size]",
            markup=True
        )
        self.add_widget(self.temporary_label)
    # *************************************************************
    # end: NotificationsTab.__init__()
    # *************************************************************
# *************************************************************
# end: class NotificationsTab
# *************************************************************