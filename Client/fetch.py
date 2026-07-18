import platform
import os
import socket

def fetchinfo():

    host_name = "Hostname:" + str(socket.gethostname())

    os_name = "OS: " + str(platform.system())
    release = "Release: " + str(platform.release())
    version = "Version: " + str(platform.version())

    machine = "Machine: " + str(platform.machine())
    architecture = "Architecture: " + str(platform.architecture()[0])

    processor = "CPU:" + str(platform.processor())

    cores_count = "CPU cores: " + str(os.cpu_count())

    return f"{host_name}\n{os_name}\n{release}\n{version}\n{machine}\n{architecture}\n{processor}\n{cores_count}"
