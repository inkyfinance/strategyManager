import re
import sys
import strategies as st
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=False, help='read from a file')
args = parser.parse_args()

default = st.Strategy("name", "exchange", "market", "entry", "exit")


def convert(text):
    if re.match('(Buy|Sell)\s(when)\s(crossover|crossunder)[(][.-^]*,[0-9]*[)]', text):
        # Finds market and amount
        bracket = re.search('(Buy|Sell)\s(when)\s(crossover|crossunder)[(](.*?)[)]', text)
        parameter = bracket.group(4).split(',')

        default.market = parameter[0]
        strategy = "indi[i:i+1]['Close'] ARROW " + parameter[1] + " and crossover==True"

        # Defines action
        if re.match('^Buy', text):
            # Defines strategy
            if text.__contains__('crossover'):
                strategy = strategy.replace("ARROW", ">")
            else:
                strategy = strategy.replace("ARROW", "<")
            default.algorithm = {
                'entry': strategy,
                'exit': default.algorithm['exit']
            }
        else:
            # Defines strategy
            if text.__contains__('crossover'):
                strategy = strategy.replace("ARROW", "<")
            else:
                strategy = strategy.replace("ARROW", ">")
            default.algorithm = {
                'entry': default.algorithm['entry'],
                'exit': strategy
            }
    else:
        print("Invalid command")


if args.file is not None:
    print("Reading from file...")
    lines = open(args.file, "r").readlines()
    for x in lines:
        convert(x)
    print(default.name, default.exchange, "['", default.algorithm['entry'], "']", "['", default.algorithm['exit'],
          "']")
else:
    while True:
        inp = input('Enter pseudocode command: ("q" to exit)\n')
        if inp == "q":
            sys.exit()
        convert(inp)
        print(default.name, default.exchange, "['", default.algorithm['entry'], "']", "['", default.algorithm['exit'],
              "']")
