
'''
Author: EkRamisa
25.04.18
A Browser bot using Selenium to crawl the Brac Academia website and carry out automated tasks
Bot V0.01
'''

from selenium import webdriver
import time
from TMemory import *

def Access_HomePage_And_Get_To_Seat_Page(username_, password_):

    print ('Initiating Bot v0.01..')
    driver = webdriver.Chrome('C:\\Users\\ekram\\Downloads\\chromedriver.exe')
    driver.get('http://usis.bracu.ac.bd/academia/')
    #i love ekram <3
    #Login Page: Automate the login procedure
    print ('Attempting to automate login..')
    login_username_box = driver.find_element_by_id('username')
    login_password_box = driver.find_element_by_id('password')
    login_button = driver.find_element_by_id('ctl00_leftColumn_ctl00_btnLogin')
            

    #Now fill in the login boxes with the user credentials/ Place input quotes here later to make this a user variable
    login_username_box.send_keys(username_)
    login_password_box.send_keys(password_)     # lol xD
    login_button.click()

    print ('Login Successful.Loading HomePage..')

    #wait 1 second for the page to load
    print ('1 second break to allow Page load..')
    time.sleep(1)

    #Home Page: Automate to the next task
    HomePage_URL = driver.current_url
    print ('Current HomePage URL is: ' + HomePage_URL)

    # Advising_Panel_Element = driver.find_element_by_id('student-advising-panel-left-menu')

    Seat_Status_URL = HomePage_URL + '#/academia/studentCourse/showCourseStatusByStudent'
    print ('Clicking on Seat Status Link..')
    driver.get(Seat_Status_URL)

    time.sleep(2)

    return (driver)

def Setup_SeatPage_For_Loop_Automation(driver, Year_, Session_, Course_):

    # #USER DEFINED VARIABLES
    Advising_Year_String = Year_
    User_Session_String = Session_
    Course_Code_String = Course_

    Advising_Year_Element = driver.find_element_by_name('academiaYear.id')
    Advising_Year_Element.send_keys(Advising_Year_String)

    User_Session_Element = driver.find_element_by_id('academiaSession')
    User_Session_Element.send_keys(User_Session_String)

    Course_Code_Element = driver.find_element_by_id('queryCourseStatus')
    Course_Code_Element.send_keys(Course_Code_String)

    Search_Button_Element = driver.find_element_by_id('search-button')
    Search_Button_Element.click()

    Loading_Element = driver.find_element_by_id('load_jqgrid-grid-studentStatusCourseList')

    while True:

        Loading_Element_Display_Property_String =  Loading_Element.is_displayed()
        print ('Still Loading..')
        time.sleep(1)

        Var_Restart = Read_Single_Data('Restart_Boolean')
        if Var_Restart=='Yes':
            print ('Hit restart boolean. Restarting script to standby mode')
            break

        if Loading_Element_Display_Property_String==False:
            print ('Loading has finished..')
            break

    print ('Out of loop')
    Search_Button_Element.click()

    time.sleep(2)

    return (driver)

def Refresh_Seat_Page(driver):

    Search_Button_Element = driver.find_element_by_id('search-button')
    Search_Button_Element.click()

    Loading_Element = driver.find_element_by_id('load_jqgrid-grid-studentStatusCourseList')

    while True:

        Loading_Element_Display_Property_String =  Loading_Element.is_displayed()
        print ('Still Loading..')
        time.sleep(1)

        if Loading_Element_Display_Property_String==False:
            print ('Loading has finished..')
            break

    print ('Out of loop')
    Search_Button_Element.click()

    time.sleep(1)

    return (driver)


def Scrape_The_Table_For_Multi_Array(driver):

    Main_Table_Element = driver.find_element_by_id('jqgrid-grid-studentStatusCourseList')
    Tr_Element = Main_Table_Element.find_elements_by_tag_name('tr')

    Tr_Element.pop(0) #Get rid of dummy first element

    Outer_Table_Array = []

    count = 1
    for tr in Tr_Element:
        print ('Starting on row: ' + str(count))
        td_element = tr.find_elements_by_tag_name('td')

        temporary_array = []

        for td in td_element:
            inner_text = td.get_attribute('innerHTML')
            temporary_array.append(inner_text)
            print (inner_text)

        Outer_Table_Array.append(temporary_array)
        count = count + 1
        print ('')

    print ('Now lets see the table we have..')

    for line in Outer_Table_Array:
        print (line)
        print ('')

    return (Outer_Table_Array)








