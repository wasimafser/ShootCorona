from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

import random
import copy
import time
import traceback


class Entity(object):
    pass


class Target(object):
    pass


class Corona(Rectangle):
    def __init__(self, **kwargs):
        super(Corona, self).__init__(**kwargs)
        self.group = 'corona'
        self.pos = kwargs.pop('pos', [0, 0])
        self.size = kwargs.pop('size', [100, 100])
        self.source = "assets/images/corona.png"
        self.speed = random.randint(100, 200)
        Clock.schedule_interval(self.move_corona, 0)

    def move_corona(self, dt):
        if int(self.pos[1]) >= 0:
            y = self.pos[1] - self.speed * dt
            self.pos = [self.pos[0], y]


class GameWidget(Widget):
    target_pos = ListProperty([0, 0])
    corona_pos = ListProperty([100, 100])

    def __init__(self, *args, **kwargs):
        super(GameWidget, self).__init__(*args, **kwargs)
        self.coronas = set()
        self.counter = 0 # temp counter for testing
        self.load_entity_event = Clock.schedule_interval(self.load_entity, 1)
        Clock.schedule_interval(self.check_bottom_touch, 0)

    def check_bottom_touch(self, dt):
        bottom_touching_corona = None
        try:
            for corona in self.canvas.get_group('corona'):
                if corona.pos[1] <= 0:
                    bottom_touching_corona = corona
        except Exception as e:
            pass
        if bottom_touching_corona is not None:
            self.canvas.remove(bottom_touching_corona)

    def load_entity(self, dt):
        self.counter += 1
        if self.counter >= 10:
            self.load_entity_event.cancel()
        if len(self.canvas.get_group('corona')) <= 10:
            size_val = random.randint(50, 100)
            corona_pos = [random.randint(0, Window.width-size_val), Window.height]
            size = [size_val, size_val]
            corona_obj = Corona(pos=corona_pos, size=size)
            self.coronas.add(corona_obj)
            self.canvas.add(corona_obj)
        # self.check_bottom_touch(dt)

    def find_colliding_corona(self, touch):
        for corona in self.canvas.get_group('corona'):
            corona_range_x = range(int(corona.pos[0]), int(corona.pos[0])+int(corona.size[0]))
            corona_range_y = range(int(corona.pos[1]), int(corona.pos[1])+int(corona.size[1]))
            if int(touch.pos[0]) in corona_range_x and int(touch.pos[1]) in corona_range_y:
                return corona
        return False

    def on_touch_down(self, touch):
        self.target_pos = touch.pos
        corona_hit = self.find_colliding_corona(touch)
        if corona_hit:
            self.canvas.remove(corona_hit)


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
