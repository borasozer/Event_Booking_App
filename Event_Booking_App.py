import csv
from datetime import datetime
filename = "bookings.csv"

#exports the data contained in csv to the list
def load_bookings(filename):
    booking_list = []
    try:
        with open(filename, 'r', newline = "") as booking_csv:
            csv_read = csv.reader(booking_csv)
            next(csv_read)
            for rows in csv_read:
                if len(rows) == 12:
                    booking_list.append({"Date":rows[0],"Hour":rows[1],"Event Name":rows[2],"Contact Name":rows[3],"Contact No":rows[4],"Contact Email":rows[5],"Number of people":rows[6],"Catering":rows[7],"Cost":rows[8],"Deposit":rows[9],"Remaining Payment":rows[10],"Additional Info":rows[11]})
                else:
                    print("There is missing info on this event:", rows, "\nPlease delete and re-add event.")
    except FileNotFoundError:
        open("bookings.csv", "w")
        with open(filename, "w", newline="") as booking_csv:
            csv_write = csv.writer(booking_csv)
            csv_write.writerow(["Date", "Hour", "Event Name", "Contact Name", "Contact No", "Contact Email","Number of people","Catering","Cost","Deposit","Remaining Payment", "Additional Info"])
    return sorted(booking_list, key=lambda x: datetime.strptime(x["Date"], "%d-%m-%Y"))

#exports the data contained in the list to csv
def save_bookings(filename, booking_list):
    with open(filename, "w", newline="") as booking_csv:
        csv_write = csv.writer(booking_csv)
        csv_write.writerow(["Date", "Hour", "Event Name", "Contact Name", "Contact No", "Contact Email","Number of people","Catering","Cost","Deposit","Remaining Payment", "Additional Info"])
        for booking in booking_list:
            csv_write.writerow([booking["Date"], booking["Hour"], booking["Event Name"], booking["Contact Name"], booking["Contact No"], booking["Contact Email"], booking["Number of people"], booking["Catering"], booking["Cost"], booking["Deposit"], booking["Remaining Payment"], booking["Additional Info"]])

#select and check date  (added this to def because it used both new_booking and change_booking)
def check_new_date(booking_list):
    load_bookings(filename)
    while True:
        while True:
            try:
                new_date_str = input("Please enter the date in day-month-year (dd-mm-yyyy) format or press enter to return menu:")
                if new_date_str == "":
                    choice = "2"
                    return None, choice
                new_date_str = new_date_str.replace('/', '-')
                new_date_str = new_date_str.replace('.', '-')
                new_date = datetime.strptime(new_date_str, "%d-%m-%Y")
                new_date_str = new_date.strftime('%d-%m-%Y')
                if new_date < datetime.now():            #check whether it is in the past history
                    print("You cannot choose a past date.")
                    continue
                if new_date > datetime.now().replace(year=datetime.now().year + 1):   #check whether the selected date is within the next 1 year
                    print("You must choose a date within the next year.")
                    continue
                break
            except ValueError:
                print("Invalid date format.\n")
        found = False
        for booking in booking_list:
            if booking["Date"] == new_date_str:
                found = True
                print("Date is full."+"\n")
                choice = input("1.New date\n2.Menu\nChoice:")
                while choice not in ["1", "2"]:
                    choice = input("Choose one of the options:")
                if choice == "1":
                    break
                elif choice == "2":
                    return new_date_str, choice
        if found == True:
            continue
        else:
            return new_date_str, None
#add new booking to the list
def new_booking(booking_list):
    new_date_str, choice = check_new_date(booking_list)
    if choice == "2":
        return
    new_hour = input("Hour:")
    new_event_name = input("Event name:")
    new_name = input("Contact Name:")
    new_no = input("Contact number:")  #No limit was set. Because the user can enter two numbers for an event or if it is a foreign number, the country code may need to be written at the beginning. For example:+44,+1,+90
    new_email = input("Contact email:")
    new_numberofpeople = input("Number of people:")   #No limit was set. Because for example, the user can enter: 15-20
    catering_choice = input("Catering (yes/no):")
    while catering_choice not in ["yes","no"]:
        catering_choice = input("\nInvalid choice.\nCatering (yes/no):").lower()  #used .lower() to eliminate the capital difference
    if catering_choice == "yes":
        new_catering = True
    else:
        new_catering = False
    while True:
        new_cost = input("Cost:")
        if new_cost.isdigit():
            break
        else:
            print("Please enter valid value.")
    while True:
        new_deposit = input("Deposit amount:")
        if new_deposit.isdigit():
            if int(new_deposit) <= int(new_cost):
                break
            else:
                print("\nDeposit amount can't be higher than total.\n")
        else:
            print("Please enter only number.")
    new_remaining_payment = int(new_cost) - int(new_deposit)
    new_additional_info = input("Additional info:")

    new_booking = {"Date":new_date_str,"Hour":new_hour,"Event Name":new_event_name,"Contact Name":new_name,"Contact No":new_no,"Contact Email":new_email,"Number of people":new_numberofpeople,"Catering":new_catering,"Cost":new_cost,"Deposit":new_deposit,"Remaining Payment":new_remaining_payment,"Additional Info":new_additional_info}
    booking_list.append(new_booking)
    print("")
    for key, value in new_booking.items():
        print(f"{key}: {value}", end="  |  ")
    print("\n\nNew booking added.")
    save_bookings(filename, booking_list)

def check_date(booking_list):
    load_bookings(filename)
    while True:
        while True:
            try:
                date_str = input("Please enter the date in day-month-year (dd-mm-yyyy) format or press enter to return menu:")
                if date_str == "":
                    choice = "2"
                    return date_str, choice, None
                date_str = date_str.replace('/', '-')
                date_str = date_str.replace('.', '-')
                date = datetime.strptime(date_str, "%d-%m-%Y")
                date_str = date.strftime('%d-%m-%Y')
                break
            except ValueError:
                print("\nInvalid date format.\n")
        found = False
        for booking in booking_list:
            if booking["Date"] == date_str:
                found = True
                return date_str, None, found
        if found == False:
            print("\nNo event found on", date_str, "\n")
            choice = input("1.New date\n2.Menu\nChoice:")
            while choice not in ["1", "2"]:
                choice = input("Choose one of the options:")
            if choice == "1":
                continue
            elif choice == "2":
                return date_str, choice, found
def check_name(booking_list):
    while True:
        load_bookings(filename)
        searched_name = input("Please enter the name of the event or press enter to return menu:")
        if searched_name == "":
            return None, None, None
        found = False
        for booking in booking_list:
            if booking["Event Name"].lower() == searched_name.lower():  #used .lower function because avoided not being able to find due to case difference
                found = True
                found_date = booking["Date"]
                print("\n")
                for key, value in booking.items():
                        print(f"{key}: {value}", end="  |  ")
        print("")               
        if found == True:
            return searched_name, None, found
        elif found == False:
            print("\nNo event found called ", searched_name, "\n")
            print("1.Search another name")
            print("2.Return menu")
            choice = input("Choice:")
            while choice not in ["1", "2"]:
                choice = input("Choose one of the options:")
            if choice == "1":
                continue
            elif choice == "2":
                return searched_name, choice, found

def change_booking(booking_list):
    date_str, choice, found = check_date(booking_list)
    if choice == "2":
        return
    while True:
        booking_list = load_bookings(filename)    
        print("\n")
        counter = 1
        for booking in booking_list:
            if booking["Date"]== date_str:
                for key, value in booking.items():
                    if key != "Remaining Payment":
                        print(f"{counter}. {key}: {value}", end="\n")
                        counter += 1
        while True:
            change = input("Type the number you want to change or press enter to return menu:")
            if change.isdigit():
                change = int(change)
                if 1 <= change <= 11:
                    break
            elif change == "":
                return
            else:
                print("Number should between 1 and 12 or enter.")
        for booking in booking_list:
            if booking["Date"] == date_str:
                if change == 1:
                    new_date_str, choice = check_new_date(booking_list)
                    if choice == "2":
                        return
                    booking["Date"] = new_date_str
                    date_str = new_date_str
                elif change == 2:
                    new_hour = input("New hour:")
                    booking["Hour"] = new_hour
                elif change == 3:
                    new_event_name = input("New event name:")
                    booking["Event Name"] = new_event_name
                elif change == 4:
                    new_name = input("New contact name:")
                    booking["Contact Name"] = new_name
                elif change == 5:
                    new_no = input("New number:")
                    booking["Contact No"] = new_no
                elif change == 6:
                    new_email = input("New email:")
                    booking["Contact Email"] = new_email
                elif change == 7:
                    new_numberofpeople = input("New number of people:")
                    booking["Number of people"] = new_numberofpeople
                elif change == 8:
                    new_catering = input("New catering choice (yes/no):").lower()
                    while new_catering not in ["yes","no"]:
                        new_catering = input("\nInvalid choice.\nCatering (yes/no):").lower()   #used .lower() to eliminate the capital difference
                    if new_catering == "yes":
                        new_catering = True
                    else:
                        new_catering = False
                    booking["Catering"] = new_catering
                elif change == 9:
                    while True:
                        new_cost = input("Cost:")
                        if new_cost.isdigit():
                            break
                        else:
                            print("Please enter valid value.")
                    booking["Cost"] = new_cost
                    booking["Remaining Payment"] = int(booking["Cost"]) - int(booking["Deposit"])
                elif change == 10:
                    while True:
                        new_deposit = input("Deposit amount:")
                        if new_deposit.isdigit():
                            if int(new_deposit) <= int(new_cost):
                                break
                            else:
                                print("\nDeposit amount can't be higher than total.\n")
                        else:
                            print("Please enter only number.")
                    booking["Deposit"] = new_deposit
                    booking["Remaining Payment"] = int(booking["Cost"]) - int(booking["Deposit"])
                elif change == 11:
                    info_choice = input("1.Rewrite info\n2.Add info\nChoice:")
                    while not info_choice in ["1","2"]:
                        info_choice = input("\nInvalid option. Type 1 or 2:")
                    new_additional_info = input("New additional info:")
                    if info_choice == "1":
                        booking["Additional Info"] = new_additional_info
                    else:
                        booking["Additional Info"] = booking["Additional Info"] +" "+ new_additional_info
                print("Booking info succesfully changed.\n")
                print("Updated event:")
                for key, value in booking.items():
                    print(f"{key}: {value}", end="  |  ")                     
        save_bookings(filename, booking_list)

def main():
    while True:
        booking_list = load_bookings(filename)
        print("")
        print("1.Search Booking")
        print("2.Upcoming Bookings")
        print("3.Add Booking")
        print("4.Change Booking")
        print("5.Delete Booking")
        print("6.Past Bookings")
        print("7.Exit")
        option = input("Type your choice:")

        if option == "1":
            while True:
                print("")
                print("1-Search by date")
                print("2-Search by name")
                print("3-Return Menu")
                find_booking = input("Type the number of your choice: ")
                if find_booking in ["1","2","3"]:
                    break
                print("Invalid choice. Please type either 1,2 or 3.")
            if find_booking == "1":
                date_str, choice, found = check_date(booking_list)
                if choice == "":
                    continue
                for booking in booking_list:
                    if booking["Date"] == date_str:
                        print("")
                        for key, value in booking.items():
                            print(f"{key}: {value}", end="\n")   
            elif find_booking == "2":
                searched_name, choice, found = check_name(booking_list)

        elif option == "2":
            found = False
            for booking in booking_list:
                event_date = datetime.strptime(booking["Date"], "%d-%m-%Y")
                if event_date >= datetime.now():
                    print("\n")
                    for key, value in booking.items():
                        print(f"{key}: {value}", end="  |  ")
                        found = True
            print("")
            if found == False:
                print("There's no upcoming booking.")
        elif option == "3":
            new_booking(booking_list)
        elif option == "4":   
            change_booking(booking_list)
        elif option == "5":
            date_str, choice, found = check_date(booking_list)
            if choice == "2":
                continue
            for booking in booking_list:
                if booking["Date"] == date_str:
                    print("")
                    for key, value in booking.items():
                        print(f"{key}: {value}", end="\n")                     
            delete = input("\nAre you sure you want to delete this event(yes/no):").lower()
            while not delete in ["yes","no"]:
                delete = input("Type yes or no:").lower()
            if delete == "yes":
                for booking in booking_list:
                    if booking["Date"] == date_str:
                        booking_list.remove(booking)
                        save_bookings(filename, booking_list)
                        print("\n"+"Booking succesfully deleted.")
                        break
        elif option == "6":
            found = False
            for booking in booking_list:
                event_date = datetime.strptime(booking["Date"], "%d-%m-%Y")
                if event_date < datetime.now():
                    print("\n")
                    for key, value in booking.items():
                        print(f"{key}: {value}", end="  |  ")
                        found = True
            print("")
            if found == False:
                        print("There's no past booking.")
        elif option == "7":
            save_bookings(filename, booking_list)
            exit()
        else:
            print("\nInvalid Choice. Only the number must be entered.")         
        save_bookings(filename, booking_list)

main()