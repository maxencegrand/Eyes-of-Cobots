import pandas as pd
import math
df_reponse = pd.DataFrame(data=pd.read_csv("reponse.csv"))
df_attribue = pd.DataFrame(data=pd.read_csv("attribue.csv"))

all_attribue = []
for idx in df_attribue.index:
    name = df_attribue.at[idx, 'name']
    if(isinstance(name, float) and math.isnan(name)):
        continue
    else:
        all_attribue.append(name)

for idx in df_reponse.index:
    name = df_reponse.at[idx, "Nom du participant"]
    if(name not in all_attribue):
        mail = df_reponse.at[idx, "E-mail"]
        print(f"{name} ({mail})")
