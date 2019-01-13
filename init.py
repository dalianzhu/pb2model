import os
import sys

sys.path.append(os.getcwd() + "/output")

import subprocess


def cmd(cmdstr):
    return subprocess.check_output(cmdstr, shell=True)


def generate_pb():
    path = os.getcwd()
    cmdstr = "cd {} && ".format(path) + \
             "python -m grpc_tools.protoc -I. --python_out=./output/ --grpc_python_out=./output/ test.proto"
    print(cmdstr)
    cmd(cmdstr)

generate_pb()