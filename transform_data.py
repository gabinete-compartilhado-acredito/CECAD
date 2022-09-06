
import os
import pandas as pd
from datetime import datetime

def to_date(df):
    df['data'] = df['ano'].astype(str) + '-' + df['mes'].apply(lambda x: '0' + str(x) if x < 10 else str(x))
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m')

def rename_cols(df, unidade, UF):
    if UF:
        df.columns = ['semnome','UF', f'{unidade}_nao_benef_ext_pobreza',  f'{unidade}_nao_benef_pobreza', f'{unidade}_benef_ext_pobreza', f'{unidade}_benef_pobreza','sr1','sr2',f'{unidade}_inscritas_ext_pobreza', f'{unidade}_insc_pobreza', 'ano', 'mes']
        df.drop(columns=['semnome','sr1','sr2'], inplace=True)
    else:
        df.columns = ['semnome',f'{unidade}_nao_benef_ext_pobreza',  f'{unidade}_nao_benef_pobreza', f'{unidade}_benef_ext_pobreza', f'{unidade}_benef_pobreza','sr1','sr2',f'{unidade}_inscritas_ext_pobreza', f'{unidade}_insc_pobreza', 'ano', 'mes']
        df.drop(columns=['semnome','sr1','sr2'], inplace=True)
    return df
 
def load_and_concat_from_sagi(): 
    # ## Carregando e tratando dados da SAGI

    files = [f for f in os.listdir("Data/Fam/") if os.path.isfile(os.path.join("Data/Fam/", f))]
    total = len(files)
    dfs=[]
    for file in files:
        df = pd.read_csv(f"Data/Fam/{file}", header=0, index_col='Código')
        df['ano'] = df['Referência'].apply(lambda x: int(x.split('/')[1]))
        df['mes'] = df['Referência'].apply(lambda x: int(x.split('/')[0]))
        df.drop(columns=['Referência'], inplace=True)
        df.set_index(['UF','Unidade Territorial','ano','mes'], inplace=True)
        dfs.append(df)
        print('Arquivo lido. Restam', total-len(dfs), 'arquivos...')
    df = pd.concat(dfs, axis=1)


    df.rename(columns={
        'Famílias não beneficiárias no Programa Bolsa Família/Programa Auxílio Brasil em situação de extrema pobreza':'fam_nao_benef_ext_pobreza',
        'Famílias beneficiárias no Programa Bolsa Família/Programa Auxílio Brasil em situação de pobreza':'fam_benef_pobreza',
        'Famílias beneficiárias no Programa Bolsa Família/Programa Auxílio Brasil em situação de extrema pobreza':'fam_benef_ext_pobreza',
        'Famílias não beneficiárias no Programa Bolsa Família/Programa Auxílio Brasil em situação de pobreza':'fam_nao_benef_pobreza',
        'Famílias inscritas no Cadastro Único em situação de extrema pobreza':'fam_inscritas_ext_pobreza',
        'Famílias inscritas no Cadastro Único em situação de pobreza':'fam_insc_pobreza',
        },
        inplace = True)

    df['demanda_reprimida_total'] = df['fam_nao_benef_pobreza'] + df['fam_nao_benef_ext_pobreza']

    uf = df.groupby(['ano','mes','UF']).sum()

    br = df.groupby(['ano','mes']).sum()

    df.reset_index(inplace=True)
    uf.reset_index(inplace=True)
    br.reset_index(inplace=True)

    uf.columns

    to_date(br)
    to_date(uf)
    to_date(df)

    return df, uf, br

def load_from_persisted():
    df = pd.read_parquet('Results/fam_mun.parquet')
    uf = pd.read_parquet('Results/fam_uf.parquet')
    br = pd.read_parquet('Results/fam_br.parquet')

    return df, uf, br

def update_from_cecad(uf, br, df=None):
    # ## Carregando e tratando dados do CECAD

    siglas = pd.read_csv('Utils/estados_siglas.csv', usecols=['Sigla', 'Estado'])
    uf_pes_cecad = pd.read_csv('Data/Pessoas/CECAD/UF_CECAD.csv')
    uf_fam_cecad = pd.read_csv('Data/Fam/CECAD/UF_CECAD.csv')
    br_fam_cecad = pd.read_csv('Data/Fam/CECAD/BR_CECAD.csv')
    br_pes_cecad = pd.read_csv('Data/Pessoas/CECAD/BR_CECAD.csv')



    uf_pes_cecad = rename_cols(uf_pes_cecad, 'pessoas', UF=True)
    uf_fam_cecad = rename_cols(uf_fam_cecad, 'fam', UF=True)
    br_fam_cecad = rename_cols(br_fam_cecad, 'fam', UF=False)
    br_pes_cecad = rename_cols(br_pes_cecad, 'pessoas', UF=False)

    uf_cecad = pd.merge(uf_pes_cecad, uf_fam_cecad, on=['UF', 'ano', 'mes'])

    uf_cecad['UF'] = uf_cecad['UF'].apply(lambda x: x.split('-')[0].strip())

    br_cecad = pd.merge(br_pes_cecad, br_fam_cecad, on=['ano', 'mes'])


    uf_cecad['demanda_reprimida_total'] = uf_cecad['fam_nao_benef_pobreza'] + uf_cecad['fam_nao_benef_ext_pobreza']
    br_cecad['demanda_reprimida_total'] = br_cecad['fam_nao_benef_pobreza'] + br_cecad['fam_nao_benef_ext_pobreza']
    uf_cecad['demanda_reprimida_pessoas'] = uf_cecad['pessoas_nao_benef_pobreza'] + uf_cecad['pessoas_nao_benef_ext_pobreza']
    br_cecad['demanda_reprimida_pessoas'] = br_cecad['pessoas_nao_benef_pobreza'] + br_cecad['pessoas_nao_benef_ext_pobreza']
    
    # ### Adicionando novas linhas referentes à coleta do CECAD ao dataframe da SAGI

    uf = pd.concat([uf,uf_cecad]).merge(siglas, left_on='UF', right_on='Sigla', how='left')
    uf.drop(columns=['Sigla'], inplace=True)

    br = pd.concat([br,br_cecad])

    dt = datetime.date(datetime.now())
    br['ts'] = dt

    to_date(br)
    to_date(uf)

    br.to_parquet('Results/fam_br.parquet')
    uf.to_parquet('Results/fam_uf.parquet')
    if df is not None:
        df.to_parquet('Results/fam_mun.parquet')


