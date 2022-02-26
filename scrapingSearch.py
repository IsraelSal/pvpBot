from genericpath import isfile
from selenium.webdriver import Chrome
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import os
import numpy as np
import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def astaSearch(LOCALITA,MESE_ASTA:list,PREZZO_RANGE:list, cliente:str ):

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "C:/Users/ADMIN/Downloads/DownloadbotIsr"}
    options.add_experimental_option("prefs",prefs)
    url = "https://pvp.giustizia.it/pvp/it/homepage.page"
    driver_path = "C:/Users/ADMIN/botIsra/chromedriver.exe"
    browser = Chrome(executable_path = driver_path, chrome_options=options)
    browser.get(url)
    #search_id = "modalInformativa"
    class_b = "btn-primary.bottoni-chiusura"
    element_search = browser.find_element_by_class_name(class_b)
    element_search.click()



    id_re = "class_affina_ricerca.pull-left.btn.btn-link.text-uppercase.button-ricerca-avanzata"
    rese = browser.find_element_by_class_name(id_re)
    rese.click()


    # Qui bisogna mettere un wait()
    
    input_id = "IDricercalibera1"
    wait = WebDriverWait(browser, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
    search = browser.find_element_by_id(input_id)
    search.clear()
    search.send_keys(f"{LOCALITA}")
    search.submit()


    ordina = "astaMinima"
    df = Select(browser.find_element_by_id(ordina))
    df.select_by_visible_text("Data vendita ▼")


    prezzo_id ="prezzo-da"
    prezzo_id_="prezzo-a"
    p_da = browser.find_element_by_id(prezzo_id)
    p_a = browser.find_element_by_id(prezzo_id_)

    p_da.clear()
    p_a.clear()

    p_da.send_keys(PREZZO_RANGE[0])
    p_a.send_keys(PREZZO_RANGE[1])

    p_a.submit()

    pg_id = "select-paginazione"
    pg_ = Select(browser.find_element_by_id(pg_id))
    pg_.select_by_visible_text("50")

    list_ele = "glyphicon.glyphicon-list.hidden-xs"
    clic_list = browser.find_element_by_class_name(list_ele)
    clic_list.click()
    today_plus3Days = datetime.datetime.now() + datetime.timedelta(days=3)
    src = browser.page_source
    #text_found = [date_ for month in MESE_ASTA for date_ in re.findall(f'../{month}/2022......', src)]
    text_found = [date_ for month in MESE_ASTA for date_ in re.findall(f'../{month}/2022', src) if datetime.datetime.strptime(date_, '%d/%m/%Y') >= today_plus3Days]

    val = [re.search(dat, src) for dat in text_found]
    print(f"Numero di date valide per possibili aste: {len(val)}")
    #text_found, val 
    #div_link

    ######################### Gabriel aqui estamos convirtiemdo el contenido html en stringa ##########
    ###############################  ###############################    ###############################
    n = 600
    id_link_found = []
    for m in val:
        text_f = src[m.start()-n:m.end()]
        if text_f.find(LOCALITA[-4:])>=0:
            if text_f.find(LOCALITA)>=0:
                id_link_found.extend([f.split("=")[1] for f in text_f.split("&amp;") if (f.find("contentId=")>=0)])# and f.find(LOCALITA[-4:])>=0)])

    print(f"Numero totale di aste effetivamente valide : {len(id_link_found)}")
    #id_page = [re.search(r'contentId=..........', pg_link) for pg_link in k]


    div_link = browser.find_elements(By.TAG_NAME, "a")
    links = [d.get_attribute("href") for d in div_link]
    valid_links = [d for d in links if d != None]
    link_asta = [s for s in valid_links for id_ in id_link_found if id_ in s]
    unique_ = np.unique(np.array(link_asta))
    print(f"I migliori annunci trovati {unique_.shape} per l'intervallo di prezzo {PREZZO_RANGE} nella zona di {LOCALITA}")
    path=f"{os.getcwd()}\\data\\{cliente}"
    isFile = os.path.isdir(path)
    if isFile==False:
        os.mkdir(f"data/{cliente}")
    if len(unique_)>0:
        np.savetxt(f"./data/{cliente}/{LOCALITA}.txt", unique_, fmt = '%s', delimiter="\n")
    browser.close()
