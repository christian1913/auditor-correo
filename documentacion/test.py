import pexpect
import time

class NetcatShell:
    def __init__(self, port):
        self.port = port
        self.process = pexpect.spawn(f'nc -lvp {port}')
        self.process.setecho(False)  # para que no se repitan los comandos enviados

    def wait_for_connection(self):
        print(f"Esperando conexión en el puerto {self.port}...")
        time.sleep(5)  # espera 5 segundos
        print("Continuando bajo la suposición de que la conexión ha sido establecida.")

        print("Leyendo el output inicial...")
        self.receive_output(max_timeout=10)
        print("Listo para enviar comandos.")

    def send_command(self, command):
        self.process.sendline(command)

    def receive_output(self, max_timeout=0.1):
        time.sleep(max_timeout)  # pequeña pausa para asegurarnos de que el comando tenga tiempo para ejecutarse
        output = ""
        while True:
            try:
                # Timeout de 0.1 segundos para leer la salida
                line = self.process.read_nonblocking(1024, timeout=max_timeout).decode()
                output += line
            except pexpect.TIMEOUT:
                break  # no hay más datos para leer, salir del bucle
            except pexpect.EOF:
                break  # el proceso terminó

        return output

    def close(self):
        self.process.terminate()

# Uso del script
if __name__ == "__main__":
    port = 4444

    shell = NetcatShell(port)
    shell.wait_for_connection()

    while True:
        command = input("$ ")
        if command.lower() == "exit":
            break
        else:
            shell.send_command(command)
            output = shell.receive_output()
            print(output)
    shell.close()
