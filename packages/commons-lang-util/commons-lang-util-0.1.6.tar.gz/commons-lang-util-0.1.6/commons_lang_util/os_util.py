import os

def execute(cmd):
    os.system(cmd)


def execute_with_resp(cmd):
    return os.popen(cmd)


def kill_by_port(port):
    execute(f'sudo kill -9 $(sudo lsof -t -i:{port})')