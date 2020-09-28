#Importing packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pdb
import time 
import os
import csv
import glob
from selenium.webdriver.support.ui import Select
from utils import sel_elem_to_links, base_function




#defining fiscal year and base folder to download data in
fiscal_year = '2019-2020'
parent_folder = "datasets/"

#setting up chrome driver
options = webdriver.ChromeOptions()
#chrome will download the files in the path defined in the below line
prefs = {'download.default_directory' : "/home/ubuntu/cdl/koshvani/up-state-budget-scrapper/datasets"}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = options)

# first target link
driver.get('http://koshvani.up.nic.in/')

close_button = driver.find_element_by_class_name("open_button").click()
# maximising because the fiscal year is not interactive in smaller window (need to discuss)
driver.maximize_window() 

select = Select(driver.find_element_by_id('ddlFinYear'))
select.select_by_visible_text(fiscal_year)
close_button = driver.find_element_by_class_name("open_button").click()

# Link to ddo-wise expenditure section
driver.get("http://koshvani.up.nic.in/KoshReports/DDOExp.aspx")


table = driver.find_elements_by_id("myTable")[0]
(links_of_ddos_url_string,links_of_ddos_name, name_of_hierarchy_ddos) = sel_elem_to_links(driver,table)
links_of_ddos_name = links_of_ddos_name[11:]
for index_ddos, ddos_link in enumerate(links_of_ddos_url_string[11:]):
    driver.get(ddos_link)
    table = driver.find_elements_by_id("myTable")[0]
    hierarchy_ddos = name_of_hierarchy_ddos[index_ddos]
    (path_ddos,links_of_grants_url_string,links_of_grants_name, name_of_hierarchy_grants) = base_function(driver,parent_folder, links_of_ddos_name[index_ddos], fiscal_year, hierarchy_ddos, table)

    for index_grants, grants_link in enumerate(links_of_grants_url_string):
        driver.get(grants_link)
        table = driver.find_elements_by_id("myTable")[0]

        # Creating a hierarchy string
        hierarchy_grants = hierarchy_ddos + "$" + name_of_hierarchy_grants[index_grants]
        (path_grants,links_of_schemes_url_string,links_of_schemes_name,name_of_hierarchy_schemes) = base_function(driver,path_ddos, links_of_grants_name[index_grants], fiscal_year, hierarchy_grants, table)

        
        #adding a "-" to recognise all the repeating scheme codes uniquely
        for index, name in  enumerate(links_of_schemes_name):
            links_of_schemes_name[index] = name + "-" + str(index)
       
        for index_schemes, schemes_link in enumerate(links_of_schemes_url_string):
            print(links_of_schemes_name[index])
            driver.get(schemes_link)
            table = driver.find_elements_by_id("myTable")[0]
            hierarchy_schemes = hierarchy_grants+ "$" + name_of_hierarchy_schemes[index_schemes]
            (path_schemes,links_of_treasury_url_string,links_of_treasury_name, name_of_hierarchy_trea) = base_function(driver,path_grants, links_of_schemes_name[index_schemes], fiscal_year, hierarchy_schemes, table)

            for index_treasury, treasury_link in enumerate(links_of_treasury_url_string):

                print(links_of_treasury_name[index_treasury])

                driver.get(treasury_link)

                table = driver.find_elements_by_id("myTable")[0]

                hierarchy_trea = hierarchy_schemes+ "$" + name_of_hierarchy_trea[index_treasury]
                base_function(driver,path_schemes, links_of_treasury_name[index_treasury], fiscal_year, hierarchy_trea, table)
