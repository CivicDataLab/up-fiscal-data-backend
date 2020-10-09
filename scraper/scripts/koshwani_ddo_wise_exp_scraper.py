#Importing packages
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
parent_folder = "../datasets/"+fiscal_year+"/ddo_wise_expenditure"

#setting up chrome driver
options = webdriver.ChromeOptions()
#chrome will download the files in the path defined in the below line
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)

url_of_section = "http://koshvani.up.nic.in/KoshReports/DDOExp.aspx"

class DdoWiseExp(SeleniumScrappingUtils):
    def get_data(self):
        
        self.section_selector(Select,driver,fiscal_year,url_of_section)

        table = driver.find_elements_by_id("myTable")[0]
       # self.table_to_csv(driver,parent_folder,"main_file", table)
        (links_of_ddos_url_string,links_of_ddos_name, name_of_hierarchy_ddos) = self.sel_elem_to_links(driver,table)
        links_of_ddos_name = links_of_ddos_name[8:]
        name_of_hierarchy_ddos = name_of_hierarchy_ddos[8:]
        for index_ddos, ddos_link in enumerate(links_of_ddos_url_string[8:]):
            driver.get(ddos_link)
            table = driver.find_elements_by_id("myTable")[0]
            hierarchy_ddos = name_of_hierarchy_ddos[index_ddos]
            (path_ddos,links_of_grants_url_string,links_of_grants_name, name_of_hierarchy_grants) = self.base_function(driver,parent_folder, links_of_ddos_name[index_ddos], fiscal_year, hierarchy_ddos, table)

            for index_grants, grants_link in enumerate(links_of_grants_url_string):
                driver.get(grants_link)
                table = driver.find_elements_by_id("myTable")[0]

                # Creating a hierarchy string
                hierarchy_grants = hierarchy_ddos + "$" + name_of_hierarchy_grants[index_grants]
                (path_grants,links_of_schemes_url_string,links_of_schemes_name,name_of_hierarchy_schemes) = self.base_function(driver,path_ddos, links_of_grants_name[index_grants], fiscal_year, hierarchy_grants, table)

                
                #adding a "-" to recognise all the repeating scheme codes uniquely
                for index, name in  enumerate(links_of_schemes_name):
                    links_of_schemes_name[index] = name + "-" + str(index)
               
                for index_schemes, schemes_link in enumerate(links_of_schemes_url_string):
                    print(links_of_schemes_name[index])
                    driver.get(schemes_link)
                    table = driver.find_elements_by_id("myTable")[0]
                    hierarchy_schemes = hierarchy_grants+ "$" + name_of_hierarchy_schemes[index_schemes]
                    (path_schemes,links_of_treasury_url_string,links_of_treasury_name, name_of_hierarchy_trea) = self.base_function(driver,path_grants, links_of_schemes_name[index_schemes], fiscal_year, hierarchy_schemes, table)

                    for index_treasury, treasury_link in enumerate(links_of_treasury_url_string):

                        print(links_of_treasury_name[index_treasury])

                        driver.get(treasury_link)

                        table = driver.find_elements_by_id("myTable")[0]

                        hierarchy_trea = hierarchy_schemes+ "$" + name_of_hierarchy_trea[index_treasury]
                        self.base_function(driver,path_schemes, links_of_treasury_name[index_treasury], fiscal_year, hierarchy_trea, table)

if __name__ == '__main__':
    obj = DdoWiseExp()
    obj.get_data()     

