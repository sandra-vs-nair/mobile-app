# -----------------------------------------------------------
# Mobile Application logic
#
# (C) 2020 Sandra VS Nair, Trivandrum
# email sandravsnair@gmail.com
# -----------------------------------------------------------

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from json.decoder import JSONDecodeError
from datetime import datetime
import json, glob, random
from pathlib import Path

#For button-hover feature.
from hoverable import HoverBehavior

#Loading the kivy file.
Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen"
    def login(self,uname,pwd):
        #FIXME
        #json.load will fail if users.json is empty.
        with open("users.json") as file:
            users=json.load(file)
            if uname in users and users[uname]['password']==pwd:
                self.manager.current="login_success"
            else:
                self.ids.login_wrong.text='Invalid username or password'
                    
        
class LoginSuccessScreen(Screen):
    def logout(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"
    def display_quote(self,feel):
        feel=feel.lower()
        available_feelings=glob.glob("files/*txt")
        
        available_feelings=[Path(filename).stem for filename in available_feelings]
        
        if feel in available_feelings:
            with open(f"files/{feel}.txt",encoding="utf8") as file:
                quotes=file.readlines()
            self.ids.quote.text=random.choice(quotes)
        else:
            self.ids.quote.text="Try another feeling"
                
        
class SignupScreen(Screen):
    def add_user(self,uname,pwd):
        #FIXME
        #json.load will fail if users.json is empty.
        with open("users.json",'r+') as file:
            users=json.load(file)
            users[uname]={'username':uname,'password':pwd,
                             'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
            json.dump(users, file)   
        self.manager.current="sign_up_success"
        
class SignupSuccessScreen(Screen):
    def login_page(self):
        self.manager.transition.direction='right'
        self.manager.current="login_screen"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass
    
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__=="__main__":
    MainApp().run()
