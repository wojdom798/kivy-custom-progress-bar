from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from .utils import rgba_to_color

PB_BACKGROUND_COLOR = rgba_to_color((33, 33, 33, 255))
PB_COLOR = rgba_to_color((0, 200, 81, 255))
# PB_COLOR = rgba_to_color((255, 136, 0, 255))

class ProgressBarCustom(Widget):
    def __init__(self, **kwargs):
        super(ProgressBarCustom, self).__init__(**kwargs)

        self.percent_complete = 0

        self.label_container = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size=self.size,
            pos=self.pos
        )
        self.add_widget(self.label_container)

        self.percent_complete_label = Label(
            text=self.get_label_text(self.percent_complete)
        )
        self.label_container.add_widget(self.percent_complete_label)

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()
    # *************************************************************
    # end: ProgressBarCustom.__init__()
    # *************************************************************
    def update_canvas(self, *args):
        with self.canvas.before:
            if self.parent:
                Color(
                    PB_BACKGROUND_COLOR[0], # R
                    PB_BACKGROUND_COLOR[1], # G
                    PB_BACKGROUND_COLOR[2], # B
                    PB_BACKGROUND_COLOR[3], # A
                    mode="rgba"
                )
                Rectangle(pos=(0, 0), size=(self.parent.size[0], self.parent.size[1]))
                Color(
                    PB_COLOR[0], # R
                    PB_COLOR[1], # G
                    PB_COLOR[2], # B
                    PB_COLOR[3], # A
                    mode="rgba"
                )
                Rectangle(
                    pos=(0, 0),
                    size=(
                        self.parent.size[0] * (self.percent_complete/100),
                        self.parent.size[1]
                    )
                )
                self.label_container.size = self.parent.size
                self.label_container.pos = self.parent.pos


    def set_percent_complete(self, percent_complete):
        if percent_complete > 100:
            percent_complete = 100
        elif percent_complete < 0:
            percent_complete = 0
        self.percent_complete = percent_complete
        self.percent_complete_label.text = self.get_label_text(self.percent_complete)
        self.update_canvas()


    def get_label_text(self, percent_complete):
        return "{0:.{1}f}% complete".format(percent_complete, 2)
# *************************************************************
# end: class ProgressBarCustom
# *************************************************************