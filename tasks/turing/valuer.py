#!/usr/bin/python3.4

import itertools
import json
import sys
import traceback


MESSAGE_OK = "Problem solved. Congratulations! Flag is ugra_turing_code_magic"


class Test:
    '''Object to store test info.'''
    
    def __init__(self, config):
        self.id      = config.get("sequenceNumber", None)
        self.verdict = config.get("verdict", "undefined").upper()
        if "-" in self.verdict:
            self.verdict = "".join(list(map(lambda word: word[0], self.verdict.split("-"))))
        self.time    = int(config.get("runningTime", 0))
        self.memory  = int(config.get("memoryUsed", 0))
        
        pointNode  = config.get("score", {})
        for key in pointNode:
            if key != "scoreType":
                self.points = pointNode[key]

    def passed(self):
        return self.verdict == "OK"
    
    def format_time(self):
        if t >= 1000:
            return "{0:>.2f} s".format(t / 1000.0)
        return "{0} ms".format(t)
  
    def format_memory(self):
        if m > 2**23:
            return "{0} MB".format(m // 2**20)
        if m >= 2**20:
            return "{0:.1f} MB".format(m / 2**20)
        if m > 2**13:
            return "{0} KB".format(m // 2**10)
        if m >= 2**10:
            return "{0:.1f} KB".format(m / 2**10)
        return "{0} bytes".format(m)



def process_log():
    '''Processes Yandex.Contest run log.'''
    
    data = {}
    report = json.loads(input())
    for test_object in report["tests"]:
        test = Test(test_object)
        data[test.id] = test
    return data


def process_results(tests):
    '''Processes results'''
    
    for test_id, test in tests.items():
        if not test.passed():
            print("Tests were not passed.", file=sys.stderr)
            return 0
    
    print(MESSAGE_OK, file=sys.stderr)
    return 100

    
def main():
    try:
        tests = process_log()
        final_score = process_results(tests)
    except Exception as e:
        print(-239)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    print(final_score)

   
if __name__ == "__main__":
    main()