from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.common.by import By
from dataclasses import dataclass

@dataclass
class loginWeb():
    url: str = "https://www.linkedin.com/login/it"
    driver_path: str = "C:/Users/ADMIN/botIsra/chromedriver.exe"
    browser = Chrome(executable_path = driver_path)
    browser_sear: str = ""
    def __post_init__(self):
        self.browser.get(self.url)        
        search_id = "username"
        search_id_psw = "password"
        element_search = self.browser.find_element_by_id(search_id)
        element_search.send_keys("giorgio.defilippo@tech-engineering.it")
        element_search_psw = self.browser.find_element_by_id(search_id_psw)
        element_search_psw.send_keys("giorgio77")
        element_search.submit()
        self.browser_sear = self.browser.current_url
    
    def ricerca_candidato(self, search_bar):
        self.browser.get(self.browser_sear)
        search_ = "search-global-typeahead__input.always-show-placeholder"
        rese = self.browser.find_element_by_class_name(search_)
        rese.clear()
        rese.send_keys(search_bar)
        rese.send_keys(Keys.ENTER)

    def filter_by_person(self):
        cl_persone = "artdeco-pill.artdeco-pill--slate.artdeco-pill--choice.artdeco-pill--2.search-reusables__filter-pill-button.search-reusables__filter-pill-button"
        click_per = self.browser.find_element_by_class_name(cl_persone)
        click_per.click()

    def lunch_location(self, xid_lo,xid_inp,ok_button,location_search):
        click_loc = self.browser.find_element_by_xpath(xid_lo)
        sleep(2)
        click_loc.click()
        sleep(2)
        click_inp = self.browser.find_element_by_xpath(xid_inp)
        click_inp.clear()
        click_inp.send_keys(location_search)
        sleep(3)
        click_inp.send_keys(Keys.DOWN)
        sleep(3)
        click_inp.send_keys(Keys.ENTER)
        sleep(1)
        clic_mostr = self.browser.find_element_by_xpath(ok_button)
        clic_mostr.click()

    def filter_role_location(self, role_search,location_search):
        self.ricerca_candidato(role_search)
        sleep(3)
        self.filter_by_person()
        sleep(2)
        button_loc = "/section/div/nav/div/ul/li[4]/div/span/button"
        button_inp = "/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[1]/div/div/input"
        button_ok_search ="/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]/span"
        #html/body/div[6]/div[3]/div/div[2]/section/div/nav/div/ul/li[4]/div/span/button
        #/html/body/div[6]/div[3]/div/div[2]/section/div/nav/div/ul/li[4]/div/span/button
        #/html/body/div[6]/div[3]/div/div[2]/section/div/nav/div/ul/li[4]/div/span/button
        #/html/body/div[6]/div[3]/div/div[2]/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]/span
        #"/html/body/div[7]/div[3]/div/div[2]/section/div/nav/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]/span"
        try:
            part1 = "/html/body/div[6]/div[3]/div/div[2]"
            loc_ser = part1+button_loc
            loc_inp = part1+button_inp
            loc_ok = part1+button_ok_search
            self.lunch_location(loc_ser, loc_inp, loc_ok, location_search)
        except:
            pass
        try:
            part2 = "/html/body/div[7]/div[3]/div/div[2]"
            loc_ser = part2+button_loc
            loc_inp = part2+button_inp
            loc_ok = part2+button_ok_search
            self.lunch_location(loc_ser, loc_inp, loc_ok, location_search)
        except:
            pass