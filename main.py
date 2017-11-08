#!/usr/bin/python3

import os, sys
import re
import itertools

from parser import lex, parse

# This function is sort of gross right now, but will allow for readline-like
# features in the future
def read_input():
    out = ""
    cont_line = False
    reading = True
    while reading:
        char = sys.stdin.read(1)
        if len(char) == 0: # EOF
            if len(out) == 0:
                exit(0)
        if char == "\\":
            cont_line = True
            print(">", end="")
            sys.stdout.flush()
        elif char == "\n":
            if not cont_line:
                reading = False
        else:
            out += char
            cont_line = False
    return out

def maybe_handle_builtin(cmd):
    if cmd[0] == "cd":
        os.chdir(cmd[1])
        return True
    elif cmd[0] == "exec":
        os.execvp(cmd[1], cmd[1:])
        return True
    elif cmd[0] == "exit":
        exit(int(cmd[1]))
    else:
        return False

def run_command(cmd):
    if not maybe_handle_builtin(cmd):
        pid = os.fork()
        if pid == 0:
            os.execvp(cmd[0], cmd)
        else:
            return os.waitpid(pid, 0)[1]

def process_input(inpt_tree):
    run_next = True
    negate_next = False
    status = 0
    for word in inpt_tree:
        if type(word) == list:
            print(word)
            pid = os.fork()
            if pid == 0:
                process_input(word)
                exit()
            else:
                status = os.waitpid(pid, 0)[1]
        else:
            if word == "&&":
                run_next = (status == 0)
            elif word == "||":
                run_next = (status != 0)
            elif word == ";":
                run_next = True
            elif word == "!":
                negate_next = True
            elif run_next:
                status = run_command(word.split(" "))
                if negate_next:
                    status = 1 if status == 0 else 0
                negate_next = False

def main():
    while True:
        print("$ ", end="")
        sys.stdout.flush()
        process_input(parse(lex(read_input())))

if __name__ == "__main__":
    main()
