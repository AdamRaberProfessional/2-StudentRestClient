import requests
from tkinter import *
from socket import *
import json

sock = socket()
messages = []
EXIT = '[EXIT]'
request_msg = ""  # The user input or edit/create step
property_editing = ""
new_property_val = ""
student_index = ""


def message_entry_event_handler(event):
    """Initiate a request when the user presses enter"""
    if event.char == "\r":
        initiate_request()


def client_id_entry_handler(event):
    """Connect when the user presses enter """
    if event.char == "\r":
        connect()


def initiate_request():
    global request_msg, student_index
    if request_msg != "edit1":
        request_msg = message_txt.get().casefold()
    message_txt.set("")
    if request_msg[0:12] == "show student":
        student_number = request_msg[13:]  # FIX THIS to account for extra spaces
        url = 'http://localhost:8080/getstudent'
        params = {'id': student_number}

        try:
            data = requests.get(url, params)
            data = data.content.decode()
            student = json.loads(data)
        except OSError:
            update_listbox("Error connecting to the server")
        else:
            try:
                print(student)
                if student["major"] is not None:
                    update_listbox(student_number + ". " + student["firstname"] + " " + student["lastname"] +
                                   " is a college student in grade " + student["grade"] + ",")
                    update_listbox("majoring in " + student["major"] + ".""Created " + student["timecreated"] + ".")
                else:
                    update_listbox(student_number + ". " + student["firstname"] + " " + student["lastname"] +
                                   " is in grade " + student["grade"] + ". Created " + student["timecreated"])
            except KeyError:
                update_listbox("That student does not exist")

    elif request_msg == "show all students":
        message_txt.set("")
        url = 'http://localhost:8080/getstudent'
        params = {"id": "all"}
        try:
            data = requests.get(url, params)
            data = data.content.decode()
            data = json.loads(data)
            for key in data:
                student = data[key]
                if student["major"] is not None:
                    update_listbox(
                        key + ". " + student["firstname"] + " " + student["lastname"] + " is a college student in grade "
                        + student["grade"] + ",")
                    update_listbox("majoring in " + student["major"] + ". Created " + student["timecreated"] + ".")
                else:
                    update_listbox(key + ". " + student["firstname"] + " " + student["lastname"] + " is in grade "
                                   + student["grade"] + ". Created " + student["timecreated"])
        except OSError:
            if OSError:
                update_listbox("Error connecting to the server")
            else:
                update_listbox("Unknown error")

    elif request_msg[0:12] == "edit student":
        student_index = msg[13:]
        request_msg = "edit1"

    elif request_msg == "edit1":
        url = 'http://localhost:8080/editstudent'
        data = {"id": request_msg[13:], "attributeChange": "firstname", "attributeVal": "Samson"}
        try:
            data = requests.post(url, data)
        except OSError:
            if OSError:
                update_listbox("Error connecting to server")
        print(data)






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
