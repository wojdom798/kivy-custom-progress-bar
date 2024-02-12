from enum import Enum

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from kivy.graphics import Rectangle
from kivy.graphics import Color

from .utils import rgba_to_color


NOTIFICATION_TYPE_COLORS = {
    "success": (0, 200, 81, 255),
    "warning": (255, 187, 51, 255),
    "error": (255, 68, 68, 255),
    "info": (51, 181, 229, 255)
}

class NotificationEnum(Enum):
    SUCCESS = 1
    WARNING = 2
    ERROR = 3
    INFO = 4


class NotificationsTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(NotificationsTab, self).__init__(**kwargs)
        self.text = "Notifications"

        # self.temporary_label = Label(
        #     text="[size=20]Notifications Tab is not implemented yet.[/size]",
        #     markup=True
        # )
        # self.add_widget(self.temporary_label)

        self.main_container = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            spacing=10,
            padding=(10, 10)
        )
        self.add_widget(self.main_container)

        test_notification_info = Notification({
            "type": NotificationEnum.INFO,
            "title": "Test Notification (Info)",
            "message": "This is a test info notification."
        })
        self.main_container.add_widget(test_notification_info)

        test_notification_success = Notification({
            "type": NotificationEnum.SUCCESS,
            "title": "Test Notification (Success)",
            "message": "This is a test success notification."
        })
        self.main_container.add_widget(test_notification_success)

        test_notification_warning = Notification({
            "type": NotificationEnum.WARNING,
            "title": "Test Notification (Warning)",
            "message": "This is a test warning notification."
        })
        self.main_container.add_widget(test_notification_warning)

        test_notification_error = Notification({
            "type": NotificationEnum.ERROR,
            "title": "Test Notification (Error)",
            "message": "This is a test error notification."
        })
        self.main_container.add_widget(test_notification_error)
    # *************************************************************
    # end: NotificationsTab.__init__()
    # *************************************************************
# *************************************************************
# end: class NotificationsTab
# *************************************************************


class NotificationLabel(Widget):
    def __init__(self, text="", color=(1, 1, 1, 1), **kwargs):
        super(NotificationLabel, self).__init__(**kwargs)
        self.color = rgba_to_color(color)

        self.centering_container = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size=self.size,
            pos=self.pos
        )
        self.add_widget(self.centering_container)

        self.label = Label(
            text=text
        )
        self.centering_container.add_widget(self.label)
        
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()
    # *************************************************************
    # end: NotificationLabel.__init__()
    # *************************************************************
    def update_canvas(self, *args):
        with self.canvas.before:
            Color(
                self.color[0],
                self.color[1],
                self.color[2],
                self.color[3],
                mode="rgba"
            )
            Rectangle(
                pos=self.pos,
                size=self.size,
                pos_hint=(0, 0),
                size_hint=(1, 1)
            )
            self.centering_container.size = self.size
            self.centering_container.pos = self.pos
# *************************************************************
# end: class NotificationLabel
# *************************************************************


class Notification(GridLayout):
    def __init__(
            self,
            notification_data,
            spacing=0,
            on_more_info_button_click=None,
            **kwargs
        ):
        super(Notification, self).__init__(**kwargs)
        self.cols = 2

        self.spacing = spacing
        self.bg_color = rgba_to_color((62, 69, 81, 255))

        self.notification_data = notification_data
        self.type = notification_data["type"]
        self.on_more_info_button_click = on_more_info_button_click
        
        self.type_icon = NotificationLabel(
            text=self.set_notification_label_text(self.type),
            color=self.get_notification_color(),
            size_hint=(0.25, 1)
        )
        self.add_widget(self.type_icon)

        self.right_side_container = BoxLayout(
            orientation="vertical",
            spacing=spacing/2
        )
        self.add_widget(self.right_side_container)

        self.notification_title = Label(
            text="[size=20]{}[/size]".format(notification_data["title"]),
            markup=True
        )
        self.right_side_container.add_widget(self.notification_title)

        self.message_container = GridLayout(cols=2)
        self.right_side_container.add_widget(self.message_container)

        self.message_truncated = Label(
            text=notification_data["message"][0:70] + "..." if \
                len(notification_data["message"]) > 70 else \
                notification_data["message"]
        )
        self.message_container.add_widget(self.message_truncated)

        self.notification_show_more_button = Button(
            text="more",
            on_release=self.handle_more_info_button_click,
            size_hint=(0.1, 1)
        )
        self.message_container.add_widget(self.notification_show_more_button)
        
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()
    # *************************************************************
    # end: Notification.__init__()
    # *************************************************************
    def update_canvas(self, *args):
        with self.canvas.before:
            Color(
                self.bg_color[0],
                self.bg_color[1],
                self.bg_color[2],
                self.bg_color[3],
                mode="rgba"
            )
            Rectangle(pos=self.pos, size=self.size)


    def get_notification_color(self):
        if self.type == NotificationEnum.INFO:
            return NOTIFICATION_TYPE_COLORS["info"]
        if self.type == NotificationEnum.SUCCESS:
            return NOTIFICATION_TYPE_COLORS["success"]
        if self.type == NotificationEnum.WARNING:
            return NOTIFICATION_TYPE_COLORS["warning"]
        if self.type == NotificationEnum.ERROR:
            return NOTIFICATION_TYPE_COLORS["error"]


    def set_notification_label_text(self, notification_type):
        if notification_type == NotificationEnum.INFO:
            return "info"
        if notification_type == NotificationEnum.SUCCESS:
            return "success"
        if notification_type == NotificationEnum.WARNING:
            return "warning"
        if notification_type == NotificationEnum.ERROR:
            return "error"


    def handle_more_info_button_click(self, button_instance):
        if self.on_more_info_button_click and callable(self.on_more_info_button_click):
            self.on_more_info_button_click(self.notification_data)
# *************************************************************
# end: class Notification
# *************************************************************