import socket
import sys
import select
from thread import *
import threading
from threading import Thread
import logging

print_lock = threading.Lock()

list_of_clients = []
logged_in_users = [] 

 
MESSAGE = 'message'
LOGOUT = 'logout'

#DICTIONARY

commands_dict = {
    MESSAGE : 'Send a private message to someone. Type \'1 <destination clientname> <content>\' ',             
    LOGOUT : 'Disconnect this session.'
}

def logout(client,conn):
    #conn.close()
    #client.close()
    for clients in list_of_clients:
        if clients==conn:
           conn.close()
           client.close()
    
    #print"closed?"

def login(client, username):
    client.sendall('\nLogin successful. Welcome to ChatRoom!')
    logged_in_users.append((username, client)) 

def clientthread(conn,addr):
    conn.send("Welcom to this chatroom !")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                print_lock.acquire()
                print " ( "+addr[0]+" )"+message
                print_lock.release()
                message_to_send = "( "+addr[0]+ " )"+message
                broadcast(message_to_send,conn)
            else:
                print_lock.acquire()
                print "Bye! "
                print_lock.release()

        except:
            continue



def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
           clients.sendall(message)

def prompt_commands(client, client_ip_and_port):    
    while 1:
        
        client.sendall('\nEnter the number command:\n 1. Message\n 2. Logout\n ')    
        command = client.recv(2024).split()
      
        if (command[0] == "1"):
            clientthread(client, client_ip_and_port)

        elif (command[0] == "2"):
            logout(client,client_ip_and_port)
            #print"2 is pressed"
            #print "will close now"
      
        else:
            client.sendall('Command not found. ')


def prompt_login(client_sock, client_ip, client_port):
    username = 'default'
    created_username = False
    new_user = ""
    #print "yes res"
    while (not created_username):
        client_sock.sendall('Please choose a username. ')
        new_user = client_sock.recv(2024)
            
        if (len(new_user) < 3 or len(new_user) > 8):
           client_sock.sendall('Usernames must be between 3 and 8 characters long. ')    
            
        elif (new_user in logins):
           client_sock.sendall('This username already exists! Please choose another!')
        else:
           created_username = True
        
    new_pass = ""
    created_password = False
    while (not created_password):
        client_sock.sendall('Please type in a secure password. ')
        new_pass = client_sock.recv(2024)
            
        if (len(new_pass) < 4 or len(new_pass) > 8):
           client_sock.sendall('Passwords must be between 4 and 8 characters long.')  #PASSWORD ENTER
        else:
           created_password = True
        
    with open('/home/alaa/Desktop/DS_Task1/user_pass.txt', 'a') as aFile:
        aFile.write('\n' + new_user + ' ' + new_pass)                                   #STORE PASSWORD
        
    logins[new_user] = new_pass
        
    client_sock.sendall('New user created.\n')
    
    while (not username in logins):
        client_sock.sendall('\nPlease enter a valid username. ')
        username = client_sock.recv(2024) 
    
        client_sock.sendall('Please enter your password. ')
        password = client_sock.recv(2024) 
        
        if (logins[username] != password):
            client_sock.sendall('Wrong Username or Password. Please try again. ')
        
        elif (logins[username]) and (logins[username] == password):
            login(client_sock, username)
            return (True, username)
    
    return (False, username)


def prompt_create_username(client_sock):
    client_sock.sendall('Welcome to ChatRoom! Would you like to create a new user? [yes/no]')
    response = client_sock.recv(2024)
    #print"i am in peompt"
    #if (response == "yes"):
       

def handle_client(client_sock, client_ip_and_port):
    client_ip = client_ip_and_port[0]                           #CLIENT IP
    client_port = client_ip_and_port[1]                         #CLIENT PORT
    #print "hello"
    prompt_create_username(client_sock)
    #print "end" 

    while 1:
        user_login = prompt_login(client_sock, client_ip, client_port)
        logging.info("User Login Info = {}".format(user_login))
        

        if (user_login[0]):                                                         #If login succeeds
            prompt_commands(client_sock, client_ip_and_port)
            #start_new_thread(clientthread,(client_sock,client_ip_and_port))


def populate_logins_dictionaries():
    user_logins = {}

    with open('/home/alaa/Desktop/DS_Task1/user_pass.txt') as aFile:
        for line in aFile:
            (key, val) = line.split()
            user_logins[key] = val

    return user_logins

def Main():
    host=""                                          
    port=12345

    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((host,port))
    print("socket binded to post ",port)

    #In this case, up to 5 clients are placed in the connection queue
    server.listen(5)
    print("socket is listening")

    while True:
        conn,addr = server.accept()
        #print(conn)
        list_of_clients.append(conn)
        print(addr[0]+" connected")

        #start_new_thread(clientthread,(conn,addr))
        thread = Thread(target=handle_client, args=(conn, addr))
        thread.start()
    

    conn.close()
    server.close()

logins = populate_logins_dictionaries()
if __name__ == '__main__':
    Main()
