

from Brac_Bot import *
from Misc import *
from TMemory import *
import Mail


def BracBot_MainLooping_Script():
    Store_Single_Data('Seat_Availability_Boolean', 'No')

    '''Start the BROWSER AND BRAC BOT SCRIPT'''

    #Read the input data from the GUI input
    try:
        Input_Data = Read_List_Data('Brac_Bot_Input_Data')
    except:
        print ('Error in Line 25 of Run.py. Skipping it')
        pass

    Username__ = Input_Data[0]
    Password__ = Input_Data[1]
    Year__ = Input_Data[2]
    Session__ = Input_Data[3]

    CourseCode__ = Input_Data[4]
    Sections__ =  Input_Data[5]
    FilteredOut__ = Input_Data[6]

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
        Store_Single_Data('Current_Action', 'On loop number: ' + str(count))

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
        print (FilteredOut__)
        Table_Filtered_By_Sections_And_Words = Get_Rid_Of_Quoted_Elements(Table_Filtered_By_Sections, str(FilteredOut__))

        print ('Filtering concluded, now printing the filtered table')
        Store_Single_Data('Current_Action', 'Filtering concluded..')

        for line in Table_Filtered_By_Sections_And_Words:
            print (line)

        print ('Now checking to see if seat is available..')
        Store_Single_Data('Current_Action', 'Now checking to see if seat is available.')

        Check_Bool = Check_To_See_If_Seat_Available(Table_Filtered_By_Sections_And_Words)

        if Check_Bool==True:
            print ('Seat is available, writing to shared memory...')
            Store_Single_Data('Current_Action', 'Seat is available. Notifying you through email and stopping the bot script..')
            Store_Single_Data('Seat_Availability_Boolean', 'Yes')
            Mail.Notify_Seat_Available_By_Mail(Username__)
            time.sleep(2)
            break
        elif Check_Bool==False:
            print ('Seat unavailable, refreshing and re-running loop to keep checking..')
            Store_Single_Data('Current_Action', 'Seat unavailable, refreshing and re-running loop to keep checking..')
            Store_Single_Data('Seat_Availability_Boolean', 'No')
            time.sleep(2)
            Refresh_Seat_Page(driver)


if __name__ == '__main__':
    BracBot_MainLooping_Script()