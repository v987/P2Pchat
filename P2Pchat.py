from tkinter import *
from tkinter import scrolledtext
import socket
import threading
import time

def shownewmessages():
    if newmessage[0]:
        chat.config(state='normal')
        chat.delete("0.0","end")
        chat.update()
        chat.insert(END, messages[0])
        newmessage[0] = False
        chat.see(END)
        chat.config(state='disabled')
    chat.after(500, shownewmessages)

def SendMessage():
    tosend = inputbox.get(0.0, END)
    inputbox.delete(0.0, END)
    connection.send(tosend.encode())
    messages[0] += "[Me]: " + tosend + "\n"
    newmessage[0] = True

def ReceiveMessage():
    while True:
        msg = receivesocket.recv(1024).decode()
        messages[0] += "[" + connectto + "]: " + msg + "\n"
        newmessage[0] = True

###Globals
messages = []
messages.append("\n")
newmessage = []
newmessage.append(False)

###Intro message and instructions
print()
print("***************************** WELCOME TO P2PCHAT *****************************")
print()
print("Enter the IP Address of who you will be messaging below.")
print("Once you and the other person have done that, the interface will open on")
print("another screen. Use the lower text box to type messages.")
print()
print("The application should be restarted to message someone else.")
print("Close the application on both machines when either person is done chatting.")
print()
print()


###Create sockets and connect
sendsocket = socket.socket()
host = socket.gethostbyname(socket.gethostname())
print("Your IP Address: " + host)
print("(If this is wrong, disable unnecessary network adapters and restart the app.)")
print()
sendsocket.bind((host, 15273))
sendsocket.listen(1)

receivesocket = socket.socket()
connectto = input("Who would you like to connect to? (Enter IP Address): ")
print("Connecting...")
while True:
    try:
        receivesocket.connect((connectto, 15273))
    except:
        continue
    break
connection, address = sendsocket.accept()
print("Connected!")

###Create the window
window = Tk()
window.title("P2Pchat")

chat = scrolledtext.ScrolledText(window, state='normal')
chat.grid(row=0, column=0)
chat.after(2000, shownewmessages)
chat.config(state='disabled')
inputbox = Text(window)
inputbox.grid(row=1, column=0)
sendbutton = Button(window, text="Send", command=SendMessage)
sendbutton.grid(row=1, column = 1)

###Threads
receivethread = threading.Thread(target=ReceiveMessage)
receivethread.start()
