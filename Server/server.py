import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

hostname = socket.gethostname()


ON = True

# Initialise the server log file and writes entry text
# with open("serverlog.log", "a") as logfile:
#     logfile.write("server has started and server log file has been sucessfully initialised.".upper)
#     logfile.write("\n")
IPAddr = socket.gethostbyname(hostname)

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

print(f"{RED}Server is running on {IPAddr} port {PORT}{RESET}")

clients = []
SERVERONLY = "-serveronly"

def server_console():

    while True:
        cmd = input()

        # Shows all available server commands
        if cmd == "/help":
            print("Please enter one of these following commands:\n" 
            "/help -> lists all possible commands and their options\n"
            "/q -> stops the server completely\n"
            "/admin <admin_password> -> sets a new administrator user acess password\n"
            "/l -> lists all currently connected users\n"
            "/kickall -> disconnects all active users from the server\n")

        # Stops the server 
        elif cmd == "/q":
            print("Server stopped")

            for client in clients:
                client.send("Server went offline".encode())
                client.close()

            server.close()
            break

        # Sets a admin password for users to get administrative rights.
        elif cmd == "/admin":
            AdminCode = input("Please enter a admin Code or type 'abort' ")

            foo = input()
            if foo != "abort":
                AdminCode = foo
                for client in clients:
                    client.send(AdminCode.encode())
                print(f"The Admin Code has sucessfully been assigned to: \033[91m{AdminCode}\033[00m")

        # Kicks users based on their source port
        elif cmd == "/kbsp":
            AdminCode = input("Please enter a source port or type 'abort' ")
            srcporttokick = None
            foo = input()
            if foo != "abort":
                srcporttokick = foo
                for client in clients:
                    if client.getpeername()[1]:
                        clients.remove(client)
                        clients.close(client)

                print(f"\033[91mAll Users with the source port {srcporttokick} have been kicked.ff\033[00m")


        # Kicks users based on their IP adress
        elif cmd == "/kbip":
            AdminCode = input("Please enter an ip adress or type 'abort' ")
            iptokick = None
            foo = input()
            if foo != "abort":
                iptokick = foo
                for client in clients:
                    if client.getipadress()[1]:
                        clients.remove(client)

                print(f"\033[91mAll Users with the ip adress {iptokick} have been kicked.ff\033[00m")

        # Shows all currently connected users on server
        elif cmd == "/l":
            ConnectedClients=0
            for client in clients:
                print(client)
                ConnectedClients=+1
            print(f"There are {ConnectedClients} Users currently on the server!")

        # Kicks all active users from the server, recommended to use before executing the command /q to shutdown the server
        elif cmd == "/kickall":
            for client in clients:
                clients.remove(client)

        elif cmd == "/fetchall":
            for client in clients:
                client.send("servercommandFetch")

        # If the typed in command does not exist or is not available
        else:
            print("Command has not been found")


threading.Thread(target=server_console, daemon=True).start()


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                # The user probably left, so can be disconnected.
                clients.remove(client)

def handle(client):
    global ON
    while ON:
        try:
            message = client.recv(1024)
            if not message:
                break
            print(message)
            if not str(message).__contains__(SERVERONLY):
                broadcast(message, client)
            else:
                print(message)
                
        except:
            break

    clients.remove(client)
    client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Shows the port that the server is running on
print(f"Server running on port {PORT}")

while True:
    # TODO: Make a server password which will be required for users to join the chat.

    client, addr = server.accept()
    print(f"{addr} connected")
    clients.append(client)
    threading.Thread(target=handle, args=(client,), daemon=True).start()