import socket
import select
import sys

def Main():

    #port= 12345
    #IP_address= '127.0.0.1'
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #1>>address domain of the socket  2>>type of the socket (read the data continuous)

    
    if len(sys.argv)!=3:
        print ("Correct usage: script, IP address, port number")
        exit()
    IP_address = str(sys.argv[1])
    port = int(sys.argv[2])
   
    server.connect((IP_address, port))
    socket_list= []
    while True:
        socket_list = [sys.stdin, server]
        read_sockets, write_socket, error_socket = select.select(socket_list,[],[])
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                print message
            else:
                message = sys.stdin.readline()
	        if (message=="logout"):
		    exit()
                else:
	            server.send(message)
	            #sys.stdout.write("<You ")
	            #sys.stdout.write(message)
	            #sys.stdout.flush()
    server.close()
if __name__ == '__main__':
    Main()
