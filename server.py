import socket
import sys
import select

def start_connection(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket (af_inet for ipv4 addresses, sock_stream for tcp) 

    server.bind((HOST, PORT)) 
    server.listen(5) #listens for 5 active connections
    while True: 
        conn, addr = server.accept()
        with conn: 
            print(f"Connected by {addr}")
            while True:
                read_sockets, write_socket, error_socket = select.select([sys.stdin, conn], [], [], 0) #select so it doesn't block

                for socks in read_sockets:
                    if socks == conn:
                        try:
                            message = socks.recv(2048).decode('UTF-8') 
                            if message == b'': 
                                break
                            print(message)
                        except: 
                            conn.close(); 
                            print("connection closed") 
                            break
                    else:
                        try: 
                            message = sys.stdin.readline().encode('UTF-8')
                            server.send(message)
                            sys.stdout.write("<You>")
                            sys.stdout.write(message)
                            sys.stdout.flush()
                        except: 
                            server.close(); 
                            break
 #   server.close()

if __name__ == '__main__':
   # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3: 
        print("Correct usage: script, IP address, port number")
        exit()
    start_connection(str(sys.argv[1]), int(sys.argv[2])) #host ip and port are given via command line 
