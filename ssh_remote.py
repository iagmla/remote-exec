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
) -> bool:
    s = paramiko.SSHClient()
    s.load_system_host_keys()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(
        hostname,
        port=port,
        username=username,
        key_filename=key
    )
    error = False
    for command in commands:
        hostname_line = hostname + " : " + command
        print(hostname_line)
        logger.info(hostname_line)
        stdin, stdout, stderr = s.exec_command(command)
        for line in stdout.readlines():
            print(hostname_line + " " + line, end="")
            log_line = line
            logger.info(log_line)

        for error_line in stderr.readlines():
            error = True
            print(error_line, end="")
            error_log_line = error_line
            logger.error(error_log_line)
    s.close()
    if error:
        return False
    return True

def run_ssh_commands_threaded(
    commands : list,
    hostname : str,
    port : str,
    username : str,
    password : str,
    key : str,
    logger : Logger,
    results : list,
    thread_num: int
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
    result = True
    for command in commands:
        hostname_line = hostname + " : " + command
        print(hostname_line)
        logger.info(hostname_line)
        stdin, stdout, stderr = s.exec_command(command)
        for line in stdout.readlines():
            print(hostname_line + " " + line, end="")
            log_line = line
            logger.info(log_line)

        for error_line in stderr.readlines():
            result = False
            print(error_line, end="")
            error_log_line = error_line
            logger.error(error_log_line)
        
    s.close()
    results[thread_num] = result

# Run multiple commands on multiple hosts via threads

def run_ssh_commands_on_hosts(
    commands : list,
    hosts : list,
    port : str,
    username : str,
    password : str,
    key : str,
    logger : Logger
) -> bool:
    num_hosts = len(hosts)
    threads = [None] * num_hosts
    results = [None] * num_hosts
    for x in range(num_hosts):
        t = Thread(
            target=run_ssh_commands_threaded,
            args=(
                commands,
                hosts[x],
                port,
                username,
                password,
                key,
                logger,
                results,
                x,
            )
        )
        threads[x] = t
        threads[x].start()

    for x in range(num_hosts):
        threads[x].join()

    for result in results:
        if result == False:
            return False
    return True
