from socketserver import ThreadingTCPServer, BaseRequestHandler

_socketLookup = dict()

def _broadcast(announcement):
    for connection in _socketLookup.values():
        connection.send(announcement)

class ChatHandler(BaseRequestHandler):
    def handle(self):
        username = 'Unknown'
        active = True
        while active:
            transmission = self.request.recv(1024)
            if transmission:
                command = transmission.split()[0]
                data = transmission[1+len(command):]

                if command == 'ADD':
                    username = data.strip()
                    _socketLookup[username] = self.request
                    _broadcast('NEW %s\n' % username)
                elif command == 'MESSAGE':
                    _broadcast('MESSAGE %s\n%s\n' % (username,data))
                elif command == 'PRIVATE':
                    rcpt = data.split('\n')[0]
                    if rcpt in _socketLookup:
                        content = data.split('\n')[1]
                        _socketLookup[rcpt].send('PRIVATE %s\n%s\n'%(username,content))
                elif command == 'QUIT':
                    active = False
                    self.request.send('GOODBYE\n')
            else:
                active = False

        self.request.close()
        _socketLookup.pop(username)
        _broadcast('LEFT %s\n' % username)

print('Server is listening...')
myServer = ThreadingTCPServer(('localhost', 5555), ChatHandler)
myServer.serve_close()