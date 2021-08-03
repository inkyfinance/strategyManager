import pandas as pd
import strategies as st

d = {'name': [], 'exchange': [], 'market': [], 'entry': [], 'exit': [], 'user_hash': []}
df = pd.DataFrame(data=d)
print(df)


def addRow(strat, user_hash):
    global df
    row = {'name': strat.name, 'exchange': strat.exchange, 'market': strat.market, 'entry': strat.algorithm['entry'],
           'exit': strat.algorithm['exit'], 'user_hash': user_hash}
    df = df.append(row, ignore_index=True)


def getStratsByHash(user_hash):
    global df
    return df[df['user_hash'].str.contains(user_hash, na=False)]


addRow(st.Strategy("alex", "coinbase", "BTC", ["indi[i:i+1]['EMA20 Close'][0] > indi[i:i+1]['EMA50 Close'][0]"],
                   ["indi[i:i+1]['EMA20 Close'][0] < indi[i:i+1]['EMA50 Close'][0]"]), '00001')
addRow(st.Strategy("alex", "coinbase", "BTC", ["indi[i:i+1]['EMA20 Close'][0] > indi[i:i+1]['EMA50 Close'][0]"],
                   ["indi[i:i+1]['EMA20 Close'][0] < indi[i:i+1]['EMA50 Close'][0]"]), '00054')
print(df)
print(getStratsByHash('00001'))
