import socket
import selectors
import threading


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

    def run(self):
        print("Starting to run the shell on port", self.port)
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
        print("Shell finished running on port", self.port)

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

    def get_connection(self, port):
        if port in self.connections:
            # La conexión ya existe, la recuperamos
            return self.connections[port]
        else:
            # La conexión no existe, intentamos establecerla
            try:
                # Verificar si el puerto ya está en uso
                if self.port_in_use(port):
                    print(f"Port {port} is already in use")
                    return None

                # Intentar establecer la conexión
                shell = SocketShell(port)
                if shell.sock is not None:
                    print(f"Shell created for port {port}")
                    shell.run()
                    print(f"Shell running on port {port}")
                    self.connections[port] = shell
                    return shell
                else:
                    print(f"Unable to create shell for port {port}")
                    return None

            except Exception as e:
                print(f"Error starting connection on port {port}: {e}")
                return None

    def port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            result = s.connect_ex(('localhost', port))
            return result == 0