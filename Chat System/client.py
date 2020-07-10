from socket import socket
from threading import Thread

class IncomingThread(Thread):
    def run(self):
        stillChatting = True
        while stillChatting:
            transmission = server.recv(1024)
            lines = transmission.split('\n')[:-1]
            i = 0
            while i < len(lines):
                command = lines[i].split()[0]
                param = lines[i][len(command)+1: ]
                if command == 'GOODBYE':
                    stillChatting = False
                elif command == 'NEW':
                    print('==>', param, 'has joined the chat room')
                elif command == 'LEFT':
                    print('==>', param, 'has left the chat room')
                elif command == 'MESSAGE':
                    i += 1
                    print('==>', param + ': ' + lines[i])
                elif command == 'PRIVATE':
                    i += 1
                    print('==>', param + ' [private]: ' + lines[i])
                i += 1
server = socket()
server.connect(('localhost', 5555))
username = input('What is your name: ').strip()
server.send(bytes(username, 'utf-8'))
incoming = IncomingThread()
incoming.start()

active = True
while active:
    message = input()
    if message.strip():
        if message.rstrip().lower() == 'quit':
            server.send('QUIT\n')
            active = False
        elif message.split()[0].lower() == 'private':
            colon = message.index(':')
            friend = message[7:colon].strip()
            server.send('PRIVATE %s\n%s\n' % (friend,message[1+colon: ]))
        else:
            server.send('MESSAGE ' + message)