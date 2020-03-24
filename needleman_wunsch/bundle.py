import pandas as pd
import numpy as np
from ruler import Ruler
import argparse


# Pour récupérer le nom du fichier
parser = argparse.ArgumentParser()
parser.add_argument("nom_fichier", type=str, help='')
args = parser.parse_args()
nom = args.nom_fichier

# Construction de la dataframe
df = pd.read_csv(nom, sep='\t', header=None)
df.head(10)

# On remplace les lignes vides par des NaN pour implémenter dropna()
# Attention, le skip empty lines est implémenté dans le read_csv donc ces deux lignes risquent d'être redondante
df[0].replace('', np.nan, inplace=True)
df.dropna(inplace=True)

# On enlève la dernière ligne si le nombre de lignes n'est pas pair
if len(df) % 2 != 0:
    df = df.drop(len(df.index)-1)

for i in range(len(df)//2):
    ruler = Ruler(df[0][2*i], df[0][2*i+1])
    ruler.compute()
    a = ruler.distance
    top, bottom = ruler.report()
    print(f'====== example # {i+1} - distance = {a} ')
    print(top)
    print(bottom)
