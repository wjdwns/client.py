#!/usr/bin/python3

import socket
import threading
import sys
import signal

class Server:
    def handler(signum,f):
        print(signum)
        sys.exit()

    signal.signal(signal.SIGINT,handler)
    def __init__(self):
            self.ip = "10.21.20.55"

            while 1:
                try:
                    self.port = int(input('Enter port number to run on --> '))

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.bind((self.ip, self.port))

                    break
                except:
                    print("Couldn't bind to that port")

            self.connections = []
            self.accept_connections()

    def accept_connections(self):
        self.s.listen(100)
        print('Running on IP: '+self.ip)
        print('Running on port: '+str(self.port))
        
        while True:
            try:
                c, addr = self.s.accept()

                self.connections.append(c)

                threading.Thread(target=self.handle_client,args=(c,addr,)).start()
            except KeyboardInterrupt:
                # Ctrl+C 입력시 예외 발생
                sys.exit()

        
    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except KeyboardInterrupt:
                    # Ctrl+C 입력시 예외 발생
                    sys.exit()
                except:
                    pass


    def handle_client(self,c,addr):
        while 1:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)
                signal.signal(signal.SIGINT, self.handler)
            
            except socket.error:
                c.close()
            except KeyboardInterrupt:
                # Ctrl+C 입력시 예외 발생
                sys.exit()

server = Server()
