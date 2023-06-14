import socket
import selectors

class SocketShell:
    def __init__(self, port):
        self.port = int(port)
        self.selector = selectors.DefaultSelector()
        self.conn = None
        self.output = ""
        self.remote_addr = None
        self.current_directory = ""  # Variable para mantener el directorio actual

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind(('0.0.0.0', self.port))
        except OSError as e:
            print(f'Error binding to port {self.port}: {e}')
            return
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

    def receive_output(self):
        output = self.output
        self.output = ""  # Restablecer el output después de devolverlo
        return output

    def start_listening(self):
        print("Starting to listen on port", self.port)
        while True:
            events = self.selector.select(timeout=2)
            print("Waiting for events...")
            print("Received events:", events)
            for key, mask in events:
                print("Processing event:", key, mask)
                callback = key.data
                callback(key.fileobj)
            if not self.selector.get_map():
                break
        print("Listening finished on port", self.port)

    def close(self):
        self.selector.close()

    def send_command(self, command):
        print("Sending command:", command)
        # Concatenar el directorio actual al comando
        command = f"cd {self.current_directory}; {command}"
        self.conn.send(command.encode())

    def set_directory(self, directory):
        self.current_directory = directory


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def send_command(self, port, command):
        print("Sending command to port", port)
        shell = self.connections.get(port)
        if shell and shell.conn:
            shell.send_command(command)
            output = self.receive_output(port)  # Agregar esto
            print("Command output:", output)

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

    def get_connection(self, port):
        if port in self.connections:
            # La conexión ya existe, la recuperamos
            return self.connections[port]
        else:
            # La conexión no existe, la iniciamos
            try:
                shell = SocketShell(port)
                self.connections[port] = shell
                print(f"Connection started on port {port}")
                return shell
            except Exception as e:
                print(f"Error starting connection on port {port}: {e}")
                return None
