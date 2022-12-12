import paramiko
import subprocess
import pytest
import time

server_ip = '192.168.0.105'
password = 'root'
username = 'diana'

@pytest.fixture(scope='function')
def server():
    client_ssh = paramiko.SSHClient()
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client_ssh.connect(server_ip, username=username, password=password, look_for_keys=False)
    _, _, stderr = client_ssh.exec_command('iperf3 -s -1')
    
    time.sleep(0.5)
    error = None
    if (stderr.channel.exit_status_ready()):
        error = stderr.read().decode()

    client_ssh.close()
    return error


@pytest.fixture(scope='function')
def client(server):
    time.sleep(0.5)
    p = subprocess.Popen(['iperf3', '-c', server_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result, error = p.communicate()
    return result, error, server
