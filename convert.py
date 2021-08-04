import re
import sys
import strategies as st
import strategyManager as stMan
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", type=str, required=False, help='read from a file')
args = parser.parse_args()

default = st.Strategy("name", "exchange", "market", "entry", "exit")


def convert(text):
    if re.match('(Buy|Sell)\s(when)\s(crossover|crossunder)[(].*[.-^].*,.*[.-^].*[)]', text):
        # Finds market and amount
        bracket = re.search('(Buy|Sell)\s(when)\s(crossover|crossunder)[(](.*?)[)]', text)
        parameter = bracket.group(4).split(',')
        type = bracket.group(3)

        identity1 = parameter[0]
        identity2 = parameter[1]
        if not re.match('^[0-9]*$',identity1):
            identity1 = "indi[i:i+1]['" + identity1 + " Close'][0]"
        if not re.match('^[0-9]*$',identity2):
            identity2 = "indi[i:i+1]['" + identity2 + " Close'][0]"
        strategy = identity1 + " ARROW " + identity2 + " and " + type + "==True"

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
    elif re.match('(Load|Save|Clear)\s(database)', text):
        if re.match('^Load', text):
            stMan.loadDataframe()
        elif re.match('^Save', text):
            stMan.saveDataframe()
        elif re.match('^Clear', text):
            stMan.clearDataframe()
    else:
        print("Invalid command")


if args.file is not None:
    print("Reading from file...")
    lines = open(args.file, "r").readlines()
    for x in lines:
        convert(x)
    print(default.name, default.exchange, default.market,  "['", default.algorithm['entry'], "']", "['", default.algorithm['exit'],
          "']")
else:
    while True:
        inp = input('Enter pseudocode command: ("q" to exit)\n')
        if inp == "q":
            sys.exit()
        convert(inp)
        print(default.name, default.exchange, default.market, "['", default.algorithm['entry'], "']", "['", default.algorithm['exit'],
              "']")
