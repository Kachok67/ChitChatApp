import socket
import threading
import random

try:
    import winsound
except ImportError:
    winsound = None
    
import platform
import datetime
import os
import fetch

SERVERONLY = "-serveronly"

SERVER_IP = input("Server IP: ")
PORT = 5555

global Color
AssignedColor = "None";
AdminCode = "None"

# COLOR SETUP
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
PURPLE = "\033[94m"
CYAN = "\033[96m"
GRAY = "\033[97m"
BLACK = "\033[90m"

# Code for resetting back to the terminals default text color
RESET = "\033[0m"

# Gives user a random color based on randomly set integer
ColorIndex = random.randint(0,5);
if ColorIndex == 0:
    Color = GREEN;
elif ColorIndex == 1:
    Color = RED;
elif ColorIndex == 2:
    Color = YELLOW;
elif ColorIndex == 3:
    Color = PURPLE;
elif ColorIndex == 4:
    Color = CYAN;
elif ColorIndex == 5:
    Color = GRAY;

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

def sendfetchinfo():

    client.send(f"{SERVERONLY}{Color}{name}{RESET} has been assigned the color {AssignedColor} ({platform.system()},{datetime.datetime.now()})".encode())
    client.send(fetch.fetchinfo()+"-serveronly")


def receive():
    global AdminCode
    while True:
        try:
            message = client.recv(1024).decode()

            # TODO: make safer and more server sided
            # Doesnt print the message if it contains the string "admincode"
            if not message.__contains__("admincode") and not message.__contains__("servercommand") or message.__contains__("/"):
                print("\n" + message)
                
                if platform.system == "Windows":
                    winsound.MessageBeep()
                elif platform.system == "Linux":
                    print("\a", end="", flush=True)

            else:
                if (message.__contains__("servercommand")):
                    if message == 'servercommandFetch':
                        sendfetchinfo()

                # Stores the message containing the code in the AdminCode variable
                AdminCode = message;
        except:
            break

# Starts a new thread to receive messages
threading.Thread(target=receive, daemon=True).start()

# Lets the user choose a username
name = "";
while name == "" or name.upper == "ADMIN":
    name = input("Your name: (You cannot pick the username ADMIN because its reserved for the chat's high priority and moderation rights user) ")

# Sets the assigned color to the correct string based on index of "ColorIndex" to show user their color
if ColorIndex == 0:
    AssignedColor = "Green"
elif ColorIndex == 1:
    AssignedColor = "Red"
elif ColorIndex == 2:
    AssignedColor = "Yellow"
elif ColorIndex == 3:
    AssignedColor = "Purple"
elif ColorIndex == 4:
    AssignedColor = "Cyan"
elif ColorIndex == 5:
    AssignedColor = "Gray"

# Shows user their Assigned Color 
print(f"You have been assigned the color: {Color}{AssignedColor}{RESET}.")

# Admin code
WantsToEnterAAdminCode = input("Do you want to enter an admin code? (y = yes | n = no) ")

if WantsToEnterAAdminCode == "y":
    UserInputAdminCode = input("Please enter an Admin Code: ")
    # If user has entered the correct administrator code then grant them the exclusive ADMIN username
    if UserInputAdminCode == AdminCode:
        name = "ADMIN";
        print("You have sucessfully joined with ADMIN rights.")
    else:
    # If user has failed to enter the correct code then report the incident to server.
        print(f"{RED}You have entered a wrong admin code. This will be reported and noted in the server logs.{RESET}")


while True:
    # takes the user input and stores it in the variable text of type string
    text = input()
    # encodes the text and sends it to server alongside some other information like the current date and time and host and username
    client.send(f"{Color}{name}{RESET} ({platform.system()},{datetime.datetime.now()}): {text}".encode())

    # detects when user wants to use non server terminal window clearing command
    if text == "//clear":
        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")