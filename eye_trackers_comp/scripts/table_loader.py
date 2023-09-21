import pandas as pd

def _LOAD(csvfile):
    return pd.DataFrame(data=pd.read_csv(csvfile))

def _GET(table, id, key, keyId="id"):
    return _GET_ALL_VALUES(table, id, key, keyId=keyId)[0]

def _GET_ALL_VALUES(table, id, key, keyId="id"):
    request = table.loc[table[keyId] == id]
    values = []
    for idx in range(len(request.index)):
        values.append(table.at[request.index[idx], key])
    # print(values)
    return values

def _EXISTS(table, id, key, keyId="id"):
    request = table.loc[table[keyId] == id]
    return len(request.index) > 0

def _GET_ALL(table, id, keyId="id"):
    request = table.loc[table[keyId] == id]
    return request

def _TOLIST(table,key):
    return table[key].tolist()

def _ADD(table, tuple):
    table[len(table)] = list
