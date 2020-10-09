import csv
import os
import pandas as pd
import pdb
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from utils import SeleniumScrappingUtils

#defining fiscal year and base folder to download data in
fiscal_year = "2019-2020"
parent_folder = "../datasets/"+fiscal_year+"/pfms_expenditure_detail/"
url_of_section = "http://koshvani.up.nic.in/KoshReports/PFMSCentralSchemeWise.aspx"

class PfmsExpScrapper(SeleniumScrappingUtils):
   
    def get_data(self):
        #setting up chrome driver
        options = webdriver.ChromeOptions()
        #chrome will download the files in the path defined in the below line
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)
      
        self.section_selector(Select,driver,fiscal_year,url_of_section)
        driver.refresh()

        table = driver.find_elements_by_id("myTable")[0]
        self.table_to_csv(driver,parent_folder,"main_file",table)
        (links_of_schemes_url_string,links_of_scheme_name, name_of_hierarchy_schemes) = self.sel_elem_to_links(driver,table)

        for index_schemes, schemes_link in enumerate(links_of_schemes_url_string):
            driver.get(schemes_link)
            table = driver.find_elements_by_id("myTable")[0]
            hierarchy = name_of_hierarchy_schemes[index_schemes]
            path = self.path_generator_dir_maker(driver,parent_folder,str(links_of_scheme_name[index_schemes]))
            self.table_to_csv(driver,path,links_of_scheme_name[index_schemes],table)
            self.add_columns(driver,path,links_of_scheme_name[index_schemes],fiscal_year,hierarchy)
          
if __name__ == '__main__':
    obj = PfmsExpScrapper()
    obj.get_data()
