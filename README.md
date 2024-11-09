# webes_kinematics_interface

# Kinematics interface for LinuxCNC Telnet

This Python script provides an interface for controlling a CNC machine via a Telnet connection to a LinuxCNC server (linuxcncrsh). The main class, `LinuxCNCKinematics`, implements basic kinematic functions to move the CNC machine either to absolute positions or by relative increments.

## Features
- **Absolute and Relative Movement**: Send commands to move the CNC machine to absolute coordinates or perform incremental moves.
- **Telnet Connection Management**: Automatically handles Telnet connection setup, machine initialization, and closure.
- **Command Execution**: Sends commands to LinuxCNC, handles responses, and monitors command completion.

## Prerequisites
- Python 3.11
- A LinuxCNC machine with Telnet interface enabled
- (The emergency stop of the machine must be switched off by default when the machine is started up)

## references
https://linuxcnc.org/docs/html/man/man1/linuxcncrsh.1.html

## Usage

### Initialization
Create a `LinuxCNCKinematics` object using the `Kinematics.create` factory method:
```python
linuxcnc_kinematics = Kinematics.create("linuxcnc")
```
### Example of performing relative movements in a loop:
```python
for x in range(0, 10):
    linuxcnc_kinematics.move_relativ(10)
    time.sleep(0.1)
    print('take pic')
```

### Closing the Connection:
```python
linuxcnc_kinematics.close_connection()
```

# Kinematics implementation for Arduino
coming soon
