#!/usr/bin/env python3.4

import itertools
import re
import sys
import traceback

class Exit:
    OK = 0
    WA = 1
    PE = 2
    ERROR = 10


def parse_turing(machine_desc, state_limit=50):
    machine = {
        "start": {},
        "finish": {}
    }
    
    for i, line in zip(itertools.count(start=1), machine_desc.split("\n")):
        if line.strip() == "":
            continue
        match = re.fullmatch("^(?P<state>\w+)\s+(?P<symbol>\w)\s+->\s+(?P<new_state>\w+)\s+(?P<new_symbol>\w)\s+(?P<direction>[<>!])$", line.strip())
        
        if match is None:
            print("Syntax error: line", i, "is invalid", file=sys.stderr)
            sys.exit(Exit.PE)
        
        state = match.group("state")
        symbol = match.group("symbol")
        new_state = match.group("new_state")
        new_symbol = match.group("new_symbol")
        direction = match.group("direction")
        
        machine[state] = machine.get(state, {})
        
        if machine[state].get(symbol, None) is not None:
            print("Machine has several ways from {{state = {}, symbol = {}}}".format(state, symbol), file=sys.stderr)
            sys.exit(Exit.PE)
        
        machine[state][symbol] = (new_state, new_symbol, direction)
        machine[new_state] = machine.get(new_state, {})
        
        if len(machine) >= state_limit:
            print("Too many states", file=sys.stderr)
            sys.exit(Exit.PE)
    
    return machine


def interpret_turing(machine, input, step_limit=262144):
    tape = {}
    for i, c in zip(itertools.count(), input):
        tape[i] = c
    pos = 0
    state = "start"
    steps = 0
    
    while state != "finish":
        move = machine.get(state, {}).get(tape[pos], None)
        
        if move is None:
            print("Machine has no ways from {{state = {}, symbol = {}}}".format(state, tape[pos]), file=sys.stderr)
            sys.exit(Exit.PE)
        
        new_state, new_symbol, direction = move
        
        tape[pos] = new_symbol
        state = new_state
        
        if direction == "<":
            pos -= 1
        elif direction == ">":
            pos += 1
        
        tape[pos] = tape.get(pos, "_")
        
        steps += 1
        
        if steps > step_limit:
            print("Too many steps", file=sys.stderr)
            sys.exit(Exit.PE)
    
    output = ''.join(map(lambda pair: pair[1], sorted(tape.items()))).replace('_', ' ').strip()
    
    return (output, steps)


def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    answer_file = sys.argv[3]
    
    with open(input_file, "r") as f:
        input = f.read().strip()
    
    with open(output_file, "r") as f:
        machine = parse_turing(f.read())
    
    with open(answer_file, "r") as f:
        answer = f.readline().strip()
    
    output, steps = interpret_turing(machine, input)
    
    if output == answer:
        print("Got correct answer in", steps, "steps", file=sys.stderr)
        sys.exit(Exit.OK)
    else:
        print("Answers differ", file=sys.stderr)
        sys.exit(Exit.WA)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except:
        traceback.print_exc()
    sys.exit(Exit.ERROR)