import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from Filters.urls_dict import urls
from Filters.filters_dict import *

class CECADScraper:

    def __init__(self, driver_path, url, headless=False):
        # Configurando exibição do navegador
        option = Options()
        option.headless = headless

        self.driver_path = driver_path
        self.driver = webdriver.Chrome(driver_path, options=option)
        self.url = url

    def acess_url(self, url):
        return self.driver.get(url)
  
    def quit(self):
        self.driver.quit()

    def get_territorio_referencia(self):
        '''
        Gets the territorial reference from the table scraped. For double checking if intended uf scrape was successful.
        '''
        xpath = '//*[@id="content"]/h2[1]'
        territorio = self.driver.find_element_by_xpath(xpath).text
        return territorio    
    
    def get_data_referencia(self):
        '''
        Gets the reference date from the webpage.
        '''
        xpath = '//*[@id="content"]/h4[1]'
        data_elemento = self.driver.find_element_by_xpath(xpath).text
        data_referencia = data_elemento.split(':')[1].strip()
        return data_referencia

    def scrape_table(self, filter_dict, output_file=None, write=False):
        '''
        Scrapes a table from a webpage.

        Parameters:
        filters (dict): A dictionary containing the filters to be applied to the table.
        output_file (str): The name of the output file.
        '''

        self.acess_url(self.url)
        geo = self.driver.find_element_by_id('estadoSAGIUFMU')
        geo.send_keys(filter_dict['geo'])
        var1 = self.driver.find_element_by_name('var1')
        var1.send_keys(filter_dict['var1'])
        var2 = self.driver.find_element_by_name('var2')
        var2.send_keys(filter_dict['var2'])

        # select "Com marcação PAB"
        self.driver.find_element_by_xpath('//*[@id="rdbSchematab_cad_16072022"]').click()

        # open filter menu
        self.driver.find_element_by_xpath('//*[@id="data"]/div/div[2]/div/label').click()

        # apply filters
        filters = ['//*[@id="filtros"]/div[1]/div/input[2]','//*[@id="filtros"]/div[2]/div/input[1]','//*[@id="filtros"]/div[2]/div/input[2]']
        for filter in filters:
            self.driver.find_element_by_xpath(filter).click()
            time.sleep(0.1)
        
        # generate table
        self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[1]').click()

        try:
            table_pessoas = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/table[2]')))
        except TimeoutException:
            print('Loading took too much time!')

        try:
            table_fam = WebDriverWait(self.driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/table[1]')))
        except TimeoutException:
            print('Loading took too much time!')

        html_fam, html_pess = table_fam.get_attribute('outerHTML'), table_pessoas.get_attribute('outerHTML')

        return html_fam, html_pess
      

if __name__=='__main__':

    scraper = CECADScraper('Utils/chromedriver', urls['CECAD'], headless=False)
    for estado in estados_brasil:
        filter = {
            'geo': estado,
            'var1': 'Bloco 1 - Recebe PAB',
            'var2': 'Bloco 1 - Faixa da renda familiar per capita'
        }
        fam, pessoas = scraper.scrape_table(filter)
        territorio_referencia = scraper.get_territorio_referencia()

        print(f'Requerido: {estado}; Concluído: {territorio_referencia}')

    #scraper.write_data(data, 'Data/Pessoas/UF_CECAD.txt')
    
    
    
