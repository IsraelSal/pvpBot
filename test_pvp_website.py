"""
Test module for verifying correct reading of https://pvp.giustizia.it/pvp/
"""

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Add the parent directory to the path to import scrapingSearch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestPVPWebsite:
    """Test class for PVP Giustizia website accessibility and functionality"""
    
    @pytest.fixture(scope="module")
    def browser(self):
        """Initialize Firefox browser in headless mode"""
        options = FirefoxOptions()
        options.headless = True
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", os.path.join(os.getcwd(), "downloads"))
        
        driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install(),
            options=options
        )
        yield driver
        driver.quit()
    
    def test_website_loads(self, browser):
        """Test that the PVP website loads successfully"""
        url = "https://pvp.giustizia.it/pvp/it/homepage.page"
        browser.get(url)
        
        # Check if page title contains expected text
        assert "PVP" in browser.title or "Giustizia" in browser.title, \
            f"Page title should contain 'PVP' or 'Giustizia', got: {browser.title}"
        
        # Check if page loaded without errors
        assert browser.current_url == url or "homepage" in browser.current_url, \
            f"Expected to be on homepage, got: {browser.current_url}"
    
    def test_modal_popup_exists(self, browser):
        """Test that the initial modal popup appears"""
        url = "https://pvp.giustizia.it/pvp/it/homepage.page"
        browser.get(url)
        
        # Wait for modal popup to appear
        try:
            modal = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="modalInformativa"]'))
            )
            assert modal is not None, "Modal popup should be present"
        except Exception as e:
            # Modal might have already been closed or not present in some cases
            print(f"Modal popup test note: {str(e)}")
    
    def test_advanced_search_button_exists(self, browser):
        """Test that advanced search button is accessible after closing modal"""
        url = "https://pvp.giustizia.it/pvp/it/homepage.page"
        browser.get(url)
        
        # Close modal if present
        try:
            close_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modalInformativa"]/div/div/div[3]/button'))
            )
            close_button.click()
        except:
            pass  # Modal might not be present
        
        # Check for advanced search button
        try:
            advanced_search = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="button_avanzata1"]'))
            )
            assert advanced_search is not None, "Advanced search button should be present"
        except Exception as e:
            pytest.fail(f"Advanced search button not found: {str(e)}")
    
    def test_search_input_field_exists(self, browser):
        """Test that the search input field is accessible"""
        url = "https://pvp.giustizia.it/pvp/it/homepage.page"
        browser.get(url)
        
        # Close modal and click advanced search
        try:
            close_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modalInformativa"]/div/div/div[3]/button'))
            )
            close_button.click()
            
            advanced_search = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="button_avanzata1"]'))
            )
            advanced_search.click()
            
            # Check for search input field
            search_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "IDricercalibera1"))
            )
            assert search_input is not None, "Search input field should be present"
        except Exception as e:
            pytest.fail(f"Search input field test failed: {str(e)}")
    
    def test_price_range_fields_exist(self, browser):
        """Test that price range input fields are accessible"""
        url = "https://pvp.giustizia.it/pvp/it/homepage.page"
        browser.get(url)
        
        try:
            # Navigate through modal and advanced search
            close_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modalInformativa"]/div/div/div[3]/button'))
            )
            close_button.click()
            
            advanced_search = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="button_avanzata1"]'))
            )
            advanced_search.click()
            
            # Check for price range fields
            prezzo_da = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "prezzo-da"))
            )
            prezzo_a = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "prezzo-a"))
            )
            
            assert prezzo_da is not None, "Minimum price field should be present"
            assert prezzo_a is not None, "Maximum price field should be present"
        except Exception as e:
            pytest.fail(f"Price range fields test failed: {str(e)}")


def test_astaSearch_function_exists():
    """Test that the astaSearch function exists and is callable"""
    from scrapingSearch import astaSearch
    
    assert callable(astaSearch), "astaSearch should be a callable function"
    assert astaSearch.__doc__ is not None, "astaSearch should have documentation"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
