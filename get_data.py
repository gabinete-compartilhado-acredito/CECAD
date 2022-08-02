import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from Filters.urls_dict import urls
from Filters.filters_dict import *

class CECADScraper:

    def __init__(self, driver_path, url):
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(driver_path)
        self.url = url

    def acess_url(self, url):
        return self.driver.get(url)

    def write_data(self, data, output_file):
        if type(data) == dict:
            with open(output_file, 'w') as f:
                for state in data.keys():
                    f.write(f'{state}:\n')
                    f.write(f'{data[state]}\n')
        else:
            with open(output_file, 'w') as f:
                f.write(data)
                f.write('\n')

    def scrape_table(self, filter_dict, output_file=None, write=False, pessoas=True):
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

        # select "Com marcação PAB"
        self.driver.find_element_by_xpath('//*[@id="data"]/div/div[1]/div[1]/span[2]/label').click()

        # open filter menu
        self.driver.find_element_by_xpath('//*[@id="data"]/div/div[2]/div/label').click()

        # apply filters
        filters = ['//*[@id="filtros"]/div[1]/div/input[2]','//*[@id="filtros"]/div[2]/div/input[1]','//*[@id="filtros"]/div[2]/div/input[2]']
        for filter in filters:
            self.driver.find_element_by_xpath(filter).click()
            time.sleep(0.2)
        
        # generate table
        self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/button[1]').click()

        if pessoas:
            try:
                table = WebDriverWait(self.driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/table[2]')))
            except TimeoutException:
                print('Loading took too much time!')
        else:
            try:
                table = WebDriverWait(self.driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/table[1]')))
            except TimeoutException:
                print('Loading took too much time!')

        # get table
        data = table.text

        if write:
            # write table to file
            self.write_data(data, output_file)

        return data
      

if __name__=='__main__':

    data = dict()
    scraper = CECADScraper('Utils/chromedriver', urls['CECAD'])
    for estado in estados_brasil:
        filter = {
            'geo': estado,
            'var1': 'Bloco 1 - Recebe PAB'
        }
        data_collected = scraper.scrape_table(filter)
        data[estado]=data_collected
        print(estado, 'concluído')

    scraper.write_data(data, 'Data/Pessoas/UF_CECAD.txt')
    
    
    