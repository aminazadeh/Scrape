import time
import re
import os 
import io
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from PIL import Image
from urllib.error import HTTPError, URLError
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC #further use 
from selenium.webdriver.chrome.options import Options
from unidecode import unidecode
from Locators import PageLocators


divar = 'https://divar.ir'
    
# Further use
def Get_path(PATH):

    if PATH == 'chrome':
        return 'C:\\Users\\mehdi\\Desktop\\Driver\\chromedriver.exe'

    return None


def Unidecode(number) -> str:
    
    return unidecode(u'{0}'.format(number))


def Config_browser():
    path = Get_path('chrome')
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    browser = webdriver.Chrome(executable_path=path, options=chrome_options)
   
    return browser



browser = Config_browser()
lstOfCities = []
lstOfLinks = []

def Parser(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup

#Extracting City Urls from the menu

try:
    soup = Parser(divar)

    try:

        for obj in soup.find('div', {'class': 'city-group'}).find_all('a'):
            lstOfCities.append(obj.get_text())


        for obj2 in soup.find('div', {'class': 'city-group'}).find_all('a', 
            href = re.compile('^(/s/)')):
                lstOfLinks.append(obj2.attrs['href'])

        CityUrls = list(map(lambda n: divar + n ,lstOfLinks))
        nums = [i for i in range(len(CityUrls))]
        dictofCities = dict(zip(nums, CityUrls))

    except AttributeError as e:
        print('Tag not found!')
    
except HTTPError as h:
    print('Page not found')

   

# Hard-coded
options = {'Vehicle': ['/vehicles', '/auto']}

goto = dictofCities[2] + options.get('Vehicle')[1]

# done 3 4 0 1
 

def Init():
    
    href = list()
    img = list()
    browser.get(goto)
    browser.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/aside/div/section[2]/div[7]/label/div/div/div').click()

    time.sleep(7)

    source = browser.page_source
    soup = BeautifulSoup(source, 'html.parser')
    
    def EachPage():

        index = 0
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            
            source = browser.page_source
            soup = BeautifulSoup(source, 'html.parser')
            time.sleep(7)

            """
            program scrapes (description, href, and img links) of first page,
            then it scrolls down and makes a beautiful soup object out of new div tags and scrapes the above elements again
            """

            for elem in soup.find('div', {'class': 'browse-post-list'}).find_all('div', {'class': PageLocators.DIV}):

                if elem not in img: 
                    img.append(elem.img['data-src'])

                if elem not in href:
                    href.append(divar + elem.a['href'])

            count = sum([1 for _ in range(len(href))])
            
            new_height = browser.execute_script("return document.body.scrollHeight")

            # Check whether scrolling pages are finished
            
            if new_height == last_height:
                break
            
            if count >= 25:
                break
            
            last_height = new_height
        
        
        # Downloading images

        try:
            for image in img:
                    
                
                Content = requests.get(image).content
                image_file = io.BytesIO(Content)
                Image_ = Image.open(image_file)
                file_path = '' + f'pic{index}.jpg'
                
                with open(file_path, 'wb') as f:
                    Image_.save(f, 'JPEG')
                    index += 1

        except Exception as e:
            print('-------Image Not Downloaded-----')

        
            
    # Checking whether the scraper is scraping from the first page!
    if soup.find('div', {'style': 'top:0;position:absolute;height:100%;width:100%'}):
        EachPage()
        
    

if __name__ == '__main__':
    Init()