from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color

class ProgressBarCustom(Widget):
    def __init__(self, **kwargs):
        super(ProgressBarCustom, self).__init__(**kwargs)

        self.percent_complete = 0

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()
    # *************************************************************
    # end: ProgressBarCustom.__init__()
    # *************************************************************
    def update_canvas(self, *args):
        with self.canvas.before:
            if self.parent:
                Color(33/255, 33/255, 33/255, 1, mode="rgba")
                Rectangle(pos=(0, 0), size=(self.parent.size[0], self.parent.size[1]))
                Color(0, 200/255, 81/255, 1, mode="rgba")
                Rectangle(
                    pos=(0, 0),
                    size=(
                        self.parent.size[0] * (self.percent_complete/100),
                        self.parent.size[1]
                    )
                )

    def set_percent_complete(self, percent_complete):
        if percent_complete > 100:
            percent_complete = 100
        elif percent_complete < 0:
            percent_complete = 0
        self.percent_complete = percent_complete
        self.update_canvas()
# *************************************************************
# end: class ProgressBarCustom
# *************************************************************