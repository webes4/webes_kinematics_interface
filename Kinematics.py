from telnetlib import Telnet
import time

class Kinematics:
    @staticmethod
    def create(kinematic_type):
        if kinematic_type == "linuxcnc":
            return LinuxCNCKinematics()
        else:
            raise ValueError("Unsupported kinematic type")

    def move_absolut(self, position):
        raise NotImplementedError("Must be implemented by subclasses")

    def move_relativ(self, delta):
        raise NotImplementedError("Must be implemented by subclasses")


class LinuxCNCKinematics(Kinematics):
    def __init__(self, host='robopi', port=5007):
        self.host = host
        self.port = port
        self.tn = None
        self._initialize_linuxcnc_connection()
        if self.tn:
            self._initialize_linuxcnc_machine()

    def _initialize_linuxcnc_connection(self):
        try:
            self.tn = Telnet(self.host, self.port)
            print(f"Telnet connection established with {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to establish Telnet connection: {e}")
            self.tn = None

    def _initialize_linuxcnc_machine(self):
        try:
            # Initialisierungsbefehle zur Vorbereitung der Maschine
            self._send_command("hello EMC user-typing-at-telnet 1.0\n")
            self._send_check_echo("set enable EMCTOO\n")
            self._send_check_echo("set wait_mode done\n")
            self._send_check_echo("set machine on\n")
            self._send_check_echo("set home -1\n")
            self._send_check_echo("set mode mdi\n")
            print("LinuxCNC machine initialized and ready")
        except Exception as e:
            print(f"Failed to initialize LinuxCNC machine: {e}")

    def move_absolut(self, position):
        if self.tn:
            command = f"set mdi g90g0x{position}\n"
            self._send_check_echo(command)
            self._wait_for_IDLE()
        else:
            print("No Telnet connection established")

    def move_relativ(self, delta):
        if self.tn:
            command = f"set mdi g91g0x{delta}\n"
            self._send_command(command)
            self._wait_for_IDLE()
        else:
            print("No Telnet connection established")

    def _send_command(self, command):
        """Sendet einen Befehl über die Telnet-Verbindung und gibt die Antwort zurück."""
        try:
            self.tn.write(command.encode('ascii'))
            response = self.tn.read_until(b"\n", timeout=2).decode('ascii').strip()
            print(f"LinuxCNC: {response}")
            return response
        except Exception as e:
            print(f"Failed to send command: {e}")
            return None
        
    def _send_check_echo(self, command):
        try:
            self.tn.write(command.encode('ascii'))
            response = self.tn.read_until(command.encode('ascii'), timeout=2).decode('ascii').strip()
            print(f"LinuxCNC: {response}")
            return response
        except Exception as e:
            print(f"Failed to send command: {e}")
            return None

    def _wait_for_IDLE(self):
        self.tn.write(b"get program_status" + b"\n")
        response = self.tn.read_until(b"IDLE").decode('ascii').strip()
        print(response)



    def close_connection(self):
        if self.tn:
            self.tn.close()
            print("Telnet connection closed")


# Beispielverwendung
"""linuxcnc_kinematics = Kinematics.create("linuxcnc")
for x in range(0,40):
    linuxcnc_kinematics.move_relativ(2.5)
    time.sleep(0.1)
    print('take pic')


linuxcnc_kinematics.close_connection()"""
