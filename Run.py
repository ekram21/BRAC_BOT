

from Brac_Bot import *
from Misc import *
from TMemory import *
import time

Store_Single_Data('Seat_Availability_Boolean', 'No')

while True:
    '''Start in Standby Mode and Set Seat Availability to No'''
    Store_Single_Data('Run_Bot_Boolean', 'No')
    Store_Single_Data('Restart_Boolean', 'No')

    while True:

        Run_Boolean = Read_Single_Data('Run_Bot_Boolean')
        time.sleep(1)
        print ('On Standby...')

        if 'Yes' in Run_Boolean:
            break


    '''Start the BROWSER AND BRAC BOT SCRIPT'''

    #Read the input data from the whatsapp post
    try:
        Input_Data = Read_List_Data('Brac_Bot_Input_Data')
    except:
        print ('Error in Line 25 of Run.py. Skipping it')
        pass

    Username__ = 'ramisa.ib1@gmail.com' #Input_Data[0]
    Password__ = 'rameesa' #Input_Data[1]
    Year__ = '2018' #Input_Data[2]
    Session__ = 'Summer 2018' #Input_Data[3]

    CourseCode__ = Input_Data[0]
    Sections__ =  Input_Data[1]
    FilteredOut__ = Input_Data[2]

    Sections_As_List = []
    Manip_String = Sections__.split(';')
    for m in Manip_String:
        Sections_As_List.append(m)

    #Get to Seat page after logging in and everything
    driver = Access_HomePage_And_Get_To_Seat_Page(Username__, Password__)

    #Setup the seat page with inputs for course code and year etc
    Setup_SeatPage_For_Loop_Automation(driver, Year__, Session__, CourseCode__)


    '''Start daemon / loop here for refreshing the page and keep checking the seat availability'''
    count = 0
    while True:

        print ('On loop number: ' + str(count))
        count = count + 1

        try:
            Outer_Table_Array = Scrape_The_Table_For_Multi_Array(driver)
        except:
            Outer_Table_Array = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]

        print (Outer_Table_Array)

        '''Scraped the Table Data so now find if seat is available or not with filter inputs as the ones set by the user'''
        #Filter by Sections
        Table_Filtered_By_Sections = Get_Elements_With_Class_Sections(Outer_Table_Array, Sections_As_List)

        #Filter Out Unwanted words
        Table_Filtered_By_Sections_And_Words = Get_Rid_Of_Quoted_Elements(Table_Filtered_By_Sections, '(lab)')

        print ('Filtering concluded, now printing the filtered table')

        for line in Table_Filtered_By_Sections_And_Words:
            print (line)

        print ('Now checking to see if seat is available..')

        Check_Bool = Check_To_See_If_Seat_Available(Table_Filtered_By_Sections_And_Words)

        Var_Restart = Read_Single_Data('Restart_Boolean')
        if Var_Restart=='Yes':
            break

        if Check_Bool==True:
            print ('Seat is available, writing to shared memory and notifying the user in whatsapp...')
            Store_Single_Data('Seat_Availability_Boolean', 'Yes')
            break
        elif Check_Bool==False:
            print ('Seat unavailable, refreshing and re-running loop to keep checking..')
            Store_Single_Data('Seat_Availability_Boolean', 'No')
            Refresh_Seat_Page(driver)

