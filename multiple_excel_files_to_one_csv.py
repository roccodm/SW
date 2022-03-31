'''
**********************************************************
 Lettore di file excel multipli con output su singolo csv
**********************************************************
Capita di ricevere dati su fogli excel sparsi che poi devono
essere riarrangiati su un singolo csv per ulteriori elaborazioni

Questo semplice script prende tutti i file in una cartella
e li processa attraverso delle operazioni su matrice che vanno
adattati in base alle esigenze


'''

path='../../Documenti/federico/PERTRE/ST42-COPIE/*.xlsm'

import pandas as pd
import numpy as np
import glob

def list_print(l):
    for element in l:
        print (str(element)+";",end="")
    print()

first=True
for filename in glob.glob(path):
    # leggo il file excel
    df = pd.read_excel (filename)
    # converto in matrice
    m = np.asmatrix(df)
    # estraggo le parti che mi interessano e preparo una singola riga
    rownames=[]
    rownames.append("Stazione")
    rownames+=(np.squeeze(np.asarray(m[2:21,3])).tolist())
    rownames+=(np.squeeze(np.asarray(m[13:20,8])).tolist())
    rownames+=(np.squeeze(np.asarray(m[2:6,11])).tolist())
    rownames.append("Classificazione")

    values=[]
    values.append(m[0,2])
    values+=(np.squeeze(np.asarray(m[2:21,5])).tolist())
    values+=(np.squeeze(np.asarray(m[13:20,11])).tolist())
    values+=(np.squeeze(np.asarray(m[2:6,12])).tolist())
    values.append(m[8,11])

    if first:
        list_print(rownames)
        first=False
    list_print(values)
