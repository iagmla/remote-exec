import paramiko
import logging
from logging import Logger
from threading import Thread
from ssh_remote import *

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


result = run_ssh_commands(
    commands=commands,
    hostname=hostname,
    port=port,
    username=username,
    password=password,
    key=key,
    logger=logger
)
print(result)

hosts = ["localhost", "asmodeus"]

result = run_ssh_commands_on_hosts(
    commands=commands,
    hosts=hosts,
    port=port,
    username=username,
    password=password,
    key=key,
    logger=logger
)
print(result)
