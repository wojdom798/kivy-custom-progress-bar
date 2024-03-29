from enum import Enum

from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput

from kivy.graphics import Rectangle
from kivy.graphics import Color

from kivy.animation import Animation

from .utils import rgba_to_color


class ActiveSubmenuEnum(Enum):
    NONE = "NONE"
    INCREASE_PROGRESS_WITH_BUTTON = "INCREASE_PROGRESS_WITH_BUTTON"
    INCREASE_PROGRESS_WITH_SLIDER = "INCREASE_PROGRESS_WITH_SLIDER"
    COMPARISON_SIMULATION = "COMPARISON_SIMULATION"


class DemoTab(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(DemoTab, self).__init__(**kwargs)
        self.text = "Demo"

        self.callbacks = {
            "increase_progress_button_click_cb": None,
            "set_button_click_step_value_cb": None,
            "progress_slider_value_change_cb": None,
            "start_simulation_cb": None,
            "set_simulation_num_of_items_cb": None,
            "abort_simulation_cb": None,
        }

        # self.main_container = AnchorLayout(
        #     anchor_x="center",
        #     anchor_y="center",
        #     size_hint=(1, 1)
        # )
        self.main_container = BoxLayout(
            size_hint=(1, 1)
        )
        self.add_widget(self.main_container)

        # self.increase_progress_button = Button(
        #     text="click to increase progress",
        #     size=(190, 50),
        #     size_hint=(None, None),
        #     on_release=lambda button_instance: \
        #         self.handle_increase_progress_button_click(button_instance)
        # )
        # # self.main_container.add_widget(self.increase_progress_button)

        # self.progress_slider = Slider(
        #     size=(400, 50),
        #     size_hint=(None, None)
        # )
        # self.progress_slider.bind(value=self.handle_slider_value_change)
        # self.main_container.add_widget(self.progress_slider)

        self.submenu_button_container = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            padding=(200, 70),
            spacing=40
        )
        self.main_container.add_widget(self.submenu_button_container)

        self.increase_progress_with_button_menu_button = Button(
            text="Increase Progress With Button (submenu)",
            size_hint=(1, 1),
            on_release=lambda btn_instance: self.show_submenu(
                ActiveSubmenuEnum.INCREASE_PROGRESS_WITH_BUTTON
            )
        )
        self.submenu_button_container.add_widget(
            self.increase_progress_with_button_menu_button
        )

        self.increase_progress_with_slider_menu_button = Button(
            text="Increase Progress With Slider (submenu)",
            size_hint=(1, 1),
            on_release=lambda btn_instance: self.show_submenu(
                ActiveSubmenuEnum.INCREASE_PROGRESS_WITH_SLIDER
            )
        )
        self.submenu_button_container.add_widget(
            self.increase_progress_with_slider_menu_button
        )

        self.comparison_simulation_menu_button = Button(
            text="Comparison Simulation (submenu)",
            size_hint=(1, 1),
            on_release=lambda btn_instance: self.show_submenu(
                ActiveSubmenuEnum.COMPARISON_SIMULATION
            )
        )
        self.submenu_button_container.add_widget(
            self.comparison_simulation_menu_button
        )

        self.increase_progress_with_button_submenu = IncreaseProgressWithButtonSubmenu(
            on_return_click=lambda btn_instance: self.return_from_submenu(),
            on_progress_btn_click=lambda btn_instance: \
                self.handle_increase_progress_button_click(btn_instance),
            on_step_value_change=self.handle_button_step_value_change
        )
        # self.main_container.add_widget(self.increase_progress_with_button_submenu)
        
        self.increase_progress_with_slider_submenu = IncreaseProgressWithSliderSubmenu(
            on_return_click=lambda btn_instance: self.return_from_submenu(),
            on_slider_change=lambda value: \
                self.handle_slider_value_change(None, value)
        )
        
        self.comparison_simulation_submenu = ComparisonSimulationSubmenu(
            on_return_click=lambda btn_instance: self.return_from_submenu(),
            on_start_simulation_click=self.handle_start_simulation,
            on_num_of_items_change=lambda new_value: \
                self.handle_simulation_num_of_items_change(new_value),
            on_abort_simulation_click=lambda: self.handle_abort_simulation(),
        )
    # *************************************************************
    # end: DemoTab.__init__()
    # *************************************************************
    def show_submenu(self, submenu_enum):
        if submenu_enum == ActiveSubmenuEnum.INCREASE_PROGRESS_WITH_BUTTON:
            self.main_container.clear_widgets()
            self.main_container.add_widget(self.increase_progress_with_button_submenu)
        elif submenu_enum == ActiveSubmenuEnum.INCREASE_PROGRESS_WITH_SLIDER:
            self.main_container.clear_widgets()
            self.main_container.add_widget(self.increase_progress_with_slider_submenu)
        elif submenu_enum == ActiveSubmenuEnum.COMPARISON_SIMULATION:
            self.main_container.clear_widgets()
            self.main_container.add_widget(self.comparison_simulation_submenu)


    def return_from_submenu(self):
        self.main_container.clear_widgets()
        self.main_container.add_widget(self.submenu_button_container)
    

    def handle_increase_progress_button_click(self, button_instance):
        if "increase_progress_button_click_cb" in self.callbacks:
            self.callbacks["increase_progress_button_click_cb"]()
    

    def handle_button_step_value_change(self, new_value):
        condition = "set_button_click_step_value_cb" in self.callbacks and \
            self.callbacks["set_button_click_step_value_cb"] and \
            callable(self.callbacks["set_button_click_step_value_cb"])
        if condition:
            self.callbacks["set_button_click_step_value_cb"](new_value)

    
    def handle_slider_value_change(self, instance, value):
        if "progress_slider_value_change_cb" in self.callbacks:
            self.callbacks["progress_slider_value_change_cb"](value)

    
    def handle_start_simulation(self):
        if "start_simulation_cb" in self.callbacks:
            self.callbacks["start_simulation_cb"]()

    
    def handle_simulation_num_of_items_change(self, new_value):
        condition = "set_simulation_num_of_items_cb" in self.callbacks and \
            self.callbacks["set_simulation_num_of_items_cb"] and \
            callable(self.callbacks["set_simulation_num_of_items_cb"])
        if condition:
            self.callbacks["set_simulation_num_of_items_cb"](new_value)

    
    def handle_abort_simulation(self):
        condition = "abort_simulation_cb" in self.callbacks and \
            self.callbacks["abort_simulation_cb"] and \
            callable(self.callbacks["abort_simulation_cb"])
        if condition:
            self.callbacks["abort_simulation_cb"]()


    def set_button_demo_default_step_value(self, value):
        self.increase_progress_with_button_submenu.set_default_step_value(value)


    def get_callbacks(self):
        return self.callbacks

    def get_comparison_sim_update_handlers(self):
        if self.comparison_simulation_submenu:
            return self.comparison_simulation_submenu.get_ui_update_handlers() 
# *************************************************************
# end: class DemoTab
# *************************************************************


class IncreaseProgressWithButtonSubmenu(BoxLayout):
    def __init__(
        self,
        on_return_click=None,
        on_progress_btn_click=None,
        on_step_value_change=None,
        **kwargs
    ):
        super(IncreaseProgressWithButtonSubmenu, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.on_return_click = on_return_click
        self.on_progress_btn_click = on_progress_btn_click
        self.on_step_value_change = on_step_value_change

        self.add_widget(SubmenuHeader(
            "Demo - Increase Progress With Button",
            lambda btn_instance: self.handle_submenu_return_btn_click(btn_instance),
            size_hint=(1, 0.10))
        )

        self.main_container = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 0.9)
        )
        self.add_widget(self.main_container)

        self.button_container = BoxLayout(
            orientation="vertical",
            size=(250, 100),
            size_hint=(None, None)
        )
        self.main_container.add_widget(self.button_container)

        self.increase_progress_button = Button(
            text="click to increase progress",
            size_hint=(1, 1),
            on_release=lambda button_instance: \
                self.handle_increase_progress_button_click(button_instance)
        )
        self.button_container.add_widget(self.increase_progress_button)

        step_value_container = GridLayout(
            cols=2,
            size_hint=(1, 1)
        )
        self.button_container.add_widget(step_value_container)

        step_value_label = Label(
            text="step value",
            size_hint=(0.8, 1)
        )
        step_value_container.add_widget(step_value_label)

        self.step_value_input = TextInput(
            text="",
            size_hint=(0.2, 1),
            multiline=False,
            halign="center"
        )
        step_value_container.add_widget(self.step_value_input)
        self.step_value_input.bind(text=self.handle_step_value_input_change)
    # *************************************************************
    # end: IncreaseProgressWithButtonSubmenu.__init__()
    # *************************************************************
    def handle_submenu_return_btn_click(self, button_instance):
        if self.on_return_click and callable(self.on_return_click):
            self.on_return_click(button_instance)


    def handle_increase_progress_button_click(self, button_instance):
        if self.on_progress_btn_click and callable(self.on_progress_btn_click):
            self.on_progress_btn_click(button_instance)


    def handle_step_value_input_change(self, textfield_instance, text):
        if self.on_step_value_change and callable(self.on_step_value_change):
            converted_value = None
            try:
                converted_value = int(text)
                if converted_value < 1:
                    converted_value = None
            except Exception as e:
                converted_value = None
            self.on_step_value_change(converted_value)


    def set_default_step_value(self, value):
        self.step_value_input.text = str(value)
# *************************************************************
# end: class IncreaseProgressWithButtonSubmenu
# *************************************************************


class IncreaseProgressWithSliderSubmenu(BoxLayout):
    def __init__(self, on_return_click=None, on_slider_change=None, **kwargs):
        super(IncreaseProgressWithSliderSubmenu, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.on_return_click = on_return_click
        self.on_slider_change = on_slider_change

        self.add_widget(SubmenuHeader(
            "Demo - Increase Progress With Slider",
            lambda btn_instance: self.handle_submenu_return_btn_click(btn_instance),
            size_hint=(1, 0.10))
        )

        self.slider_container = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 0.9)
        )
        self.add_widget(self.slider_container)

        self.progress_slider = Slider(
            size=(400, 50),
            size_hint=(None, None)
        )
        self.progress_slider.bind(value=self.handle_slider_value_change)
        self.slider_container.add_widget(self.progress_slider)
    # *************************************************************
    # end: IncreaseProgressWithSliderSubmenu.__init__()
    # *************************************************************
    def handle_submenu_return_btn_click(self, button_instance):
        if self.on_return_click and callable(self.on_return_click):
            self.on_return_click(button_instance)

    def handle_slider_value_change(self, instance, value):
        if self.on_slider_change and callable(self.on_slider_change):
            self.on_slider_change(value)
# *************************************************************
# end: class IncreaseProgressWithSliderSubmenu
# *************************************************************


class ComparisonSimulationSubmenu(BoxLayout):
    def __init__(
        self,
        on_return_click=None,
        on_start_simulation_click=None,
        on_num_of_items_change=None,
        on_abort_simulation_click=None,
        **kwargs
    ):
        super(ComparisonSimulationSubmenu, self).__init__(**kwargs)
        self.orientation = "vertical"

        self.on_return_click = on_return_click
        self.on_start_simulation_click = on_start_simulation_click
        self.on_num_of_items_change = on_num_of_items_change
        self.on_abort_simulation_click = on_abort_simulation_click

        self.is_button_active = True

        self.add_widget(SubmenuHeader(
            "Demo - Comparison Simulation",
            lambda btn_instance: self.handle_submenu_return_btn_click(btn_instance),
            size_hint=(1, 0.10))
        )

        self.centering_container = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 0.9)
        )
        self.add_widget(self.centering_container)

        self.main_container = BoxLayout(
            orientation="vertical",
            size=(400, 150),
            size_hint=(None, None),
            spacing=10
        )
        self.centering_container.add_widget(self.main_container)

        num_of_comparisons_container = GridLayout(
            cols=2,
            size_hint=(1, 1)
        )
        self.main_container.add_widget(num_of_comparisons_container)

        num_of_comparisons_label = Label(
            text="number of comparisons",
            size_hint=(0.8, 1)
        )
        num_of_comparisons_container.add_widget(num_of_comparisons_label)

        self.num_of_comparisons_input = TextInput(
            text="",
            size_hint=(0.2, 1),
            multiline=False,
            halign="center"
        )
        num_of_comparisons_container.add_widget(self.num_of_comparisons_input)
        self.num_of_comparisons_input.bind(
            text=self.handle_num_of_comparisons_input_change
        )

        self.start_simulation_button = Button(
            text="start simulation",
            on_release=lambda btn_instance: \
                self.handle_start_simulation_btn_click(btn_instance)
        )
        self.main_container.add_widget(self.start_simulation_button)

        self.abort_simulation_button = Button(
            text="abort simulation",
            on_release=lambda btn_instance: \
                self.handle_abort_simulation_btn_click(btn_instance)
        )
        self.main_container.add_widget(self.abort_simulation_button)
    # *************************************************************
    # end: ComparisonSimulationSubmenu.__init__()
    # *************************************************************
    def handle_submenu_return_btn_click(self, button_instance):
        if self.on_return_click and callable(self.on_return_click):
            self.on_return_click(button_instance)

    
    def handle_num_of_comparisons_input_change(self, textfield_instance, text):
        if self.on_num_of_items_change and callable(self.on_num_of_items_change):
            converted_value = None
            try:
                converted_value = int(text)
                if converted_value < 1:
                    converted_value = None
            except Exception as e:
                converted_value = None
            self.on_num_of_items_change(converted_value)


    def handle_start_simulation_btn_click(self, button_instance):
        condition = self.on_start_simulation_click \
            and callable(self.on_start_simulation_click) \
            and self.is_button_active
        if condition:
            # self.is_button_active = False
            self.play_button_animation(button_instance)
            self.on_start_simulation_click()


    def handle_abort_simulation_btn_click(self, button_instance):
        condition = self.on_abort_simulation_click \
            and callable(self.on_abort_simulation_click) \
            and not self.is_button_active
        if condition:
            self.on_abort_simulation_click()


    def play_button_animation(self, button_instance):
        # if active then play the disable animation
        if self.is_button_active:
            button_animation = Animation(
                background_color=rgba_to_color((255, 10, 10, 255)),
                duration=0.2
            )
            button_animation.start(button_instance)
        else:
            button_animation = Animation(
                background_color=rgba_to_color((255, 255, 255, 255)),
                duration=0.2
            )
            button_animation.start(button_instance)


    def set_start_simulation_button_enabled(self, enabled):
        if type(enabled) == bool:
            self.play_button_animation(self.start_simulation_button)
            self.is_button_active = enabled
            # print("self.is_button_active = {}".format(self.is_button_active))
    

    def get_ui_update_handlers(self):
        return {
            "set_start_simulation_button_enabled": \
                self.set_start_simulation_button_enabled
        }
# *************************************************************
# end: class ComparisonSimulationSubmenu
# *************************************************************


class SubmenuHeader(BoxLayout):
    def __init__(self, submenu_name, on_return_click, **kwargs):
        super(SubmenuHeader, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = (5, 4)
        self.color = rgba_to_color((33, 33, 33, 255))

        self.return_button = Button(
            text="< go back",
            size_hint=(0.20, 1),
            on_release=lambda btn_instance: on_return_click(btn_instance)
        )
        self.add_widget(self.return_button)

        self.label = Label(text=submenu_name)
        self.add_widget(self.label)

        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()
    # *************************************************************
    # end: SubmenuHeader.__init__()
    # *************************************************************
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2], self.color[3], mode="rgba")
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.remove_widget(self.return_button)
        self.remove_widget(self.label)
        self.add_widget(self.return_button)
        self.add_widget(self.label)
# *************************************************************
# end: class SubmenuHeader
# *************************************************************