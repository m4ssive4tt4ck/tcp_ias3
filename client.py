import sys
import socket
import select


def start_connection(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.connect((HOST, PORT))

    try: 
        while True: 
            conn, addr = server.accept()
            read_sockets, write_socket, error_socket = select.select([sys.stdin, conn], [], [], 0) #select so it doesn't block

            for socks in read_sockets:
                if socks == conn:
                        message = socks.recv(2048).decode('UTF-8') 
                        if message == b'': 
                            break
                        print(message)
                else:
                    message = sys.stdin.readline().encode('UTF-8')
                    server.send(message)
                    print("I wrote: ", message)
    finally: 
        server.close()
             
            
               

if __name__ == '__main__':
    # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()
    start_connection(str(sys.argv[1]), int(sys.argv[2]))
