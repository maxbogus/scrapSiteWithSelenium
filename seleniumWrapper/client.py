import time
from selenium import webdriver


class SeleniumClient:
    chromeDriver = './chromedriver'
    driver = webdriver.Chrome(chromeDriver)

    @staticmethod
    def get_elements_by_css_locator(self, locator):
        result = None
        try:
            result = self.driver.find_elements_by_css_selector(locator)
        except Exception as exception:
            print('Cannot find {}. Exception: {}'.format(locator, exception))
        return result

    @staticmethod
    def get_element_by_css_locator(self, locator):
        result = None
        try:
            result = self.driver.find_element_by_css_selector(locator)
        except Exception as exception:
            print('Cannot find {}. Exception: {}'.format(locator, exception))
        return result

    @staticmethod
    def get_element_by_id(self, locator):
        result = None
        try:
            result = self.driver.find_element_by_id(locator)
        except Exception as exception:
            print('Cannot find {}. Exception: {}'.format(locator, exception))
        return result

    @staticmethod
    def get_page(self, page_url):
        print(page_url)
        self.driver.get(page_url)
        time.sleep(2)

    @staticmethod
    def open_nasa_site(self):
        my_url = 'https://images.nasa.gov/'
        self.get_page(self, my_url)

    @staticmethod
    def terminate(self):
        self.driver.close()
