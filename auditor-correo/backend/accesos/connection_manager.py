import socket
import selectors

class SocketShell:
    def __init__(self, port):
        self.port = int(port)
        self.selector = selectors.DefaultSelector()
        self.conn = None
        self.output = ""
        self.remote_addr = None  # Para almacenar la dirección remota

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen()
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, self.accept)

    def accept(self, sock):
        self.conn, addr = sock.accept()  # Should be ready to read
        self.remote_addr = addr  # Guardar la dirección remota
        print('Accepted connection', self.conn, 'from', addr)
        self.conn.setblocking(False)
        self.selector.register(self.conn, selectors.EVENT_READ, self.read)
        self.conn.send('echo "Connection Established"\n'.encode())  # Enviar un comando inicial


    def read(self, conn):
        data = conn.recv(1000)
        if data:
            print('Received', repr(data), 'from', conn)
            self.output += data.decode()

    def run(self):
        print("Starting to run the shell on port", self.port)
        while True:
            events = self.selector.select(timeout=2)
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
        print("Starting connection on port", port)
        port = int(port)
        shell = SocketShell(port)
        print("Shell created for port", port)
        shell.run()
        print("Shell running on port", port)
        self.connections[port] = shell

    def send_command(self, port, command):
        print("Sending command to port", port)
        shell = self.connections.get(port)
        if shell and shell.conn:
            command = command + "\n"  # Asegúrate de enviar una nueva línea al final del comando
            shell.conn.send(command.encode())
            output = shell.receive_output()  # Agrega esto
            print("Output:", output) 

    def receive_output(self, port):
        print("Receiving output from port", port)
        shell = self.connections.get(port)
        if shell:
            return shell.output

    def close_connection(self, port):
        shell = self.connections.get(port)
        if shell:
            shell.close()
        self.connections.pop(port, None)