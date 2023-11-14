import pandas as pd

KEY_NAME = "Nom du participant"
def get_position(key):
    return key.split(" ")[3].split(".")[0]

def get_date(key):
    return key.split(" ")[3].split(".")[1]

def get_hour(key):
    begin = key.split(" ")[4]
    return begin

def get_crenaux(key):
    return f"{get_date(key)}_{get_hour(key)}"

def is_assis(key):
    if(len(key.split(" ")) < 4):
        return False
    return get_position(key) == "assise"

def is_debout(key):
    if(len(key.split(" ")) < 4):
        return False
    return get_position(key) == "debout"

def get_crenaux_assis(keys):
    crenaux = {}
    for key in keys:
        if is_assis(key):
            crenaux[get_crenaux(key)] = []
    return crenaux

def get_crenaux_debout(keys):
    crenaux = {}
    for key in keys:
        if is_debout(key):
            crenaux[get_crenaux(key)] = []
    return crenaux

def get_all_crenaux_assis_for_participant(df, participant):
    crenaux = []
    table = df.loc[df[KEY_NAME] == participant]
    idx = table.index[0]
    for key in table.keys():
        if(is_assis(key)):
            if(df.at[idx, key] > 0):
                crenaux.append(get_crenaux(key))
    return crenaux

def get_all_crenaux_debout_for_participant(df, participant):
    crenaux = []
    table = df.loc[df[KEY_NAME] == participant]
    idx = table.index[0]
    for key in table.keys():
        if(is_debout(key)):
            if(df.at[idx, key] > 0):
                crenaux.append(get_crenaux(key))
    return crenaux

def get_email(df, participant):
    crenaux = []
    table = df.loc[df[KEY_NAME] == participant]
    idx = table.index[0]
    return df.at[idx, "E-mail"]

def get_deja_attribue_date():
    df = pd.DataFrame(data=pd.read_csv("attribue.csv"))
    att = []
    for i in df.index:
        att.append(df.at[i, "date"])
    return att

def get_deja_attribue_nom():
    df = pd.DataFrame(data=pd.read_csv("attribue.csv"))
    att = []
    for i in df.index:
        att.append(df.at[i, "name"])
    return att

df = pd.DataFrame(data=pd.read_csv("reponse.csv"))

all_crenaux = get_crenaux_debout(df.keys())

nb_dispo = {}
n_participant_debout = 0
for idx in df.index:
    name = df.at[idx, KEY_NAME]
    if(name == "Les \"Oui\""):
        continue
    if(name == "Les \"Peut-être\""):
        continue
    n_assis = 0
    n_debout = 0
    for key in df.keys():
        if(is_assis(key)):
            n_assis += df.at[idx, key]
        if(is_debout(key)):
            n_debout += df.at[idx, key]
    nb_dispo[name] = [n_assis, n_debout]

only_assis = {}
can_debout = {}
for name in nb_dispo.keys():
    if(nb_dispo[name][1] > 0):
        nb = nb_dispo[name][1]
        if(nb not in can_debout.keys()):
            can_debout[nb] = []
        can_debout[nb].append(name)
        n_participant_debout += 1
        # only_assis[name] = nb_dispo[name][0]
    # else:
    #     can_debout[name] = nb_dispo[name][1]

can_debout = dict(sorted(can_debout.items()))

print(n_participant_debout)
print(can_debout)
impossible = []
possible = []
for n in can_debout.keys():
    if (n < 0):
        # print(n)
        continue
    for name in can_debout[n]:
        if (name not in get_deja_attribue_nom()):
            crenaux = get_all_crenaux_debout_for_participant(df, name)
            no_crenaux = True
            for c in crenaux:
                if (not c in get_deja_attribue_date() and len(all_crenaux[c]) <= 0):
                    all_crenaux[c].append([name, get_email(df, name)])
                    no_crenaux = False
                    break
            if(no_crenaux):
                impossible.append(name)
            else:
                possible.append(name)
for n in can_debout.keys():
    for name in can_debout[n]:
        print(f"{name} {get_email(df, name)}")
# print(impossible)
# for c in all_crenaux.keys():
#     if (len(all_crenaux[c]) > 0):
#         print(f"{c} {all_crenaux[c][0]}")
