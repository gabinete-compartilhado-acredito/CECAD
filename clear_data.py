import pandas as pd


def html_to_frame(html):
    '''
    Converts an html table to a pandas dataframe.
    '''
    df = pd.read_html(html, header=1)[0]
    df.dropna(inplace=True)
    df.rename(columns={'Unnamed: 0':'Territorio'}, inplace=True)
    df = df[df['Territorio']!='TOTAL']

    return df

def html_to_csv(data, name):

    if type(data) == dict:
        # Iterate through each UF and concatenate the dataframes
        dfs = []
        for v in data.values():
            df = html_to_frame(v)
            dfs.append(df)
        agg = pd.concat(dfs).reset_index(drop=True)
        agg.to_csv(f'Data/{name}/UF_CECAD.csv')
    else:
        df = html_to_frame(data)
        df.to_csv(f'Data/{name}/BR_CECAD.csv')
