from plyer import notification
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
import kivy

class MYDesign(Widget):

    def noty(self):
        notification.notify(title='kivy Notification', message='Das ist eine wichtige Nachricht')



kv = '''
MYDesign:
    BoxLayout:
        Button: 
            text: 'send Notification'
            on_press: root.noty()


'''

class MyApp(App):
    def build(self):
        return Builder.load_string(kv)


MyApp().run()