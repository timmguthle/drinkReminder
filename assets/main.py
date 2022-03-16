import kivy
from datetime import datetime
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.uix.screenmanager import FadeTransition, SlideTransition
from kivy.core.window import Window
Window.size = (400, 600)

class MyDesign(FloatLayout):
    pass


class StartingScreen(Screen):

    def on_enter(self, *args):
        Clock.schedule_once(self.switch, 2)
        self.manager.transition = FadeTransition()

    def switch(self, dt):
        self.parent.current = 'main'



class ConfigWindow(Screen):
    menge = ObjectProperty(None)
    auf = ObjectProperty(None)
    ab = ObjectProperty(None)
    drinking_rate = 0

    def on_pre_enter(self, *args):
        if self.manager.get_screen('main').mystore.exists('my_config'):
            self.menge.text = str(self.manager.get_screen('main').mystore.get('my_config')['menge'])
            self.auf.value = self.manager.get_screen('main').mystore.get('my_config')['auf']
            self.ab.value = self.manager.get_screen('main').mystore.get('my_config')['ab']

    def btn(self):
        global drinking_rate
        a, b = int(self.auf.value), int(self.ab.value)
        if a < b:
            hours_awake = (24 - a) - (24 - b)
        elif a >= b:
            hours_awake = (24 - a) + b
        try:
            menge_int = int(self.menge.text)
        except ValueError:
            menge_int = 0
        drinking_rate = menge_int / hours_awake
        self.drinking_rate = drinking_rate

        self.manager.get_screen('main').mystore.put('my_config',
                                                    drinking_rate=int(self.drinking_rate),
                                                    menge=menge_int,
                                                    auf=a,
                                                    ab=b,
                                                    hours_awake=hours_awake)


class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):
    dr = ObjectProperty(None)
    sb_drunken = ObjectProperty(None)
    drunken = ObjectProperty(None)
    amount_add = ObjectProperty(None)
    wake_up_hour = 0
    drinking_rate = 0
    amount_drunken = 0
    mystore = JsonStore('assets/data.json')
    first_open = True
    monthday = datetime.now().strftime('%d')

    def add(self):
        self.amount_drunken += self.amount_add.value
        self.amount_add.value = 0
        self.drunken.text = f'Bis jetzt getrunken: \n {int(self.amount_drunken)}ml'
        self.mystore.put('user_data', amount_drunken=self.amount_drunken, day=self.monthday)


    def on_pre_enter(self, *args):
        global wake_up_date

        if self.monthday != self.mystore.get('user_data')['day']:
            self.amount_drunken = 0

        if self.first_open:
            if self.mystore.exists('my_config'):
                self.dr.text = f'drinking rate [ml/h]: \n {self.mystore.get("my_config")["drinking_rate"]}'
                self.wake_up_hour = self.mystore.get('my_config')['auf']
                self.drinking_rate = self.mystore.get('my_config')['drinking_rate']
            self.first_open = False
        else:
            try:
                self.dr.text = f'drinking rate [ml/h]: \n {int(self.manager.get_screen("config").drinking_rate)}'
                self.wake_up_hour = int(self.manager.get_screen('config').auf.value)
                self.drinking_rate = self.manager.get_screen('config').drinking_rate
            except kivy.uix.screenmanager.ScreenManagerException:
                pass

        now = datetime.now()
        today = now.strftime('%d %m %Y')
        if self.wake_up_hour < 10:
            wake_up_str = f'{today} 0{str(self.wake_up_hour)}'
        else:
            wake_up_str = f'{today} {str(self.wake_up_hour)}'

        wake_up_date = datetime.strptime(wake_up_str, '%d %m %Y %H')

        try:
            self.update_sb_drunken()
        except kivy.uix.screenmanager.ScreenManagerException:
            pass

    def update_sb_drunken(self):
        delta = datetime.now() - wake_up_date
        delta_h = round(delta.seconds / 3600, 2)
        sb = delta_h * self.drinking_rate
        if sb > int(self.manager.get_screen('config').menge.text):
            sb = int(self.manager.get_screen('config').menge.text)
        self.sb_drunken.text = f'Bis jetzt getrunken haben sollte: {int(sb)}ml'


    #Clock.schedule_interval(update_sb_drunken, 1)
    # Warum zum Teufel kann ich in der Funktion wenn ich sie mitels der Clock verwende keien self verwenden


kv = Builder.load_file('assets/kv_main.kv')


class MyApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MyApp().run()