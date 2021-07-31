import re
import sys


def convert(text):
    if re.match('(Buy|Sell)\s(when)\s(crossover|crossunder)[(][.-^]*,[0-9]*[)]', text):
        # Defines action
        if re.match('^Buy', text):
            function = 'buy()'
        else:
            function = 'sell()'
        # Defines strategy
        if text.__contains__('crossover'):
            strategy = 'crossover'
        else:
            strategy = 'crossunder'

        # Finds market and amount
        bracket = re.search('(Buy|Sell)\s(when)\s(crossover|crossunder)[(](.*?)[)]', text)
        parameter = bracket.group(4).split(',')

        # Returns details
        return function + ' ' + parameter[1] + ' ' + parameter[0] + ' ' + strategy


print(convert(sys.argv[1]))
