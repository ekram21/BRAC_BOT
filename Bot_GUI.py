'''
Author: Ekram
02.05.18
A GUI for the Browser bot using Selenium to crawl the Brac Academia website and carry out automated tasks
Bot V0.01
'''


import kivy
kivy.require('1.0.6') # replace with your current kivy version !
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import multiprocess
import TMemory
from Run import *

class BracBot(App):

    def build(self):
        '''Global Variables'''
        self.multiprocess_job_boolean = False

        '''OUTER ROOT WINDOW WIDGET'''
        Outer_Window = BoxLayout(orientation='vertical')

        '''HEADING LABEL'''
        Heading_Label = BoxLayout(orientation='vertical', size_hint=(1,0.5))
        Heading_Label.add_widget(Label(text='[size=40][b]BRAC BOT V0.01[/b][/size]', markup=True))

        '''USER INPUT WINDOW'''
        Input_Window = GridLayout(cols=2) 

        Input_Window.add_widget(Label(text='User Name:', font_size=20))
        self.username = TextInput(multiline=False)
        Input_Window.add_widget(self.username)

        Input_Window.add_widget(Label(text='Password:', font_size=20))
        self.password = TextInput(password=True, multiline=False)
        Input_Window.add_widget(self.password)

        Input_Window.add_widget(Label(text='Year:', font_size=20))
        self.Year = TextInput(multiline=False)
        Input_Window.add_widget(self.Year)

        Input_Window.add_widget(Label(text='Session:', font_size=20))
        self.Session = TextInput(multiline=False)
        Input_Window.add_widget(self.Session)

        Input_Window.add_widget(Label(text='Course Code:', font_size=20))
        self.CourseCode = TextInput(multiline=False)
        Input_Window.add_widget(self.CourseCode)

        Input_Window.add_widget(Label(text='Sections:', font_size=20))
        self.Sections = TextInput(multiline=False)
        Input_Window.add_widget(self.Sections)

        Input_Window.add_widget(Label(text='Words to Filter Out:', font_size=20))
        self.Filter_Out = TextInput(multiline=False)
        Input_Window.add_widget(self.Filter_Out)

        '''USER INPUT BUTTON WINDOW'''
        Input_Buttons_Window = GridLayout(cols=2, size_hint=(1,0.4), padding=15) 

        Start_Button = Button(text='Start', font_size=20)  
        Input_Buttons_Window.add_widget(Start_Button)

        Start_Button.bind(on_press=self.Start_Button_Press)  

        Stop_Button = Button(text='Stop', font_size=20)
        Input_Buttons_Window.add_widget(Stop_Button)

        Stop_Button.bind(on_press=self.Stop_Button_Press)

        '''OUTPUT TEXT WINDOW'''
        self.Output_Label_Box = BoxLayout(orientation='vertical', size_hint=(1,0.3))
        Current_Action = TMemory.Read_Single_Data('Current_Action')
        self.Output_Label = Label(text='[size=20]' + Current_Action + '[/size]', markup=True)
        self.Output_Label_Box.add_widget(self.Output_Label)


        '''ADDING ALL CHILD WIDGETS TO PARENT'''
        Outer_Window.add_widget(Heading_Label)
        Outer_Window.add_widget(Input_Window)
        Outer_Window.add_widget(Input_Buttons_Window)
        Outer_Window.add_widget(self.Output_Label_Box)

        '''loading sound alert when seat is found'''
        self.alert_sound = SoundLoader.load('Alert.wav')

        '''Setting up looping event'''
        Update_Output_Label_Event = Clock.schedule_interval(self.Update_Current_Action_Label, 1.)
        print (Update_Output_Label_Event)

        return (Outer_Window)

    def Start_Button_Press(self, instance):

        print ('Starting Script with input values..')

        Input_List_Memory = []

        Username_Input_String = self.username.text
        Password_Input_String = self.password.text
        Year_Input_String = self.Year.text
        Session_Input_String = self.Session.text
        CourseCode_Input_String = self.CourseCode.text
        Sections_Input_String = self.Sections.text
        FilterOut_Input_String = self.Filter_Out.text

        Input_List_Memory.append(Username_Input_String)
        Input_List_Memory.append(Password_Input_String)
        Input_List_Memory.append(Year_Input_String)
        Input_List_Memory.append(Session_Input_String)        
        Input_List_Memory.append(CourseCode_Input_String)
        Input_List_Memory.append(Sections_Input_String)
        Input_List_Memory.append(FilterOut_Input_String)

        TMemory.Store_List_Data('Brac_Bot_Input_Data', Input_List_Memory)

        #Start the Brac Scraping script in async mode
        self.Async_Start_BracScript()


    def Stop_Button_Press(self, instance):

        print ('Stopping..')
        TMemory.Store_Single_Data('Current_Action', 'Script stopped. Ready to be restarted again..')
        if self.multiprocess_job_boolean:
            self.p.terminate()
            self.p.join()
            self.multiprocess_job_boolean = False

    def Async_Start_BracScript(self):
        self.p = multiprocess.Process(target = BracBot_MainLooping_Script)
        self.p.start()
        self.multiprocess_job_boolean = True

    def Update_Current_Action_Label(self, dt):
        #print ('Updating Current Action Label..')
        self.Output_Label_Box.clear_widgets(children=None)

        Current_Action = TMemory.Read_Single_Data('Current_Action')

        self.Output_Label = Label(text='[size=20]' + Current_Action + '[/size]', markup=True)
        self.Output_Label_Box.add_widget(self.Output_Label)



if __name__ == '__main__':
    multiprocess.freeze_support()
    TMemory.Store_Single_Data('Current_Action', 'Started BRAC BOT V0.01. Hope this is useful to you 8) Made by Ekram')
    BracBot().run()
