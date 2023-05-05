import pandas as pd
import logging
from logging.config import fileConfig
from lxml import etree
import os
import re
import requests
from requests.adapters import HTTPAdapter
import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import shutil
from urllib3.util import Retry

MAX_RELOADS = 3
SLEEP_TIME = 2
class SeleniumScrappingUtils(object):
    def __init__(self, path):
        self.path = path
        self.url = url
        self.browser = browser
        
    def get_tender_id(path):
        dataframe = pd.read_csv(path)
        tender_id = dataframe["tender.id"][dataframe['tender.stage'] == "AOC"]
        return tender_id
    
    def get_multiple_page_elements(browser,xpath = None):
        '''
        returns list of page element identifies with the given path
        '''
        page_element = WebDriverWait(browser.driver, SLEEP_TIME).until(EC.presence_of_all_elements_located((By.XPATH,xpath)))
        return page_element
    
    def get_page_element(browser, xpath=None):
        ''' Get page element by xpath
        '''
        page_element = WebDriverWait(browser.driver, SLEEP_TIME).until(EC.presence_of_element_located((By.XPATH,xpath)))
        return page_element
    def input_text_box(browser, select_element, text=None):
        '''
        Input text in input box
        '''
        select_element.send_keys(text)
    def save_image_as_png(image_element):
        '''
        Save a image from web to png helps in captcha breaking 
        '''
        with open('captcha_image.png', 'wb') as file:
             file.write(image_element.screenshot_as_png)
    def get_text_from_element(element):
        ''' Extracts name from webelement'''
        name_of_element = [element[i].text for i in range(len(element))]
        return name_of_element
    def extract_vertical_table(table_section,name_of_file,skip_header_number = None):
        '''
        Extracts vertical tables
        '''
        with open(str(name_of_file)+".csv", 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            for row in table_section.find_elements_by_css_selector('tr')[skip_header_number:]:
                wr.writerow([d.text for d in row.find_elements_by_css_selector('td,th')])
    def extract_horizontal_table(table_section,name_of_file,skip_header_number = None):
        '''
        Extracts horizontal tables
        '''
        with open(str(name_of_file) + ".csv", 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            for row in table_section.find_elements_by_css_selector("tbody"):
                wr.writerow([d.text for d in row.find_elements_by_css_selector('td:nth-of-type(2n+1)')[skip_header_number:]])
                wr.writerow([d.text for d in row.find_elements_by_css_selector('td:nth-of-type(2n+2)')])
    
    def is_file_downloaded(filename, timeout=60):
        end_time = time.time() + timeout
        while not os.path.exists(filename):
            time.sleep(1)
            if time.time() > end_time:
                print("File not found within time")
                return False

        if os.path.exists(filename):
            print("File found")
            return True
        
    def select_element(select_element, text=None):
        select = Select(select_element)
        select.select_by_visible_text(text)

