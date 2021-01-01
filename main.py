# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.storage.dictstore import DictStore
from kivy.uix.popup import Popup 


from datetime import datetime
from git import Git
import pickle, requests, os


BSIZE = 20
MAX_COMMIT = 100
UP_URL = 'mrlittle.heroku.app/gitpalette/update'
CR_INFO = '''
@Source Code
    Github - https://github.com/dmrlittle/gitpalette
                                    
@Author                      
    Email - shyamselvaraj@protonmail.com
    Github ID - dmrlittle
'''

class ParentLayout(BoxLayout):
    pass

class gitpaletteApp(App):
    ids={}
    selected_id = []
    g = None
    
    colourbutton = Button(background_color=[0, 1, 0, 1],
                                size_hint=(None, None), size=(20,20))
    pop = Popup(size_hint=(.8, .2), size=(500, 100))
    
    def __init__(self):
        super().__init__()
        self.dictstore = DictStore(filename=f'{self.user_data_dir}/defaults')
        self.dictstore.store_load()
        self.date = datetime.today().date()
        
    def build(self):
        self.icon = 'gitpalette.ico'

        layout1 = self.add_id(BoxLayout(orientation='vertical'), 'LT1')
        
        layout10 = StackLayout(orientation='lr-tb', padding=[0,20,20,0],
                               size_hint=(1,None),size=(30,80))
        
        popup = Popup(title='Details',
                      content=TextInput(text=CR_INFO, readonly = True),
                      size_hint=(None, None), size=(400, 400))
        
        layout10.add_widget(Label(text = f"Info! - Daily you used click on 'Initiate', Don't worry if you're a Active Github member, this can be Undone by deleting the repo.", size_hint=(0.9, .6), size=(150,50)))
        layout10.add_widget(Button(text = "Help",on_press= popup.open,
                                   background_color = [34/255.0,167/255.0,240/255.0,1],
                                   size_hint=(0.1, .6), size=(150,50)))

        
        layout100 = BoxLayout(orientation='vertical', padding=[20,0,20,0], size_hint=(1, None), size=(150,100))
        
        layout101 = StackLayout(orientation='lr-tb')
        layout101.add_widget(self.add_id(CheckBox(size_hint=(.03, .6), size=(30,30), group='radio1'),'UP'))
        layout101.add_widget(Label(text='Username', size_hint=(.1,.6), size=(100,30)))
        layout101.add_widget(self.add_id(TextInput(size_hint=(.2,.6), size=(100,30)),'TI1'))
        layout101.add_widget(Label(text='Password', size_hint=(.1,.6), size=(100,30)))
        layout101.add_widget(self.add_id(TextInput(size_hint=(.2, .6), size=(130,30)),'TI2'))
        
        layout102 = StackLayout(orientation='lr-tb')
        layout102.add_widget(self.add_id(CheckBox(size_hint=(.03, .6), active=True, size=(30,30), group='radio1'),'AU'))
        layout102.add_widget(Label(text='AuthCode', size_hint=(.1, .6), size=(100,30)))
        layout102.add_widget(self.add_id(TextInput(size_hint=(.5, .6), size=(370,30)),'TI3'))
        layout102.add_widget(Label(size_hint=(.02, .6), size=(30,30)))
        layout102.add_widget(self.add_id(Button(text='Connect', background_color=[0, 1, 0, 1],
                         on_press= self.bpress3, size_hint=(.1, .6), size=(100,30)),'BT'))
        layout100.add_widget(layout101)
        layout100.add_widget(layout102)
        
        layout11 =  GridLayout(orientation='tb-lr', rows=7, cols=54, padding=[20,20,20,20])
        start_day = datetime(self.date.year,1,1).weekday()+1
        [layout11.add_widget(Label()) for i in range(start_day)]
        for i in range(366 if (self.date.year%4 == 0 and self.date.year%100 != 0)  else 365):
            if i < int(self.date.strftime('%j'))-1 :
                layout11.add_widget(self.add_id(Button(disabled=True,
                                                on_press= self.bpress1),i))
            else:
                layout11.add_widget(self.add_id(Button(on_press= self.bpress1),i))
                
        layout12 = StackLayout(orientation='rl-tb', padding=[20,0,20,0], size_hint=(1, None), size=(150,20))
        
        layout12.add_widget(Label(text="Days Unavailable", size_hint=(None, None), size=(130,20)))
        layout12.add_widget(Button(disabled=True,
                                   size_hint=(None, None), size=(20,20)))
        layout12.add_widget(Label(text='Days Available', size_hint=(None, None), size=(130,20)))
        layout12.add_widget(Button(size_hint=(None, None), size=(20,20)))
        
        label2 = Label(text='Configurations', bold=True,
                       size_hint=(1, None), size=(150,50))
        
        layout13 = StackLayout(orientation='lr-tb', padding=[20,0,20,0], size_hint=(1, None), size=(150,50))
        layout13.add_widget(Label(text='Choose Colour - ', size_hint=(.13, None), size=(125,20)))
        for i in range(2, 11, 2):
            layout13.add_widget(Button(background_color=[0, 1, 0, i*0.1],
                                       on_press= self.bpress2,
                                       size_hint=(None, None), size=(20,20)))
        
        layout13.add_widget(Label(text='Selected Colour - ', size_hint=(None, None), size=(150,20)))
        layout13.add_widget(self.colourbutton)
        
        layout14 = StackLayout(orientation='lr-tb', padding=[20,0,20,0], size_hint=(1, None), size=(150,50))
        layout14.add_widget(Label(text="Today's Date - ", size_hint=(.12,.6), size=(125,20)))
        layout14.add_widget(self.add_id(TextInput(text=str(self.date.day), disabled = True, 
                                                  size_hint=(.035, .6), size=(370,30)),'DATED'))
        layout14.add_widget(self.add_id(TextInput(text=str(self.date.month), disabled = True, 
                                                  size_hint=(.035, .6), size=(370,30)),'DATEM'))
        layout14.add_widget(self.add_id(TextInput(text=str(self.date.year), disabled = True,
                                                  size_hint=(.06, .6), size=(370,30)),'DATEY'))
        layout14.add_widget(Label(size_hint=(.01,.6), size=(125,20)))
        layout14.add_widget(Button(text = 'Change', on_press = self.bpress6,
                                        size_hint=(.1, .6), size=(370,30)))
        layout14.add_widget(self.add_id(Label(size_hint=(.6,.6), size=(125,20)),'DATEE'))
                
        layout2 = BoxLayout(orientation='vertical', size_hint=(1, None), size=(150,50))
        
        layout15 = StackLayout(orientation='rl-tb', padding=[0,0,20,0])
        layout15.add_widget(self.add_id(Button(text = 'Save', disabled = True,
                                               on_press = self.bpress4,
                                               size_hint=(.11, None), size=(80,30)),'SB'))
        layout15.add_widget(Label(size_hint=(None, None), size=(10,30)))
        layout15.add_widget(self.add_id(Button(text = 'Initiate', disabled = True,
                                               on_press = self.bpress5,
                                               size_hint=(.11, None), size=(80,30)),'SB1'))
        layout15.add_widget(Label(size_hint=(None, None), size=(10,30)))
        layout15.add_widget(self.add_id(Button(text = 'From 0/100', disabled = True,
                                               on_press = self.bpress7,
                                               size_hint=(.11, None), size=(80,30)),'SB2'))
        layout15.add_widget(self.add_id(Label(text=f"0/100 Commits", size_hint=(None, None), size=(128,30)),'PBL'))
        layout15.add_widget(self.add_id(ProgressBar(max = MAX_COMMIT,
                                               size_hint=(.44, None), size=(710,30)),'PB'))
        layout15.add_widget(Label(text=f"Day - {self.date.strftime('%j')}" ,
                                  size_hint=(.09, None), size=(20,30)))
        

        layout1.add_widget(layout10)
        layout1.add_widget(layout100)
        layout1.add_widget(layout11)
        layout1.add_widget(layout12)
        layout1.add_widget(label2)
        layout1.add_widget(layout13)
        layout1.add_widget(layout14)
        layout2.add_widget(layout15)
        
        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(layout1)
        layout.add_widget(layout2)
        layout1.disabled = False
        
            
        return layout
    
    def on_start(self):
        try:
            self.sys_load()
            data = pickle.loads(requests.get(UP_URL))
            if(data != None):
                self.pop.title = data[0]
                self.pop.content = Label(text=data[1])
                self.pop.auto_dismiss = data[2]
                self.pop.open()
        except Exception as e:
            pass
    
    def sys_load(self):
        try:
            if(self.dictstore.store_exists(key=1)):
                self.selected_id = self.dictstore.store_get(key=1)
                for i in self.selected_id:
                    print(self.ids[i].background_color)
                    self.bpress1(self.ids[i])
            if(self.dictstore.store_exists(key=0)):
                self.g = self.dictstore.store_get(key=0)
                self.bpress3(self.ids['BT'])
                self.bpress4(self.ids['SB'])
            if(self.dictstore.store_exists(key=3)):
                if(self.dictstore.store_get(key=2) == self.date):
                    self.ids['PB'].value = self.dictstore.store_get(key=3)
        except:
            self.selected_id = []
            self.g = None
            self.ids['PB'].value = 0
        
    def bpress1(self,button):
        if(button.background_color == [1, 1, 1, 1]):
            button.background_color = self.colourbutton.background_color
            if self.get_id(button) not in self.selected_id:
                self.selected_id.append(self.get_id(button))
        else:
            button.background_color = [1, 1, 1, 1]
            self.selected_id.remove(self.get_id(button))

        print(self.selected_id)
    def bpress2(self,button):
        self.colourbutton.background_color=button.background_color

        
    def bpress3(self,button):
        try:
            
            if(button.text == 'Connect'):
                if(self.g != None):
                    pass
                elif(self.ids['UP'].active):
                    self.g = Git(self.ids['TI1'].text, self.ids['TI2'].text)
                else:
                    print('gf')
                    self.g = Git(self.ids['TI3'].text)
                    print('gf')
                if(self.g.check() != 0):
                    self.pop.title = 'Warning'
                    self.pop.content = Label(text=self.g.check())
                    self.pop.open()
                    self.g = None
                    return
                b = self.ids['BT']
                b.text = 'Disconnect'
                b.background_color = [1,0,0,1]
                self.ids['SB'].disabled = False
                self.ids['SB'].background_color = [0,1,0,1]
                
            else:
                self.g = None
                button.text = 'Connect'
                button.background_color = [0,1,0,1]
                self.ids['SB'].disabled = True
                self.ids['SB'].background_color = [1,1,1,1]
        except Exception as e:
            print(str())
                        
    def bpress4(self,button):
        if(button.text == 'Save'):
            if(self.g != None):
                self.g.create()
                self.dictstore.store_put(key=0,value=self.g)
                self.dictstore.store_put(key=1,value=self.selected_id)
                self.dictstore.store_put(key=2,value=self.date)
                self.dictstore.store_sync()
                button.disabled = False
                button.text = 'Abort'
                button.background_color = [1,0,0,1]
                self.ids['LT1'].disabled = True
                self.ids['SB1'].disabled = False
                self.ids['SB1'].background_color = [0,1,0,1]
                self.ids['SB2'].disabled = False
                self.ids['SB2'].background_color = [0,1,0,1]
            else:
                print('Failure !')
        else:
            button.disabled = False
            button.text = 'Save'
            button.background_color = [0,1,0,1]
            self.ids['LT1'].disabled = False    
            self.ids['SB1'].disabled = True
            self.ids['SB1'].background_color = [1,1,1,1]
            self.ids['SB2'].disabled = True
            self.ids['SB2'].background_color = [1,1,1,1]
            
            
    
    def bpress5(self, button):
        if(button.text == 'Pause'):
            button.text = 'Resume'
            button.background_color = [0,1,0,1]
            self.loadbar_stat = False
            self.ids['SB2'].disabled = False
        else:
            button.text = 'Pause'
            button.background_color = [0,0,1,1]
            self.loadbar_stat = True
            self.ids['SB2'].disabled = True
            self.loadbar = Clock.create_trigger(self.loader, 1)
            self.loadbar()
            
    def bpress6(self,button):
        if(button.text == 'Change'):
            self.ids['DATED'].disabled = False
            self.ids['DATEM'].disabled = False
            self.ids['DATEY'].disabled = False
            button.text = 'Save'
        else:
            self.ids['DATED'].disabled = True
            self.ids['DATEM'].disabled = True
            self.ids['DATEY'].disabled = True
            button.text = 'Change'
            try:
                assert int(self.ids['DATEY'].text)>2020, "Year should be after 2020"
                self.date = datetime(int(self.ids['DATEY'].text),
                     int(self.ids['DATEM'].text),
                     int(self.ids['DATED'].text))
                self.ids['DATEE'].text = 'Successfully Changed !'
                self.datechange()
            except ValueError:
                self.ids['DATEE'].text = 'Invalid Date !'
            except Exception as e:
                self.ids['DATEE'].text = str(e)
                
    def bpress7(self,button):
        self.ids['PBL'].text = f"0/100 Commits"
        self.ids['PB'].value = 0
        self.dictstore.store_put(key=3,value=self.ids['PB'].value)
        self.dictstore.store_sync()
        
    def datechange(self):
        for i in range(366 if (self.date.year%4 == 0 and self.date.year%100 != 0)  else 365):
            if i < int(self.date.strftime('%j'))-1 :
                self.ids[i].disabled = True
            else:
                self.ids[i].disabled = False
            
    def loader(self, dt):
        if self.ids['PB'].value < MAX_COMMIT and self.loadbar_stat:
            self.ids['PB'].value += 1
            if((int(self.date.strftime('%j'))-1) in self.selected_id):
                self.g.commit()
            self.dictstore.store_put(key=3,value=self.ids['PB'].value)
            self.dictstore.store_sync()
            self.ids['PBL'].text=f"{int(self.ids['PB'].value)}/100 Commits"
            self.loadbar()
               
    def add_id(self,widget,id):
        self.ids[id]=widget
        return widget
    
    def get_id(self,widget):
        for key,val in self.ids.items():
            if(val is widget):
                return key
        return None
    
    def on_stop(self):
        self.root_window.close()

def font_size(width, height):
    print(width,height)
    
def winclose(*args):
    print(90)
    
if __name__=="__main__":
    
    Window.size = (1210,590)
    Window.on_resize = font_size
    Window.set_icon("gitpalette.ico")
    
    obj = gitpaletteApp()
    obj.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
