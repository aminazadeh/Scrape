from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import io
from PIL import Image
import time
import re
from urllib.error import HTTPError, URLError
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from locators import PageLocators




def Get_url(numUrl):
    

    if numUrl not in {'divar', 'shey'}: 
        raise ValueError 
            

    Dict = {1: 'https://divar.ir', 2:'https://www.sheypoor.com'}
    
    if numUrl == 'divar':
        return Dict.get(1)

    return Dict.get(2)
    
    
# Further use
def Get_path(PATH):

    if PATH == 'chrome':
        return 'C:\\Users\\mehdi\\Desktop\\Driver\\chromedriver.exe'

    return None

# (1920*1080) loading all the elements
def Config_browser():
    path = Get_path('chrome')
    chrome_options = Options()
    # chrome_options.add_argument('--kiosk')
    browser = webdriver.Chrome(executable_path=path)
    browser.set_window_size(1920, 1080)
    return browser


url = Get_url('divar')
brow = Config_browser()

lstOfCities = []
lstOfLinks = []

#Extracting City Urls from the menu
try:
    html = urlopen(url)
    bs_object = BeautifulSoup(html.read(), 'html.parser')

    try:

        for obj in bs_object.find('div', {'class': 'city-group'}).find_all('a'):
            lstOfCities.append(obj.get_text())


        for obj2 in bs_object.find('div', {'class': 'city-group'}).find_all('a', 
            href = re.compile('^(/s/)')):
                lstOfLinks.append(obj2.attrs['href'])

    except AttributeError as e:
        print('Tag not found!')
    
except HTTPError as h:
    print('Page not found')


CityUrls = list(map(lambda n: url + n ,lstOfLinks))
nums = [i for i in range(len(CityUrls))]
dictofCities = dict(zip(nums, CityUrls))


# Hard-coded
options = {'Vehicle': ['/vehicles', '/auto']}

goto = dictofCities[3] + options.get('Vehicle')[1]


    
def Init():

    img = list()
    desc = list()
    href = list()
  
    brow.get(goto)
    brow.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/aside/div/section[2]/div[7]/label/div/div/div').click()

    time.sleep(7)

    source = brow.page_source
    soup = BeautifulSoup(source, 'html.parser')
    
    def EachPage():
        index = 0
        
        last_height = brow.execute_script("return document.body.scrollHeight")
        while True:
            
            brow.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            
            source = brow.page_source
            soup = BeautifulSoup(source, 'html.parser')
            time.sleep(7)

            """
            program scrapes (description, href, and img links) of first page,
            then it scrolls down and makes a beautiful soup object out of new div tags and scrapes the above elements again
            """

            for elem in soup.find('div', {'class': 'browse-post-list'}).find_all('div', {'class': PageLocators.DIV}):

                if elem not in desc:
                    desc.append(elem.h2.get_text())  

                if elem not in img: 
                    img.append(elem.img['data-src'])

                if elem not in href:
                    href.append(Get_url('divar') + elem.a['href'])

                

            new_height = brow.execute_script("return document.body.scrollHeight")

            # Check whether scrolling pages are finished
            if new_height == last_height:
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
    

Init()