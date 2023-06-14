class SocketShell:
    def __init__(self, port):
        self.port = int(port)
        self.selector = selectors.DefaultSelector()
        self.conn = None
        self.output = ""
        self.remote_addr = None

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
        self.output = ""  # Restablece el output después de devolverlo
        return output

    def run(self):
        print("Starting to run the shell on port", self.port)
        while True:
            print("Waiting for events...")
            events = self.selector.select(timeout=2)
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

class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def start_connection(self, port):
        print("Starting connection on port", port)
        port = int(port)
        shell = SocketShell(port)
        if shell.sock is not None:
            print("Shell created for port", port)
            shell.run()
            print("Shell running on port", port)
            self.connections[port] = shell
        else:
            print("Unable to create shell for port", port)

    def send_command(self, port, command):
        print("Sending command to port", port)
        shell = self.connections.get(port)
        if shell and shell.conn:
            command = command + "\n"  # Asegúrate de enviar una nueva línea al final del comando
            shell.conn.send(command.encode())
            output = self.receive_output(port)  # Agrega esto
            print("Output:", output) 

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
