#################################################
# Class to create the webdriver object to run selenium
# I like to name it WebDriverTorso (with Torso at the end)
# to avoid using reserved names (also as a reference to a
# youtube channel that google used for upload tests)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import traceback
#change the above webdriver options class if not using firefox driver... 
#from selenium.webdriver.{$webdriver}.options import Options 

class WebDriverTorso:
    def __init__(self, params):
        self.target_url = params.get('url')
        self.options = Options()

        #forcing locale to EN because I use ñ at home
        self.options.set_preference('intl.accept_languages', 'en-US')
        self.options.headless = params.get('headless_mode')

        #replace this if using a different driver
        self.driver = webdriver.Firefox(options=self.options)

    def wait_element_click(self, query, time=5):
        try:
            target_element = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable(('xpath', query))).click()
        except TimeoutException as e:
            print("TimeoutException")
        except Exception as e:
            print(traceback.format_exc())


    def login(self):
        ##################
        # Optional: use this if you want to log in
        # TODO: populate function
        pass

    def finish(self):
        #call this function when completed your task
        self.driver.quit()

    def run(self):
        self.driver.get(self.target_url) #open the target URL
        self.driver.implicitly_wait(10) #adding a 10 second wait to make sure the page has time to load