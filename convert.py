import re
import sys


class Strategy:
    def __init__(self, name, exchange, entry, exit):
        self.name = name
        self.exchange = exchange
        self.algorithm = {
            'entry': entry,
            'exit': exit
        }


default = Strategy("name", "exchange", "entry", "exit")


def convert(text):
    if re.match('(Buy|Sell)\s(when)\s(crossover|crossunder)[(][.-^]*,[0-9]*[)]', text):
        # Finds market and amount
        bracket = re.search('(Buy|Sell)\s(when)\s(crossover|crossunder)[(](.*?)[)]', text)
        parameter = bracket.group(4).split(',')
        default.exchange = parameter[0]

        # Defines strategy
        if text.__contains__('crossover'):
            strategy = "indi[i:i+1]['Close'] ARROW AMOUNT and crossover==True"
            strategy = strategy.replace("AMOUNT", parameter[1])

            # Defines action
            if re.match('^Buy', text):
                strategy = strategy.replace("ARROW", ">")
                default.algorithm = {
                    'entry': strategy,
                    'exit': default.algorithm['exit']
                }
            else:
                strategy = strategy.replace("ARROW", "<")
                default.algorithm = {
                    'entry': default.algorithm['entry'],
                    'exit': strategy
                }
        else:
            strategy = 'crossunder'


while True:
    inp = input()
    if inp == "exit":
        sys.exit()
    convert(inp)
    print(default.name, default.exchange, "['", default.algorithm['entry'], "']", "['", default.algorithm['exit'], "']")
