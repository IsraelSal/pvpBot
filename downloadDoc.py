from selenium.webdriver import Chrome
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def documentiImmobile(url):
    browser.get(url)
    fotgra = []
    vendita = []
    perizia = []
    div_link = browser.find_elements(By.TAG_NAME, "a")

    for d in div_link:
        if d.text.lower().find('fot') >= 0:
            fotgra.extend([d.get_attribute("href")])
        elif (d.get_attribute("href").find(".pdf")!=-1) and (d.text.lower().find('ven') >= 0):
            vendita.extend([d.get_attribute("href")])
        elif (d.get_attribute("href").find(".pdf")!=-1) and (d.text.lower().find('peri') >= 0):
            perizia.extend([d.get_attribute("href")])

    return fotgra, vendita, perizia