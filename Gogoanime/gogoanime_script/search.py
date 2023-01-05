from selenium import webdriver
import os
from selenium.webdriver.common.by import By

import gogoanime_script.constants as const
from gogoanime_script.links import AnimeLinks


class Anime(webdriver.Chrome):
    def __init__(self, driver_path=r"E:\\CHROME DRIVERS\\chromedriver_win32", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(Anime, self).__init__(options=options)
        self.implicitly_wait(30)
        self.maximize_window()
        self.link_list = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def load_main_page(self):
        self.get(const.MainLink)

    def search(self, anime='one piece'):
        search_field = self.find_element(
            By.ID,
            'keyword'
        )
        search_field.clear()
        search_field.send_keys(anime)
        self.find_element(
            By.CSS_SELECTOR,
            'input[type="button"]'
        ).click()

        main_body_element = self.find_element(
            By.CLASS_NAME,
            'last_episodes'
        )
        new_link_element = AnimeLinks(main_body_element)
        self.get(new_link_element.get_new_link())

    def number_of_episode(self):
        number_of_episodes = 0
        for episode in self.get_episode_page():
            episode.click()
            episode_field = self.find_element(By.ID, 'episode_related')
            episode_len = episode_field.find_elements(
                By.TAG_NAME,
                'li'
            )
            number_of_episodes += len(episode_len)
        return number_of_episodes

    def get_episode_links(self):
        for episode in self.get_episode_page():
            episode.click()
            episode_field = self.find_element(By.ID, 'episode_related')
            episode_len = episode_field.find_elements(
                By.TAG_NAME,
                'li'
            )
            for links in episode_len:
                link = links.find_element(By.TAG_NAME, 'a').get_attribute('href')
                self.link_list.append(link)
        return self.link_list

    def download_page(self):
        self.login()
        p = self.current_window_handle
        parent = self.window_handles[0]
        child = self.window_handles[1]
        page = self.find_element(By.CLASS_NAME, 'favorites_book')
        link = page.find_element(By.CLASS_NAME, 'download')
        self.switch_to.window(child)
        print('Switching to child')
        link.find_element(By.TAG_NAME, 'a').click()

    def print_link_list(self):
        for i, link in enumerate(self.get_episode_links()):
            print(f'{i}: {link}')

    def get_episode_page(self):
        episode_groups = self.find_element(
            By.ID,
            "episode_page"
        )

        episodes = episode_groups.find_elements(
            By.TAG_NAME,
            'li'
        )
        return episodes

    def get_recent_episode(self):
        link = self.find_element(By.ID, 'load_ep')
        link.find_element(By.TAG_NAME, 'a').click()



        print('Login successfully...')

    def switch_tab(self):
        #p = self.current_window_handle
        parent = self.window_handles[0]
        child = self.window_handles[1]
        self.switch_to.window(child)
        print('Switching to child')
        self.get('https://www.google.com')
