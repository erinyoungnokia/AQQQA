import os

import paramiko
import time
from telnetlib import Telnet
from scp import SCPClient
from paramiko import SSHClient
import subprocess, sys
import re
import logging





class SSHClient_noauth(SSHClient):

    def _auth(self, username, *args):
        self._transport.auth_none(username)
        return


class SSHClient_auth(SSHClient):
    def createSSHClient(server, port, user, password):
        try:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, port, user, password)
            return client

        except:
            print("SSH not created")


class SshInterface():
    def __init__(self, server, port=22, user='rfsw', password='3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc='):
        print('Connecting through secure shell...')
        try:
            self.ip = server
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(server, port, user, password)
            time.sleep(0.15)
            print('SSH connection to {} is established.\n'.format(server))
            self.cmd = self.client.invoke_shell()
        except Exception as e:
            print("ERROR establishing SSH connection: {}".format(e))

    def SSHClose(self):
        self.client.close()
        time.sleep(0.25)
        print('Connection to SSH CLOSED.\n')

    def sshWrite(self, cmd):
        self.cmd.send(cmd + '\n')

    def sshWriteShell(self, cmd):
        self.cmd.send(cmd.encode())

    def sshRead(self):
        while not self.cmd.recv_ready():
            time.sleep(0.1)
        Out = self.cmd.recv(1024).decode()  # 9999 buffer size 4096 decode('utf-8')
        print(Out)
        return Out

    def frmonShellOpen(self, ip='127.0.0.1', port='2000'):
        self.frmon = Telnet(ip, port)
        print(self.frmon.read_very_eager())
        time.sleep(0.25)
        # print self.frmon.read_until('>\n', 5)
        print('Connection to FRMon OPENED.\n')

    def frmonShellClose(self):
        self.frmon.close()
        print('Connection to FRMon CLOSED.\n')

    def fileList(self):
        stdin, stdout, stderr = self.client.exec_command("/bin/busybox ls /")  # ,get_pty=True)
        exit_status = stdout.channel.recv_exit_status()
        flist = stdout.readlines()
        print("Number of files in the current directory is {}\n".format(len(flist)))
        for i in flist:
            print(str.replace((str(i)), '\n', ''))

            #    def Init

    def putFile(self, localFilename,
                radioFilename):  # eg: 'C:\Users\labuser\GALAXY\Init_files\ADC_config.sh','/var/tmp/ADC_config.sh'
        scp = SCPClient(self.client.get_transport())
        scp.put(r'{}'.format(localFilename), r'{}'.format(radioFilename))

    def getFile(self, radioFilename, localFilename):
        scp = SCPClient(self.client.get_transport())
        scp.get(r'{}'.format(radioFilename), r'{}'.format(localFilename))


