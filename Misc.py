



def Get_Rid_Of_Quoted_Elements(input_2d_array, quoted_string):

    output_array = []

    for element in input_2d_array:
        if quoted_string not in element[3]:
            output_array.append(element)

        else:
            print ('Found a' + quoted_string +  'and hence dropping it from array')

    print ('Done getting rid of' + quoted_string + ' elements')
    return (output_array)


def Get_Elements_With_Class_Sections(input_2d_array, quoted_section):

    output_array = []

    for element in input_2d_array:
        for section in quoted_section:
            if section in element[6]:
                output_array.append(element)

            else:
                print ('Did not find ' + str(quoted_section) +  ' and hence dropping it from array')

    print ('Done collecting ' + str(quoted_section) + ' elements')
    return (output_array)


def Check_To_See_If_Seat_Available(Table_Input):
    '''
    accepts a table array and tells you if seat is available or not as a boolean
    '''
    print ('Checking to see if seat is available..')
    Seat_Available_List = []
    Seat_Available_Boolean_Output = False
    for row in Table_Input:
        try:
            Total_Seats = int(row[7])
            Seat_Remaining = int(row[8])
        except:
            print ('Hit &nbsp so setting seats to unavailable..')
            Total_Seats = 20
            Seat_Remaining = 20

        Available_Seats = Total_Seats - Seat_Remaining

        if Available_Seats==0:
            Seat_Available_List.append(False)
        elif Available_Seats>0:
            Seat_Available_List.append(True)

    print (Seat_Available_List)
    for line in Seat_Available_List:
        if line==True:
            Seat_Available_Boolean_Output = True
            break
        elif line==False:
            Seat_Available_Boolean_Output = False

    return Seat_Available_Boolean_Output

