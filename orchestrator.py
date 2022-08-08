from get_data import CECADScraper
from clear_data import *
from Filters.urls_dict import urls
from Filters.filters_dict import *

# Adquirindo dados através do CECAD
uf_fam = dict()
uf_pessoas = dict() 
scraper = CECADScraper('Utils/chromedriver', urls['CECAD'], headless=True)
for estado in estados_brasil:
    filter = {
        'geo': estado,
        'var1': 'Bloco 1 - Recebe PAB'
    }
    fam, pessoas = scraper.scrape_table(filter)
    uf_fam[estado]=fam
    uf_pessoas[estado]=pessoas
    print(estado, 'concluído')

filter = {
    'geo': 'Brasil',
    'var1': 'Bloco 1 - Recebe PAB'
}
html_br_fam, html_br_pes = scraper.scrape_table(filter)
scraper.quit()

# Persistindo dados para csv (Pode ser pulado para utilização em memória e peristência posterior em parquet)
html_to_csv(uf_fam, 'Fam')
html_to_csv(uf_pessoas, 'Pessoas')
html_to_csv(html_br_fam, 'Fam')
html_to_csv(html_br_pes, 'Pessoas')

# Transformação de dados para adequação ao consumo via DataStudio
