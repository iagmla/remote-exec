import paramiko
import logging
from logging import Logger

def run_ssh_command(
    commands : list,
    hostname : str,
    port : str,
    username : str,
    password : str,
    key : str,
    logger : Logger
) -> None:
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(
        hostname,
        port=port,
        username=username,
        key_filename=key
    )
    for command in commands:
        stdin, stdout, stderr = s.exec_command(command)
        for line in stdout.readlines():
            print(line, end="")
            logger.info(line)
    s.close()

commands = ["ls -l", "uptime"]
hostname = "localhost"
port = 22
username = "iagmla"
password = ""
key="/home/iagmla/.ssh/id_ed25519_sk"

ssh_log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
ssh_log_file = 'ssh_commands.log'
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=ssh_log_file,
    filemode='a',
    format=ssh_log_format,
    datefmt='%H:%M:%S',
    level=logging.INFO
)
logger.setLevel(logging.INFO)


run_ssh_command(
    commands=commands,
    hostname=hostname,
    port=port,
    username=username,
    password=password,
    key=key,
    logger=logger
)
