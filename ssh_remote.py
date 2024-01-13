import paramiko
import logging
from logging import Logger
from threading import Thread

# Run multiple commands on one host

def run_ssh_commands(
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
        hostname_line = hostname + " : " + command
        print(hostname_line)
        logger.info(hostname_line)
        stdin, stdout, stderr = s.exec_command(command)
        for line in stdout.readlines():
            print(line, end="")
            log_line = line
            logger.info(log_line)
    s.close()

# Run multiple commands on multiple hosts via threads

def run_ssh_commands_on_hosts(
    commands : list,
    hosts : list,
    port : str,
    username : str,
    password : str,
    key : str,
    logger : Logger
) -> None:
    for host in hosts:
        t = Thread(
            target=run_ssh_commands,
            args=(
                commands,
                host,
                port,
                username,
                password,
                key,
                logger,
            )
        )
        t.start()
 
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


run_ssh_commands(
    commands=commands,
    hostname=hostname,
    port=port,
    username=username,
    password=password,
    key=key,
    logger=logger
)

hosts = ["localhost", "asmodeus"]

run_ssh_commands_on_hosts(
    commands=commands,
    hosts=hosts,
    port=port,
    username=username,
    password=password,
    key=key,
    logger=logger
)
