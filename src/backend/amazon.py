import requests
import json
from flask.views import MethodView
from flask import jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup
import time

import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class AmazonService(MethodView):
    def test_function(self,procnum,return_dict,url):
        CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = CHROME_PATH

        driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                chrome_options=chrome_options
                                )
        driver.get('https://www.amazon.in')
        email = driver.find_element(By.ID ,"twotabsearchtextbox")
        email.send_keys(url)
        email.send_keys(Keys.ENTER)
         # select = Select(driver.find_element(By.NAME,'s'))

        # select.select_by_visible_text("Price: Low to High")

        # time.sleep(2)
        return_dict[procnum] = driver.page_source     

    def test_function2(self,procnum,return_dict,url):
        CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
        CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
        WINDOW_SIZE = "1920,1080"

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = CHROME_PATH

        driver2 = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                chrome_options=chrome_options
                                )
        
        driver2.get('https://www.flipkart.com/search?q={}'.format(url))

        return_dict[procnum] = driver2.page_source

    @cross_origin()
    def get(self,url):

        return_dict={}
        t1 = threading.Thread(target=self.test_function, args=[1,return_dict,url]) 
        t1.start()
        t2 = threading.Thread(target=self.test_function2, args=[2,return_dict,url]) 
        t2.start()

        t1.join() 
        t2.join()

        # response = jsonify({'html':driver.page_source},{'html2':driver2.page_source})
        response ={'html':return_dict[1],'html2':return_dict[2]}
        return response