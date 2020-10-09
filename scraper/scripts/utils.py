#Importing packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pdb
import time 
import os
import csv
import glob

class SeleniumScrappingUtils(object):
      
    def base_function(self,driver,dir,head_name,fiscal_year,hierarchy, table):
        '''
        Baisc function that calls all the other function and return the needed variables
        (driver = chromedriver, dir = parent directory, head_name = name of folder (name of head),
        fiscal_year = year selected,hierarchy = hierarchy string, table = selected table)
        '''
        path = self.path_generator_dir_maker(driver,dir,str(head_name))
        self.table_to_csv(driver,path,head_name,table)
        self.add_columns(driver,path,head_name,fiscal_year, hierarchy)
        (links_url_string,links_name,name_of_hierarchy) = self.sel_elem_to_links(driver,table)
        return(path,links_url_string,links_name,name_of_hierarchy)

    def section_selector(self,Select,driver,fiscal_year,url_of_section):
        '''
        select fiscal year and section
        '''
        driver.get('http://koshvani.up.nic.in/')

        close_button = driver.find_element_by_class_name("open_button").click()
        # maximising because the fiscal year is not interactive in smaller window (need to discuss)
        driver.maximize_window() 
        time.sleep(3)
        select = Select(driver.find_element_by_id('ddlFinYear'))
        select.select_by_visible_text(fiscal_year)
        close_button = driver.find_element_by_class_name("open_button").click()
        driver.get(url_of_section)

    def table_to_csv(self,driver,path,name,table):
        '''
        Converting html table to csv (driver = chrome driver, path = path to save csv file, 
        name = name of file, table = selected table)
        '''
        with open(os.path.join(path+"/" + str(name)+'.csv'), 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            for row in table.find_elements_by_css_selector('tr')[0:1]:
                wr.writerow([d.text for d in row.find_elements_by_css_selector('th')])
            for row in table.find_elements_by_css_selector('tr')[1:]:
                wr.writerow([d.text for d in row.find_elements_by_css_selector('td')])

    def add_columns(self,driver,path,name,fiscal_year, hierarchy):
        '''
        This function add columns to downloaded csv
        driver = chrome driver, path = path of saved csv file, name = name of file, fiscal_year = year selected
        hierarchy = hierarchy string
        '''

        file_df = pd.read_csv(path+"/" + name + ".csv")
        file_df['fiscal_year'] = fiscal_year
        file_df['hierarchy'] = hierarchy
        file_df.to_csv(path+"/" + name + "_prep.csv", index = False)
           
    def sel_elem_to_links(self,driver,table):
        '''
        This function converts selenium list of links to href text and name
        '''
        links_sel = driver.find_elements_by_class_name("Hyperlink")
        links_url_string = [links_sel[i].get_attribute('href') for i in range(len(links_sel))]
        links_name = [links_sel[i].text.split('-')[0] for i in range(len(links_sel))]
        name_of_hierarchy = [links_sel[i].text for i in range(len(links_sel))]
        return (links_url_string,links_name,name_of_hierarchy)

    def path_generator_dir_maker(self,driver,parent_directory, name_of_folder):
        '''
        This function generates path from parent_directory to name_of_folder
        '''
        child_directory =  str(name_of_folder)
        path = os.path.join(parent_directory, child_directory) 
        os.mkdir(path)
        return(path)

    def table_download(self,folder_to_download,driver,path,name,table,columns):
        '''
        Used with tables where multiindex is found
        '''
        driver.find_elements_by_id("btnExport")[0].click()
        time.sleep(3)
        os.rename(folder_to_download+ "/"+"Excel.xls" , path+"/" + str(name)+".xls")
        html_df = pd.read_html(path+"/" + str(name)+".xls")
        html_df[0].columns = columns
        html_df[0].to_csv(path+"/" + str(name)+".csv",index = False)


