import pandas as pd


df_train = pd.read_csv('data/cv-corpus-19.0-2024-09-13/pl/train.tsv', sep='\t')
df_test = pd.read_csv('data/cv-corpus-19.0-2024-09-13/pl/test.tsv', sep='\t')
print(df_train.head())
df_train = df_train.drop([column for column in df_train.columns if column not in ['path', 'sentence']], axis=1)
df_test = df_test.drop([column for column in df_test.columns if column not in ['path', 'sentence']], axis=1)
df = pd.concat([df_train, df_test])
df.to_csv('data/pl_dataset.csv')
