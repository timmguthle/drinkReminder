import kivy
from datetime import datetime
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
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
from kivy.uix.CircularProgressBarr import CircularProgressBar
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.card import MDCard
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    FakeRectangularElevationBehavior,
    BackgroundColorBehavior
)

Window.size = (400, 600)

class MyDesign(FloatLayout):
    pass

class MyProgress(CircularProgressBar):
    pass

class RectangularElevationButton(
    RectangularRippleBehavior,
    FakeRectangularElevationBehavior,
    ButtonBehavior,
    BackgroundColorBehavior,
):
    pass


class MD3Card(MDCard, RoundedRectangularElevationBehavior):
    '''Implements a material design v3 card.'''
    pass


class StartingScreen(Screen):

    def on_enter(self, *args):
        Clock.schedule_once(self.switch, 2)
        self.manager.transition = FadeTransition()
        Clock.schedule_interval(self.animate, 0.05)


    def switch(self, dt):
        self.parent.current = 'main'

    def animate(self, dt):
        for Layout in self.children:
            for bar in Layout.children:
                if type(bar) == CircularProgressBar:
                    if bar.value < bar.max:
                        bar.value += 1
                    else:
                        bar.value = bar.min






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
        self.validate()

    def validate(self):
        try:
            x = int(self.menge.text)
            if x != 0:
                self.menge.error = False
            else:
                self.menge.error = True

        except ValueError:
            self.menge.error = True

    def btn(self):
        global drinking_rate
        self.validate()

        a, b = int(self.auf.value), int(self.ab.value)
        if a < b:
            hours_awake = (24 - a) - (24 - b)
        elif a >= b:
            hours_awake = (24 - a) + b
        try:
            if int(self.menge.text) != 0:
                menge_int = int(self.menge.text)
            else:
                menge_int = 1000
        except ValueError:
            menge_int = 1000
        drinking_rate = menge_int / hours_awake
        self.drinking_rate = drinking_rate

        self.manager.get_screen('main').mystore.put('my_config',
                                                    drinking_rate=int(self.drinking_rate),
                                                    menge=menge_int,
                                                    auf=a,
                                                    ab=b,
                                                    hours_awake=hours_awake)

    def reset_drunken(self):
        self.manager.get_screen('main').amount_drunken = 0
        self.manager.get_screen('main').mystore.put('user_data', amount_drunken=0, day=datetime.now().strftime('%d'))


class WindowManager(ScreenManager):
    pass


class MainWindow(Screen):
    dr = ObjectProperty(None)
    sb_drunken = ObjectProperty(None)
    drunken = ObjectProperty(None)
    amount_add = ObjectProperty(None)
    drunken_bar = ObjectProperty(None)
    sb_drunken_bar = ObjectProperty(None)
    deficit = ObjectProperty(None)
    btn_notification = ObjectProperty(None)
    notification = False
    wake_up_hour = 0
    drinking_rate = 0
    amount_drunken = 0
    sb = 0
    mystore = JsonStore('assets/data.json')
    first_open = True
    monthday = datetime.now().strftime('%d')

    def btn_noty(self):
        if self.notification:
            self.notification = False
            self.btn_notification.icon = 'bell-off-outline'
        else:
            self.notification = True
            self.btn_notification.icon = 'bell-outline'

    def add(self):
        self.amount_drunken += self.amount_add.value
        self.amount_add.value = 0
        self.drunken.text = f'Bis jetzt getrunken: \n [b]{int(self.amount_drunken)}[/b] ml'
        self.drunken_bar.value = (self.amount_drunken / int(self.manager.get_screen('config').menge.text)) * 100
        self.mystore.put('user_data', amount_drunken=self.amount_drunken, day=self.monthday)
        self.update_deficit()


    def on_pre_enter(self, *args):
        global wake_up_date

        if self.monthday != self.mystore.get('user_data')['day']:
            self.amount_drunken = 0
        else:
            self.amount_drunken = self.mystore.get('user_data')['amount_drunken']
        self.drunken.text = f'Bis jetzt getrunken: \n [b]{int(self.amount_drunken)}[/b] ml'
        self.drunken_bar.value = (self.amount_drunken / int(self.mystore.get('my_config')['menge'])) * 100

        if self.first_open:
            if self.mystore.exists('my_config'):
                self.dr.text = f'Trinkrate: \n [b]{self.mystore.get("my_config")["drinking_rate"]}[/b] ml/h'
                self.wake_up_hour = self.mystore.get('my_config')['auf']
                self.drinking_rate = self.mystore.get('my_config')['drinking_rate']
            self.first_open = False
        else:
            try:
                self.dr.text = f'Trinkrate: \n [b]{self.mystore.get("my_config")["drinking_rate"]}[/b] ml/h'
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

        self.update_deficit()

    def update_deficit(self):
        # positiv = mehr als noetig getrunken
        deficit_int = self.amount_drunken - int(self.sb)
        if deficit_int >= 0:
            self.deficit.text = f'Überschuss:\n[color=1ed421][b]{deficit_int}[/b][/color]'
        else:
            self.deficit.text = f'Defizit:\n[color=db1818][b]{deficit_int}[/b][/color]'

    def update_sb_drunken(self):
        delta = datetime.now() - wake_up_date
        delta_h = round(delta.seconds / 3600, 2)
        sb = delta_h * self.drinking_rate
        try:
            if sb > int(self.manager.get_screen('config').menge.text):
                sb = int(self.manager.get_screen('config').menge.text)
            self.sb_drunken.text = f'[b]{int(sb)}[/b] ml \n Solltest Du heute schon getrunken haben!'
            if int(self.manager.get_screen('config').menge.text) != 0:
                self.sb_drunken_bar.value = (int(sb) / int(self.manager.get_screen('config').menge.text)) * 100
            else:
                self.drunken_bar.value = 0
        except ValueError:
            sb = 0
        self.sb = sb



class MyApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "LightBlue"

        return Builder.load_file('assets/kv_main_MD.kv')


if __name__ == '__main__':
    MyApp().run()