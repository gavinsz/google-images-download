# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait  
from time import sleep  
import os
import codecs
from utils import *

if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
    driver.set_window_size(1280, 1000) 
    driver.implicitly_wait(15)
    url = 'http://top.iqiyi.com/paopao.html'
    driver.get(url)

    '''
    load_more = driver.find_element_by_class_name('dn')
    #点击显示更多
    count = 0
    while count < 5:
        load_more.click
        count += 1
    '''
    stars_list = []
    top_details = driver.find_element_by_class_name('topDetails')
    if top_details:
        h3_list = top_details.find_elements_by_tag_name('h3')
        for it in h3_list:
            link = it.find_element_by_tag_name('a')
            if link:
                name = link.get_attribute("text")
                name = name.strip()
                print(name)
                stars_list.append(name)

    write_list_to_file(stars_list, 'iqiyi-top-stars.txt')
    driver.close()