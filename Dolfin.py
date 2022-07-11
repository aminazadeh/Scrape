from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from locators import PageLocators
import collections
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re


def Get_url(numUrl):
    

    if numUrl not in {'divar', 'shey'}: 
        raise ValueError 
            

    Dict = {1: 'https://divar.ir', 2:'https://www.sheypoor.com'}
    
    if numUrl == 'divar':
        return Dict.get(1)
    elif numUrl == 'sheyp':
        return Dict.get(2)
    else:
        return None
    

def Get_path(PATH):

    if PATH == 'chrome'.lower():
        return 'C:\\Users\\mehdi\\Desktop\\Driver\\chromedriver.exe'

    elif PATH == 'firefox'.lower():
        return None


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
nums = [i for i in range(1,10)]
dictofCities = dict(zip(nums, CityUrls))


# for i, j in zip(dictofCities.keys(), dictofCities.values()):
#     print(i, j)

Options = {'Vehicle': ['/vehicles', '/auto']}

goto = dictofCities[3] + Options.get('Vehicle')[1]

    
def Init():

    img = list()
    desc = list()
    href = list()
    cnt = 0

    brow.get(goto)
    brow.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/aside/div/section[2]/div[7]/label/div/div/div').click()

    time.sleep(5)

    source = brow.page_source
    soup = BeautifulSoup(source, 'html.parser')
    
    last_height = brow.execute_script("return document.body.scrollHeight")

    def EachPage():
        for elem in soup.find('div', {'class': 'browse-post-list'}).find_all('div', {'class': PageLocators.DIV}):
    
            desc.append(elem.h2.get_text())    
            img.append(elem.img['data-src'])
            href.append(Get_url('divar') + elem.a['href'])

        cnt = sum([1 for _ in range(len(href))])
        print(href)
        return cnt

    
    if soup.find('div', {'style': 'top:0;position:absolute;height:100%;width:100%'}):
        EachPage()
        
        while cnt % 2 == 0:
            brow.execute_script(f'window.scrollTo(0, {last_height});')

            time.sleep(5)

            new_height = brow.execute_script('return document.body.scrollHeight')
            
            if new_height == last_height:
                break

            last_height = new_height
            EachPage()

    else:
        EachPage()


Init()