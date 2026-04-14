from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
import numpy as np
import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def astaSearch(LOCALITA, MESE_ASTA: list, PREZZO_RANGE: list, cliente: str):
    """
    Search for auctions on the PVP Giustizia website using Firefox browser.
    
    Args:
        LOCALITA: Location to search for
        MESE_ASTA: List of months to filter auctions
        PREZZO_RANGE: Price range [min, max]
        cliente: Client name for saving results
    """
    # Configure Firefox options
    options = FirefoxOptions()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", os.path.join(os.getcwd(), "downloads"))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    
    # Use headless mode for automated testing (can be disabled for debugging)
    options.headless = True
    
    url = "https://pvp.giustizia.it/pvp/it/homepage.page"
    
    # Initialize Firefox driver with webdriver-manager for automatic driver management
    service = FirefoxService(GeckoDriverManager().install())
    browser = webdriver.Firefox(service=service, options=options)
    browser.get(url)
    
    # Close the initial modal popup
    class_b = '//*[@id="modalInformativa"]/div/div/div[3]/button'
    element_search = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, class_b))
    )
    element_search.click()

    # Click on advanced search button
    id_re = '//*[@id="button_avanzata1"]'
    rese = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, id_re))
    )
    rese.click()
    
    # Enter location in search field
    input_id = "IDricercalibera1"
    wait = WebDriverWait(browser, 10)
    search = wait.until(EC.element_to_be_clickable((By.ID, input_id)))
    search.clear()
    search.send_keys(f"{LOCALITA}")
    search.submit()

    # Sort by sale date
    ordina = "astaMinima"
    df = Select(wait.until(EC.presence_of_element_located((By.ID, ordina))))
    df.select_by_visible_text("Data vendita ▼")

    # Set price range
    prezzo_id = "prezzo-da"
    prezzo_id_ = "prezzo-a"
    p_da = wait.until(EC.element_to_be_clickable((By.ID, prezzo_id)))
    p_a = wait.until(EC.element_to_be_clickable((By.ID, prezzo_id_)))

    p_da.clear()
    p_a.clear()

    p_da.send_keys(PREZZO_RANGE[0])
    p_a.send_keys(PREZZO_RANGE[1])

    p_a.submit()

    # Set pagination to 50 results per page
    pg_id = "select-paginazione"
    pg_ = Select(wait.until(EC.presence_of_element_located((By.ID, pg_id))))
    pg_.select_by_visible_text("50")

    # Click on list view button
    list_ele = "glyphicon.glyphicon-list.hidden-xs"
    clic_list = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, list_ele)))
    clic_list.click()
    
    # Filter auction dates
    today_plus3Days = datetime.datetime.now() + datetime.timedelta(days=3)
    src = browser.page_source
    
    # Find dates matching the specified months in 2022
    text_found = [
        date_ for month in MESE_ASTA 
        for date_ in re.findall(f'../{month}/2022', src) 
        if datetime.datetime.strptime(date_, '%d/%m/%Y') >= today_plus3Days
    ]

    val = [re.search(dat, src) for dat in text_found]
    print(f"Numero di date valide per possibili aste: {len(val)}")

    # Extract content IDs from matching results
    n = 600
    id_link_found = []
    for m in val:
        text_f = src[m.start()-n:m.end()]
        if text_f.find(LOCALITA[-4:]) >= 0 and text_f.find(LOCALITA) >= 0:
            id_link_found.extend([
                f.split("=")[1] 
                for f in text_f.split("&amp;") 
                if f.find("contentId=") >= 0
            ])

    print(f"Numero totale di aste effetivamente valide : {len(id_link_found)}")

    # Extract all links and filter for valid auction links
    div_link = browser.find_elements(By.TAG_NAME, "a")
    links = [d.get_attribute("href") for d in div_link]
    valid_links = [d for d in links if d is not None]
    link_asta = [s for s in valid_links for id_ in id_link_found if id_ in s]
    unique_ = np.unique(np.array(link_asta))
    print(f"I migliori annunci trovati {unique_.shape} per l'intervallo di prezzo {PREZZO_RANGE} nella zona di {LOCALITA}")
    
    # Save results to file
    path = f"{os.getcwd()}/data/{cliente}"
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)
    
    if len(unique_) > 0:
        np.savetxt(f"./data/{cliente}/{LOCALITA}.txt", unique_, fmt='%s', delimiter="\n")
    
    # Close browser properly
    browser.quit()
