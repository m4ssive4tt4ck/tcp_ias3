import socket
import sys
import select

def start_connection(HOST, PORT):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen(5) #listens for 5 active connections
    while True:
        conn, addr = server.accept()
        with conn: #braucht es das ??? 
            print(f"Connected by {addr}")
            while True:
                read_sockets, write_socket, error_socket = select.select([sys.stdin, conn], [], [])

                for socks in read_sockets:
                    if socks == conn:
                        message = socks.recv(2048).decode('UTF-8') #decode ?? 
                        if message == b'':
                            break
                        print(message)
                    else:
                        message = sys.stdin.readline()
                        server.send(message.encode())
                        sys.stdout.write("<You>")
                        sys.stdout.write(message)
                        sys.stdout.flush()
    server.close()

if __name__ == '__main__':
   # checks whether sufficient arguments have been provided
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()
    start_connection(str(sys.argv[1]), int(sys.argv[2]))
