import socket
import selectors

class SocketShell:
    def __init__(self, port):
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.conn = None
        self.output = ""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', port))
        self.sock.listen()
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, self.accept)

    def accept(self, sock):
        self.conn, addr = sock.accept()  # Should be ready to read
        print('accepted', self.conn, 'from', addr)
        self.conn.setblocking(False)
        self.selector.register(self.conn, selectors.EVENT_READ, self.read)

    def read(self, conn):
        data = conn.recv(1000)
        if data:
            print('echoing', repr(data), 'to', conn)
            self.output += data.decode()

    def run(self):
        while True:
            events = self.selector.select(timeout=None)
            for key, mask in events:
                callback = key.data
                callback(key.fileobj)
            if not self.selector.get_map():
                break

    def close(self):
        self.selector.close()


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def start_connection(self, port):
        shell = SocketShell(port)
        shell.run()
        self.connections[port] = shell

    def send_command(self, port, command):
        shell = self.connections.get(port)
        if shell and shell.conn:
            shell.conn.send(command.encode())

    def receive_output(self, port):
        shell = self.connections.get(port)
        if shell:
            return shell.output

    def close_connection(self, port):
        shell = self.connections.get(port)
        if shell:
            shell.close()
        self.connections.pop(port, None)