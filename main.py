#!/usr/bin/env python3
import os
import random
import sys
import time
import subprocess

DEFAULT_PROMPT = "{}@{}:{}$".format(os.environ.get("USER", "my"),
                                    os.environ.get("HOSTNAME", "box"),
                                    os.environ.get("PWD", "~"))
PROMPT = os.environ.get("PROMPT", DEFAULT_PROMPT)

def main():
    try:
        file = sys.argv[1]
    except IndexError:
        print("Please add an argument for the filename")
        sys.exit(1)

    try:
        with open(file, 'r') as f:
            work(f)
    except FileNotFoundError:
        print("File '{}' not found, please enter a file that exists!".format(file))
        sys.exit(1)

def setenv(line):
    stmt = " ".join(line.split()[1:])
    key, value = stmt.split("=")
    os.environ[key] = value

def work(file):
    for line in file:
        process(line.strip())

def process(line):
    if len(line) == 0:
        return

    cmd = line.split()[0]

    print_prompt(line)
    f = shell_map.get(cmd, run)
    try:
        f(line)
    except NoneTypeError:
        raise

def run(cmd):
    subprocess.run("{}".format(cmd), shell=True)

def print_prompt(line):
    print("{}".format(PROMPT), end=' ')
    sys.stdout.flush()
    time.sleep(1)
    type_line(line)

def type_line(line):
    for char in line:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(0.03)
    print("")

shell_map = {
    "#": lambda x: None,
    "export": setenv
}

if __name__ == '__main__':
    main()
