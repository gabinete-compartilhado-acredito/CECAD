import pandas as pd


def html_to_frame(html, date, **kwargs):
    '''
    Converts an html table to a pandas dataframe.
    '''
    df = pd.read_html(html, header=1, decimal=',', thousands='.')[0]
    if 'UF' in kwargs:
        df['UF'] = kwargs['UF']
        df = df[df["Faixa da renda familiar per capita"].isin(["Extrema Pobreza", "Pobreza"])]
        df=df.pivot(index='UF', columns='Faixa da renda familiar per capita').reset_index()
        df.columns = ['_'.join(col).rstrip('_') for col in df.columns.values]
        df['ano'] = date.year
        df['mes'] = date.month
    else:
        df = df[df["Faixa da renda familiar per capita"].isin(["Extrema Pobreza", "Pobreza"])]
        df['c'] = 'BR'
        df=df.pivot(index='c', columns='Faixa da renda familiar per capita').reset_index()
        df.columns = ['_'.join(col).rstrip('_') for col in df.columns.values]
        df['ano'] = date.year
        df['mes'] = date.month
        df.drop(columns=['c'], inplace=True)

    return df

def html_to_csv(data, name, date):

    if type(data) == dict:
        # Iterate through each UF and concatenate the dataframes
        dfs = []
        for i, v in enumerate(data.values()):
            uf = list(data.keys())[i]
            df = html_to_frame(v, date, UF=uf)
            dfs.append(df)
        agg = pd.concat(dfs).reset_index(drop=True)
        agg.to_csv(f'Data/{name}/CECAD/UF_CECAD.csv')
    else:
        df = html_to_frame(data, date)
        df.to_csv(f'Data/{name}/CECAD/BR_CECAD.csv')
