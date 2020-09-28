#Importing packages
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import pdb
import time 
import os
import csv
import glob

def base_function(driver,dir,head_name,fiscal_year,hierarchy, table):
'''
Baisc function that calls all the other function and return the needed variables
(driver = chromedriver, dir = parent directory, head_name = name of folder (name of head),
fiscal_year = year selected,hierarchy = hierarchy string, table = selected table)
'''
    path = path_generator_dir_maker(driver,dir,str(head_name))
    table_to_csv(driver,path,head_name,table)
    add_columns(driver,path,head_name,fiscal_year, hierarchy)
    (links_url_string,links_name,name_of_hierarchy) = sel_elem_to_links(driver,table)
    return(path,links_url_string,links_name,name_of_hierarchy)

def table_to_csv(driver,path,name,table):
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

def add_columns(driver,path,name,fiscal_year, hierarchy):
    '''
    This function add columns to downloaded csv
    driver = chrome driver, path = path of saved csv file, name = name of file, fiscal_year = year selected
    hierarchy = hierarchy string
    '''

    file_df = pd.read_csv(path+"/" + name + ".csv")
    file_df['fiscal_year'] = fiscal_year
    file_df['hierarchy'] = hierarchy
    file_df.to_csv(path+"/" + name + "_prep.csv", index = False)
       
def sel_elem_to_links(driver,table):
    '''
    This function converts selenium list of links to href text and name
    '''
    links_sel = driver.find_elements_by_class_name("Hyperlink")
    links_url_string = [links_sel[i].get_attribute('href') for i in range(len(links_sel))]
    links_name = [links_sel[i].text.split('-')[0] for i in range(len(links_sel))]
    name_of_hierarchy = [links_sel[i].text for i in range(len(links_sel))]
    return (links_url_string,links_name,name_of_hierarchy)

def path_generator_dir_maker(driver,parent_directory, name_of_folder):
    '''
    This function generates path from parent_directory to name_of_folder
    '''
    child_directory =  str(name_of_folder)
    path = os.path.join(parent_directory, child_directory) 
    os.mkdir(path)
    return(path)

