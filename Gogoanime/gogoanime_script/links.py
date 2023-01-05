from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement


class AnimeLinks:
    def __init__(self, main_body_element: WebElement):
        self.boxes_element = main_body_element
        self.link_elements = self.get_boxes()

    def get_boxes(self):
        return self.boxes_element.find_elements(
            By.TAG_NAME,
            'li'
        )

    def get_new_link(self):
        link = self.link_elements[0].find_element(
            By.TAG_NAME,
            'a'
        ).get_attribute('href')
        return link
