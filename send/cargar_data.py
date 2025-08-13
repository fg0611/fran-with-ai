import pandas as pd

nombre_arhivo = 'prueba.csv'
df = pd.read_csv(nombre_arhivo, header=None, skiprows=1)

# print(df.head())

for i, v in df.iterrows():
    print(v[0])
    tlf = v[2].replace(' ', '').replace('-', '')
    print(f'351{tlf[-7:]}')