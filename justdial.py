from selenium import webdriver
import pandas as pd 
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

#chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.11 Safari/537.36")
chrome_options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=chrome_options)  

csv_data = []

number_intercept  = {
    'icon-acb' : '0',
    'icon-yz' : '1',
    'icon-wx' : '2',
    'icon-vu' : '3',
    'icon-ts' : '4',
    'icon-rq' : '5',
    'icon-po' : '6',
    'icon-nm' : '7',
    'icon-lk' : '8',
    'icon-ji' : '9',
    'icon-fe' : '(',
    'icon-dc' : '+',
    'icon-hg' : ')',
    'icon-ba' : '-',
    'c' : ' ',
}

page = 1
total_page = 50
save_dir_name = ""

for i in range(page, total_page + 1):

    page_data = []
    init_url = 'https://www.justdial.com/Gwalior/Electronic-Shops/nct-10185144/page-{0}'.format(page)
    driver.get(init_url)
    getCards = driver.find_elements_by_css_selector('.jbbg')
    if len(getCards) == 0 : getCards = driver.find_elements_by_css_selector('.jgbg') 

    for card in getCards:
        seller_name = card.find_element_by_css_selector('.lng_cont_name').text
        number = ''
        for number_class in card.find_elements_by_css_selector('.mobilesv'):
            class_ = number_class.get_attribute('class').split(' ')[1]
            number += number_intercept[class_]

        csv_data.append([seller_name, number])
        page_data.append([seller_name, number])

    create_frame = pd.DataFrame(page_data, columns=['Store Name', 'Number'])
    with open('./{0}/page-{1}.csv'.format(save_dir_name, page), 'w', newline='') as file:
        create_frame.to_csv(file, index=False )
    page +=1


create_frame = pd.DataFrame(csv_data, columns=['Store Name', 'Number'])
with open('./{0}/full.csv'.format(save_dir_name), 'w', newline='') as file:
    create_frame.to_csv(file, index=False)

