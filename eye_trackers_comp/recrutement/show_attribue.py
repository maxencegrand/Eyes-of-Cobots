import pandas as pd
import math
df_reponse = pd.DataFrame(data=pd.read_csv("reponse.csv"))
df_attribue = pd.DataFrame(data=pd.read_csv("attribue.csv"))

for idx in df_attribue.index:
    date = df_attribue.at[idx, 'date']
    name = df_attribue.at[idx, 'name']
    # print(name)
    # # print(len(df_reponse.loc[df_reponse["Nom du participant"] == name]))
    #
    if(isinstance(name, float) and math.isnan(name)):
        continue
    else:
        idx2 = df_reponse.loc[df_reponse["Nom du participant"] == name].index[0]
        mail = df_reponse.at[idx2, "E-mail"]
        print(f"{date} - {name} ({mail})")
