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
        try:
            self.conn, addr = sock.accept()  # Should be ready to read
            self.remote_addr = addr  # Guardar la dirección remota
            print('Accepted connection', self.conn, 'from', addr)
            self.conn.setblocking(False)
            self.selector.register(self.conn, selectors.EVENT_READ, self.read)
            self.conn.send('echo "Connection Established"\n'.encode())  # Enviar un comando inicial
        except Exception as e:
            print('Error accepting connection:', e)

    def read(self, conn):
        try:
            data = conn.recv(1000)
            if data:
                print('Received', repr(data), 'from', conn)
                self.output += data.decode()
        except Exception as e:
            print('Error reading data:', e)

    def receive_output(self):
        output = self.output
        self.output = ""  # Restablecer el output después de devolverlo
        return output

    def run(self):
        print("Starting to run the shell on port", self.port)
        while True:
            try:
                events = self.selector.select(timeout=2)
                print("Waiting for events...")
                print("Received events:", events)
                for key, mask in events:
                    print("Processing event:", key, mask)
                    callback = key.data
                    callback(key.fileobj)
                if not self.selector.get_map():
                    break
            except Exception as e:
                print('Error in event loop:', e)
        print("Shell finished running on port", self.port)

    def close(self):
        try:
            self.selector.close()
        except Exception as e:
            print('Error closing selector:', e)

    def send_command(self, command):
        try:
            print("Sending command:", command)
            # Concatenar el directorio actual al comando
            command = f"cd {self.current_directory}; {command}"
            self.conn.send(command.encode())
        except Exception as e:
            print('Error sending command:', e)

    def set_directory(self, directory):
        self.current_directory = directory


class ConnectionManager:
    def __init__(self):
        self.connections = {}

    def start_connection(self, port):
        try:
            print("Starting connection on port", port)
            port = int(port)
            shell = SocketShell(port)
            if shell.sock is not None:
                print("Shell created for port", port)
                self.connections[port] = shell

                # Iniciar un hilo para ejecutar el shell en segundo plano
                thread = threading.Thread(target=shell.run)
                thread.daemon = True  # Marcar el hilo como "daemon" para que se detenga cuando finalice el programa principal
                thread.start()

                print("Shell running on port", port)
            else:
                print("Unable to create shell for port", port)
        except Exception as e:
            print(f"Error starting connection on port {port}: {e}")

    def send_command(self, port, command):
        try:
            print("Sending command to port", port)
            shell = self.connections.get(port)
            if shell and shell.conn:
                shell.send_command(command)
                output = self.receive_output(port)  # Agregar esto
                print("Command output:", output)
            else:
                print("No active connection on port", port)
        except Exception as e:
            print(f"Error sending command to port {port}: {e}")

    def receive_output(self, port):
        try:
            print("Receiving output from port", port)
            shell = self.connections.get(port)
            if shell:
                return shell.receive_output()
        except Exception as e:
            print(f"Error receiving output from port {port}: {e}")

    def close_connection(self, port):
        try:
            shell = self.connections.get(port)
            if shell:
                shell.close()
            self.connections.pop(port, None)
        except Exception as e:
            print(f"Error closing connection on port {port}: {e}")

    def get_connection(self, port):
        if port in self.connections:
            # La conexión ya existe, la recuperamos
            return self.connections[port]
        else:
            # La conexión no existe, la iniciamos
            try:
                self.start_connection(port)
                print(f"Connection started on port {port}")
                return self.connections[port]
            except Exception as e:
                print(f"Error starting connection on port {port}: {e}")
                return None

    def set_directory(self, port, directory):
        try:
            shell = self.connections.get(port)
            if shell:
                shell.set_directory(directory)
        except Exception as e:
            print(f"Error setting directory on port {port}: {e}")
