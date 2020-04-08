from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

import random
import copy


class Entity(object):
    pass


class Target(object):
    pass


class Corona(Rectangle):
    def __init__(self, **kwargs):
        super(Corona, self).__init__(**kwargs)
        self.pos = kwargs.pop('pos', [0, 0])
        self.size = kwargs.pop('size', [100, 100])
        self.source = "assets/images/corona.png"


class GameWidget(Widget):
    target_pos = ListProperty([0, 0])
    corona_pos = ListProperty([100, 100])

    def __init__(self, *args, **kwargs):
        super(GameWidget, self).__init__(*args, **kwargs)
        self.coronas = set()
        Clock.schedule_once(self.load_entity, 2)

    def load_entity(self, dt):
        for i in range(10):
            pos = [random.randint(0, Window.width), random.randint(0, Window.height)]
            size_val = random.randint(25, 100)
            size = [size_val, size_val]
            corona_obj = Corona(pos=pos, size=size)
            self.coronas.add(corona_obj)
            self.canvas.add(corona_obj)
            print("CORONA", i, pos, size)

    def on_touch_down(self, touch):
        self.target_pos = touch.pos
        temp_set = copy.copy(self.coronas)
        for corona in self.coronas:
            corona_range_x = range(int(corona.pos[0]), int(corona.pos[0])+int(corona.size[0]))
            corona_range_y = range(int(corona.pos[1]), int(corona.pos[1])+int(corona.size[1]))
            if touch.pos[0] in corona_range_x and touch.pos[1] in corona_range_y:
                print(corona_range_x, touch.pos[0])
                print("CORONA IS HIT")
                self.canvas.remove(corona)
                temp_set.remove(corona)
        self.coronas = temp_set


class GameScreen(Screen):
    pass
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)


class MainScreen(Screen):
    def start_game(self, *args):
        MDApp.get_running_app().sm.current = 'game_screen'


class ShootCorona(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen())
        self.sm.add_widget(GameScreen())
        return self.sm


if __name__ == '__main__':
    ShootCorona().run()
