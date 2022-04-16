from signal import signal, SIGPIPE, SIG_DFL 
#Ignore SIG_PIPE and don't throw exceptions on it... (http://docs.python.org/library/signal.html)
signal(SIGPIPE,SIG_DFL) 

import sys
import socket
import select


def start_connection(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind(('192.168.112.100', 54322)) 
    server.connect((HOST, PORT))

    while True:
        read_sockets, write_socket, error_socket = select.select([sys.stdin, server], [], [], 0) #ka Obs timeout do irgendwas macht tbh

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048).decode('UTF-8')
                print(message)
            else:
                message = sys.stdin.readline()
                server.sendall(message.encode('UTF-8'))
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
    
    server.close()
    #todo: close socket

if __name__ == '__main__':
    # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()
    start_connection(str(sys.argv[1]), int(sys.argv[2]))
