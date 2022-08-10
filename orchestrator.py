from get_data import CECADScraper
from clear_data import *
from Filters.urls_dict import urls
from Filters.filters_dict import *
from Utils.calculators import convert_date_pt

# Adquirindo dados através do CECAD
uf_fam = dict()
uf_pessoas = dict() 
scraper = CECADScraper('Utils/chromedriver', urls['CECAD'], headless=True)
for estado in estados_brasil:
    filter = {
        'geo': estado,
        'var1': 'Bloco 1 - Recebe PAB',
        'var2': 'Bloco 1 - Faixa da renda familiar per capita'
    }
    fam, pessoas = scraper.scrape_table(filter)
    territorio_referencia = scraper.get_territorio_referencia()
    uf_fam[estado]=fam
    uf_pessoas[estado]=pessoas
    print(f'Requerido: {estado}; Concluído: {territorio_referencia}')

# Adquirindo e convertendo a data de referência para formato datetime    
DATA_REFERENCIA = convert_date_pt(scraper.get_data_referencia())

filter = {
    'geo': 'Brasil',
    'var1': 'Bloco 1 - Recebe PAB',
    'var2': 'Bloco 1 - Faixa da renda familiar per capita'
}
html_br_fam, html_br_pes = scraper.scrape_table(filter)
scraper.quit()

# Persistindo dados para csv (Pode ser pulado para utilização em memória e peristência posterior em parquet)
html_to_csv(uf_fam, 'Fam', DATA_REFERENCIA)
html_to_csv(uf_pessoas, 'Pessoas', DATA_REFERENCIA)
html_to_csv(html_br_fam, 'Fam', DATA_REFERENCIA)
html_to_csv(html_br_pes, 'Pessoas', DATA_REFERENCIA)

# Transformação de dados para adequação ao consumo via DataStudio
