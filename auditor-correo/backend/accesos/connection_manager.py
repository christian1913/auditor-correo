import socket
import selectors

class SocketShell:
    def __init__(self, port):
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.output = ""

    def connect(self):
        try:
            self.sock.bind(('0.0.0.0', self.port))
            self.sock.listen()
            self.conn, addr = self.sock.accept()
            print('Accepted connection', self.conn, 'from', addr)
            self.conn.send('echo "Connection Established"\n'.encode())  # Enviar un comando inicial
        except OSError as e:
            print(f'Error binding to port {self.port}: {e}')
            self.conn = None

    def send_command(self, command):
        if self.conn:
            command = command + "\n"
            self.conn.send(command.encode())

    def receive_output(self):
        if self.conn:
            data = self.conn.recv(1000)
            if data:
                self.output += data.decode()
                return self.output

    def close(self):
        if self.conn:
            self.conn.close()
        self.sock.close()

class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def start_connection(self, port):
        print("Starting connection on port", port)
        port = int(port)
        shell = SocketShell(port)
        shell.connect()
        self.connections[port] = shell

    def send_command(self, port, command):
        print("Sending command to port", port)
        shell = self.connections.get(port)
        if shell:
            shell.send_command(command)

    def receive_output(self, port):
        print("Receiving output from port", port)
        shell = self.connections.get(port)
        if shell:
            return shell.receive_output()

    def close_connection(self, port):
        shell = self.connections.get(port)
        if shell:
            shell.close()
        self.connections.pop(port, None)

