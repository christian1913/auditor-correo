import time
import pexpect

class ConnectionManager:
    def __init__(self):
        self.connections = {}

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
        self.process = pexpect.spawn(f'nc -lvp {port}')
        self.process.setecho(False)

    def wait_for_connection(self):
        print(f"Esperando conexión en el puerto {self.port}...")
        time.sleep(5)
        print("Continuando bajo la suposición de que la conexión ha sido establecida.")

        print("Leyendo el output inicial...")
        self.receive_output(max_timeout=10)
        print("Listo para enviar comandos.")

    def send_command(self, command):
        self.process.sendline(command)

    def receive_output(self, max_timeout=0.1):
        time.sleep(max_timeout)
        output = ""
        while True:
            try:
                line = self.process.read_nonblocking(1024, timeout=max_timeout).decode()
                output += line
            except pexpect.TIMEOUT:
                break
            except pexpect.EOF:
                break

        return output

    def close(self):
        self.process.terminate()
