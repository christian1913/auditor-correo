import time
import pexpect

class ConnectionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConnectionManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.connections = {}
        return cls._instance

    def start_connection(self, port):
        shell = NetcatShell(port)
        shell.wait_for_connection()
        self.connections[port] = shell

    def send_command(self, port, command):
        shell = self.connections.get(port)
        if shell:
            shell.send_command(command)

    def receive_output(self, port):
        shell = self.connections.get(port)
        output = None
        if shell:
            output = shell.receive_output()
        return output

    def close_connection(self, port):
        shell = self.connections.get(port)
        if shell:
            shell.close()
        self.connections.pop(port, None)


class NetcatShell:
    def __init__(self, port):
        self.port = port
        self.process = pexpect.spawn(f'nc -lvnp {port}')
        self.process.setecho(False)
        self.process.sendline('export LC_ALL=C.UTF-8')  # Asegura que la codificación es UTF-8

    def wait_for_connection(self):
        print(f"Esperando conexión en el puerto {self.port}...")
        print("Leyendo el output inicial...")
        self.receive_output(max_timeout=1)
        print("Listo para enviar comandos.")

    def send_command(self, command):
        self.process.sendline(command)

    def receive_output(self, max_timeout=2):
        time.sleep(max_timeout)
        output = ""
        while True:
            try:
                line = self.process.read_nonblocking(1024, timeout=max_timeout).decode('utf-8', 'ignore')
                output += line
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break

        return output

    def close(self):
        self.process.terminate()