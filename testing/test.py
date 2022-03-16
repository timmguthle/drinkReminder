import kivy
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



# class Touch(Widget):
#     def on_touch_down(self, touch):
#         pass
#     def on_touch_move(self, touch):
#         pass
#     def on_touch_up(self, touch):
#         pass

# class Mygrid(GridLayout):
#     def __init__(self,**kwargs):
#         super(Mygrid, self).__init__(**kwargs)
#         self.rows  = 2
#
#         self.subgrid1 = GridLayout()
#         self.subgrid1.cols = 2
#
#         self.subgrid1.add_widget(Label(text='name: '))
#         self.name = TextInput(multiline=False)
#         self.subgrid1.add_widget(self.name)
#
#         self.add_widget(self.subgrid1)
#
#         self.submit = Button(text='Submit', font_size=30)
#         self.submit.bind(on_press=self.press)
#         self.add_widget(self.submit)

# class Mygrid(Widget):
#    name = ObjectProperty(None)

class MainW(Screen):
    pass

class SecondW(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('../assets/my.kv')


class MyMainapp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyMainapp().run()