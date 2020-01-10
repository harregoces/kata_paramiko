from ..interfaces.OsCommands import OsCommands
import paramiko


class Debian(OsCommands):

    __os_check_list = ["DISTRIB_DESCRIPTION"]
    __ssh = None
    __hard_disks = [
        'sda', 'sdb', 'sdc', 'sdd', 'sde', 'sdf', 'sdg',
        'sdh', 'sdi', 'sdj', 'sdk', 'sdl', 'sdm', 'sdn',
        'sdo', 'sdp', 'sdq', 'sdr', 'sds'
    ]

    def __init__(self, ip, port, username, password):
        self.__ssh = paramiko.SSHClient()
        self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh.load_system_host_keys()
        try:
            self.__ssh.connect(ip, int(port), username=username, password=password)
        except:
            return 'an exception has occurred'

    def __ssh_cmd(self, cmd, *args, **kwargs):
        stdin, stdout, stderr = self.__ssh.exec_command(cmd, *args, **kwargs)
        return stdout.readlines()

    def get_os(self):
        for line in self.__ssh_cmd("cat /etc/*release", root_passwd=self.__client.root_passwd):
            if any(x in line for x in self.__os_check_list):
                # check for the obvious stuff first
                return line.split("=")[1]
        for os in self.__ssh_cmd("cat /etc/system-release"):
            return os

    def get_ram(cls):
        pass

    def get_hard_disk(self):
        for line in self.__ssh_cmd("sudo -k udisksctl status", get_pty=True, root_passwd=self.__client.root_passwd):
            if any(hd in line for hd in self.__hard_disks):
                return line
            elif "command not found" in line:
                print("udisksctl not installed on target server")
