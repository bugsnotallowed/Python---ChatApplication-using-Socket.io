#importing required modules
import socket
import threading


HOST = '127.0.0.1'
PORT = 1234 # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = [] # list of all currently connected users

# Function to listen for upcoming msgs from a client
def listen_for_msg(client, username):
  
  while 1:

    message = client.recv(2048).decode('utf-8')
    if message !='':

      final_msg = username + '-' + message
      send_msg_to_all(final_msg)

    else:
      print("the mmsg sent from client {username} is empty!")

# Function to send mesg to a single client
def send_msg_to_client(client, message):

  client.sendall(message.encode())

#function to send any new msg to all the clients connected to this server
def send_msg_to_all(message):
  
  for user in active_clients:

    send_msg_to_client(user[1], message)

#function to handle clients
def client_handler(client):
  
  # Server will listen for client msg taht will contain the username
  while 1:

    username = client.recv(2048).decode('utf-8')
    if username != '':
      active_clients.append((username, client))
      prompt_message = "SEVER-" + f"{username} added to the chat"
      send_msg_to_all(prompt_message)
      break
    else:
      print("Client username is empty!")

  threading.Thread(target = listen_for_msg, args=(client, username, )).start()


# main function
def main():
  # Creating the socket class object
  # AF_INET type is for IPV4 addresses
  # SOCK_STREAM i.e. we are going to use TCP packages for communication
  server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Creating a try catch block
  try:
    # Providing the server with an adddress in the form of HOst IP and port
    server.bind((HOST, PORT))
    print(f"Running the server on {HOST} & port {PORT}")
  except:
    print(f"Unable to bind to host: {HOST} and the port {PORT}")

# Set sever list
  server.listen(LISTENER_LIMIT)

#this while loop will keep listening to client connections
  while 1:

    client, address = server.accept()
    print(f"Successfully connected to client {address[0]} {address[1]}")

    threading.Thread(target= client_handler, args= (client, )).start()


if __name__ == '__main__':
  main()