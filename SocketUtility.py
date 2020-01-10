import paramiko
from collections import namedtuple


class SocketUtility:

    __client = None
    __ssh = None
    __Client = namedtuple("Client", "ip username passwd root_passwd")
    __HARD_DISKS_CMD = "for /f \"tokens=1-3\" %a in ('WMIC LOGICALDISK GET FreeSpace^,Name^,Size ^|FINDSTR /I /V \"Name\"') do @echo wsh.echo \"%b\" ^& \" free=\" ^& FormatNumber^(cdbl^(%a^)/1024/1024/1024, 2^)^& \" GiB\"^& \" size=\" ^& FormatNumber^(cdbl^(%c^)/1024/1024/1024, 2^)^& \" GiB\" > %temp%\\tmp.vbs & @if not \"%c\"==\"\" @echo( & @cscript //nologo %temp%\\tmp.vbs & del %temp%\\tmp.vbs"

    def __init__(self, ip, username, password):
        self.__client = self.__Client(ip, username, password, "")
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh.load_system_host_keys()
        self.__ssh.connect('localhost', username='User', password='user')

    def __ssh_cmd(self, cmd, root_passwd=None, *args, **kwargs):
        stdin, stdout, stderr = self.__ssh.exec_command(cmd, *args, **kwargs)
        return stdout.readlines()

    def get_os(self, os_name="OS Name"):
        for line in self.__ssh_cmd('systeminfo | findstr /B /C:"OS Name"', root_passwd=self.__client.root_passwd):
            if any(x in line for x in os_name):
                return line.split(":")[1].strip()

    def get_ram(self, ram_name="Total Physical Memory"):
        for line in self.__ssh_cmd('systeminfo | findstr /B /C:"Total Physical Memory"', root_passwd=self.__client.root_passwd):
            if any(x in line for x in ram_name):
                return line.split(":")[1].strip()

    def get_hard_disks(self):
        all_info = []
        for line in self.__ssh_cmd(self.__HARD_DISKS_CMD, root_passwd=self.__client.root_passwd):
            print line
            if any(x in line for x in ":"):
                all_info.append(line)
        return "<br/>".join(all_info)
