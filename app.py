from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
Window.size = (650, 250)
import winreg
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivymd.app import MDApp
import subprocess
from kivymd.uix.menu import MDDropdownMenu
import webbrowser

Builder.load_file('interface.kv')

class Interface(MDScreen):
    def on_pre_enter(self, *args):
        self.change_icon()

    def open_defender_settings(self):
        subprocess.Popen('start windowsdefender://Threatsettings',shell=True)

    def open_defender(self):
        subprocess.Popen('start windowsdefender:',shell=True)

    def disable_antivirus(self):
        try:
            antivirus = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Policies\Microsoft\Windows Defender")
            winreg.SetValueEx(antivirus, "DisableAntiSpyware",
                              0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(antivirus, "DisableAntivirus",
                              0, winreg.REG_DWORD, 1)
            winreg.CloseKey(antivirus)
            self.change_icon()
        except Exception as e:
            print(e)

    def enable_antivirus(self):
        try:
            antivirus = winreg.CreateKeyEx(
                winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\Policies\Microsoft\Windows Defender")
            winreg.DeleteValue(antivirus, "DisableAntiSpyware")
            winreg.DeleteValue(antivirus, "DisableAntivirus")
            winreg.CloseKey(antivirus)
            self.change_icon()
        except Exception as e:
            print(e)

    def change_icon(self, *args):
        if self.check_reg():
            self.ids.def_label.text = "windows Defender is enabled"
            self.ids.button_image.source = "true.png"
        else:
            self.ids.def_label.text = "windows Defender is disabled"
            self.ids.def_label.color = "red"
            self.ids.button_image.source = "false.png"

    def check_reg(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,"SOFTWARE\Policies\Microsoft\Windows Defender")
            winreg.QueryValueEx(key, "DisableAntiSpyware")
            winreg.QueryValueEx(key, "DisableAntivirus")
            winreg.CloseKey(key)
            return False
        except:
            return True
        
    
    def dropdown(self):
        self.menu_dict = [
        {
            "viewclass":"OneLineListItem",
            "text": "defender settings",
            "on_release": lambda x = "defender settings": self.open_defender_settings()
        },
        {
            "viewclass":"OneLineListItem",
            "text": "Refresh",
            "on_release": lambda x = "Refresh": self.change_icon() 
        },
        {
            "viewclass":"OneLineListItem",
            "text": "Donate",
            "on_release": lambda x = "Donate": self.donate() 
        },
        {
            "viewclass":"OneLineListItem",
            "text": "Contact Us",
            "on_release": lambda x = "Donate": self.discord() 
        },
        {
            "viewclass":"OneLineListItem",
            "text": "Help",
            "on_release": lambda x = "Donate": self.discord() 
        },
        {
            "viewclass":"OneLineListItem",
            "text": "Homepage",
            "on_release": lambda x = "Donate": self.website() 
        },
        {
            "viewclass":"OneLineListItem",
            "text": "About"
        }
        ]
        self.menu = MDDropdownMenu(caller = self.ids.dropdown,items = self.menu_dict,width_mult = 3)
        self.menu.open()

    
    def donate(self):
        webbrowser.open('https://paypal.me/furjack')

    def discord(self):
        webbrowser.open('https://discord.gg/YN9RKxewsq')

    def website(self):
        webbrowser.open("https://furjackgaming.blogspot.com/")


class DefCon(MDApp):
    def build(self):
        self.icon = 'img.ico'
        self.screen = ScreenManager()
        self.interface = Interface()
        self.screen.add_widget(self.interface)
        return self.screen


DefCon().run()


