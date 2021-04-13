import requests
from tkinter import *
import json

"""
Command examples:
create student adam raber 16 cis
create student barrack obama 11

show all students
show student 0

edit student 1 firstname Adam
edit student 2 major CIS
edit student 3 grade 10
edit student 4 lastname Raber

delete student 5
"""

messages = []


def message_entry_event_handler(event):
    """Initiate a request when the user presses enter"""
    if event.char == "\r":
        initiate_request()


def client_id_entry_handler(event):
    """Connect when the user presses enter """
    if event.char == "\r":
        connect()


def initiate_request():
    request_msg = message_txt.get().casefold()
    message_txt.set("")

    if request_msg[0:12] == "show student":
        student_number = request_msg[13:]  # FIX THIS to account for extra spaces
        url = 'http://localhost:8080/getstudent'
        params = {'id': student_number}
        try:
            response = requests.get(url, params)
            response = response.content.decode()
            student = json.loads(response)
        except OSError:
            update_listbox("Error connecting to the server")
        else:
            try:
                if student["major"] is not None:
                    update_listbox(student_number + ". " + student["firstname"] + " " + student["lastname"] +
                                   " is a college student in grade " + student["grade"] + ",")
                    update_listbox("majoring in " + student["major"] + ". Created " + student["timecreated"] + ".")
                else:
                    update_listbox(student_number + ". " + student["firstname"] + " " + student["lastname"] +
                                   " is in grade " + student["grade"] + ". Created " + student["timecreated"])
            except KeyError:
                update_listbox("That student does not exist")

    elif request_msg == "show all students":
        url = 'http://localhost:8080/getstudent'
        params = {"id": "all"}
        try:
            response = requests.get(url, params)
            response = response.content.decode()
            response = json.loads(response)
            for key in response:
                try:
                    student = response[key]
                    if student["major"] is not None:
                        update_listbox(
                            key + ". " + student["firstname"] + " " + student["lastname"] + " is a college student in grade "
                            + student["grade"] + ",")
                        update_listbox("majoring in " + student["major"] + ". Created " + student["timecreated"] + ".")
                    else:
                        update_listbox(key + ". " + student["firstname"] + " " + student["lastname"] + " is in grade "
                                       + student["grade"] + ". Created " + student["timecreated"])
                except:
                    print(Exception)
                    pass
        except OSError:
            if OSError:
                update_listbox("Error connecting to the server")
            else:
                update_listbox("Unknown error")
    elif request_msg[0:12].casefold() == "edit student":
        msg = request_msg.split(" ")
        student_num = msg[2]
        valid_property = True
        property_editing = msg[3]
        new_property_val = msg[4]
        valid_properties = ["firstname", "lastname", "grade", "major"]
        property_editing = property_editing.casefold()
        if property_editing in valid_properties:
            if property_editing == "firstname" or property_editing == "lastname":
                new_property_val = new_property_val.capitalize()
            elif property_editing == "grade":
                try:
                    new_property_val = int(new_property_val)
                except:
                    print(Exception)
                    update_listbox("Grade must be numerical")
                    valid_property = False
            elif property_editing == "major":
                if len(new_property_val) > 4:
                    valid_property = False
                    update_listbox("Major cannot be over 4 characters")
                else:
                    new_property_val = new_property_val.upper()
        else:
            update_listbox("Sorry, this is not a recognized command. Edit cancelled.")
            valid_property = False
        if valid_property:
            url = "http://localhost:8080/editstudent"
            data = {"id": student_num, "attributeChange": property_editing, "attributeVal": new_property_val}
            try:
                response = requests.post(url, data)
                if response.status_code == 200:
                    update_listbox("Student " + student_num + "'s " + property_editing + " has been edited")
                else:
                    update_listbox("Error editing student")
            except OSError:
                update_listbox("Error connecting to server")
    elif request_msg[0:14] == "create student":
        request_msg = request_msg.casefold().split(" ")
        firstname = request_msg[2]
        lastname = request_msg[3]
        grade = request_msg[4]
        major = None
        legit_request = True
        try:
            grade = int(grade)
            if 0 > grade > 17:
                legit_request = False
                update_listbox("grade must be between 1 and 16")
        except:
            print(Exception)
            legit_request = False
            update_listbox("grade must be numerical")
        try:
            major = request_msg[5]
            if 0 >= len(major) >= 5:
                legit_request = False
                update_listbox("Major must be between 1 and 4 characters.")
        except:
            print(Exception)

        if legit_request:
            url = 'http://localhost:8080/createstudent'
            if major is None:
                data = {"fname": firstname.capitalize(), "lname": lastname.capitalize(), "grade": grade}
            else:
                data = {"fname": firstname.capitalize(), "lname": lastname.capitalize(), "grade": grade, "major": major.upper()}
            response = None
            try:
                response = requests.post(url, data)
            except OSError:
                update_listbox("Error connecting to server")
            if response.status_code == 200:
                update_listbox("The student has been created.")
            else:
                update_listbox("Error creating student")
    elif request_msg[0:14] == "delete student":
        request_msg = request_msg.split(" ")
        try:
            student_num = int(request_msg[2])
        except:
            update_listbox("Student number must be numeric")
            print(Exception)
        else:
            url = 'http://localhost:8080/deletestudent'
            data = {"id": student_num}
            try:
                response = requests.post(url, data)
                if response.status_code == 200:
                    update_listbox("Student " + request_msg[2] + " has been deleted")
                else:
                    update_listbox("Error deleting student (may not exist)")
            except OSError:
                update_listbox("Error connecting to server")



def update_listbox(msg):
    message_listbox.delete(0, len(messages))
    messages.append(msg)
    count = 0
    for message in messages:
        message_listbox.insert(count, message)
        count += 1
        message_listbox.yview_scroll(count, UNITS)


def connect():
    """Connects the client to the server and changes the GUI"""
    message_listbox.delete(0, len(messages))
    win.geometry("330x490")
    connect_button['text'] = 'Disconnect'
    connect_button['bg'] = 'light blue'
    message_listbox.grid(row=3, column=0, columnspan=2, ipady=120, sticky=N + S + E + W)


win = Tk()
win.geometry("330x51")
win.title("Client")

message_txt = StringVar()
scrname_entry_txt = StringVar()

client_id_label = Label(win, text="Client ID")
client_id_label.grid(row=1, column=0, padx=(0, 25), sticky=W)
client_id_entry = Entry(win, textvariable=scrname_entry_txt, justify=LEFT, width=35)
client_id_entry.grid(row=1, column=1, sticky=E)
client_id_entry.bind('<Key>', client_id_entry_handler)

connect_button = Button(text="Connect", width=45, command=connect)
connect_button.grid(row=2, column=0, columnspan=2)

scrollbar = Scrollbar(win)
message_listbox = Listbox(win, borderwidth=5, highlightcolor='light blue', yscrollcommand=scrollbar.set)
scrollbar.config(command=message_listbox.yview)

message_entry = Entry(win, textvariable=message_txt)
message_entry.grid(row=4, column=0, columnspan=2, ipadx=80, sticky=W)
message_entry.bind('<Key>', message_entry_event_handler)

send_btn = Button(win, text="Send", command=initiate_request)
send_btn.grid(row=4, column=1, ipadx=15, sticky=E)

win.mainloop()
