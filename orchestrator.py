from get_data import CECADScraper
from clear_data import clear_br, clear_uf
from Filters.urls_dict import urls
from Filters.filters_dict import *

data = dict() 
scraper = CECADScraper('Utils/chromedriver', urls['CECAD'])
# for estado in estados_brasil:
#     filter = {
#         'geo': estado,
#         'var1': 'Bloco 1 - Recebe PAB'
#     }
#     data_collected = scraper.scrape_table(filter)
#     data[estado]=data_collected
#     print(estado, 'concluído')

#scraper.write_data(data, 'Data/Pessoas/UF_CECAD.txt')
br_pessoas = {}
br_familias = {}
filter = {
    'geo': 'Brasil',
    'var1': 'Bloco 1 - Recebe PAB'
}
data_collected_br_pessoas = scraper.scrape_table(filter)
data_collected_br_familias = scraper.scrape_table(filter, pessoas=False)
br_pessoas['Brasil']=data_collected_br_pessoas
br_familias['Brasil']=data_collected_br_familias

print('Brasil concluído')

scraper.write_data(br_pessoas, 'Data/Pessoas/BR_CECAD.txt')
scraper.write_data(br_familias, 'Data/Fam/BR_CECAD.txt')


clear_br('Data/Pessoas/BR_CECAD.txt')
clear_br('Data/Fam/BR_CECAD.txt')
clear_uf('Data/Pessoas/UF_CECAD.txt')
