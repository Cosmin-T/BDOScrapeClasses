from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from util import *
import time


class BDOaccesslink():
    """ A general access to link """

    def __init__(self, URL, BASE_URL):
        """ Getting link """
        self.URL = URL
        self.BASE_URL = BASE_URL
        self.characters = []

    def access_wiki(self):
        """ Accessing the wiki """
        try:
            self.response = requests.get(self.URL)
            print("Fetched URL")
            self.soup = BeautifulSoup(self.response.content, 'html.parser')
            print("Parsed the page successfully")
        except Exception as e:
            print("Failed to fetch or parse URL:", str(e))

    def show_characters(self):
        """ Show Characters """
        self.characters = ["Warrior", "Valkyrie", "Berserker", "Tamer", "Musa", "Maehwa", "Ninja", "Kunoichi", "Wizard", "Witch", "Sorceress", "Ranger", "Dark Knight", "Striker", "Mystic"]
        print(f"\nClass:")
        for self.char in self.characters:
            print(f"\t{self.char}")

    def access_driver(self):
        """ Access the driver """
        self.access_wiki()
        self.options = Options()
        self.options.add_argument('-headless')
        self.driver = webdriver.Safari(options=self.options)
        self.driver.set_window_size(1400, 1440)

    def open_link(self):
        """ Opening the link with the specified character at the end of the url """
        self.link = f"{self.BASE_URL}{self.selector}"
        self.driver.get(self.link)

    def get_information(self):
        """ Get Summary, Style, Weapon, Secondary Weapon, Awakening Weapon, Stats Image """

        def get_element_text(xpath):
            try:
                wait = WebDriverWait(self.driver, 5)
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                element_text = element.text.strip()
                return element_text if element_text else None
            except Exception as e:
                print("An error occurred:", str(e))
                return None

        # Information categories and their XPaths
        categories = {
            'Summary': f"//p[contains(text(), '{self.selector}')]",
            'Style': '//*[@id="mw-content-text"]/div/aside/div[1]/div',
            'Weapon': '//*[@id="mw-content-text"]/div/aside/div[2]/div',
            'Secondary Weapon': '//*[@id="mw-content-text"]/div/aside/div[3]/div',
            'Awakening Weapon': '//*[@id="mw-content-text"]/div/aside/div[4]/div'
        }

        extracted_info = {}

        # Iterate over categories and extract information
        for category, xpath in categories.items():
            info_text = get_element_text(xpath)
            if info_text:
                print(f"\n{category}: \n{info_text}")
            else:
                print(f"No {category.lower()} information found")
            extracted_info[category] = info_text

        # Get Stats Image
        try:
            wait = WebDriverWait(self.driver, 5)
            stats = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mw-content-text"]/div/aside/figure[2]/a/img')))
            stats_src = stats.get_attribute("src")
            if stats_src:
                print(f"\nStats Image: \n{stats_src}")
            else:
                print("No stats image information found")
            extracted_info['Stats Image'] = stats_src
        except Exception as e:
            print("An error occurred:", str(e))
            extracted_info['Stats Image'] = None

        # Return the extracted information
        return extracted_info


    def character_selection(self):
        """ Selecting the character """
        while True:
            self.selector = input('\nChoose from the above list of Characters: \n')
            if self.selector == 'q':
                break
            if self.selector.strip().capitalize() in self.characters:
                self.open_link()
                print(f"**New Link Appended: {self.link}")
                self.get_information()
            else:
                print(f"\nError: Character '{self.selector.title()}' is not in the list of characters")

    def compare(self):
        """Comparing between two characters"""
        while True:
            self.selector1 = input("\nEnter the first character: ").capitalize()
            if self.selector1 == 'Q':
                break
            if self.selector1.strip() in self.characters:
                break
            else:
                print(f"\nError: Character '{self.selector1}' is not in the list of characters")

        while True:
            self.selector2 = input("Enter the second character: ").capitalize()
            if self.selector2 == 'Q':
                break
            if self.selector2.strip() in self.characters:
                break
            else:
                print(f"\nError: Character '{self.selector2}' is not in the list of characters")

        # Compare the selected characters
        if self.selector1 != 'Q' and self.selector2 != 'Q':
            print(f"\nComparing '{self.selector1}' and '{self.selector2}':")

            # Get info for the 1st character
            print(f"\nInformation for '{self.selector1}':")
            self.selector = self.selector1
            self.open_link()
            info_character1 = self.get_information()

            # Get information for the second character
            print(f"\nInformation for '{self.selector2}':")
            self.selector = self.selector2
            self.open_link()
            info_character2 = self.get_information()

            # Compare the information
            print("\nComparison:\n")
            for key in info_character1:
                value1 = info_character1[key]
                value2 = info_character2[key]
                print(f"\n{key}:")
                print(f"\t{self.selector1}: {value1}")
                print(f"\t{self.selector2}: {value2}")



    def menu(self):
        """ Selecting Menu """
        while True:
            self.m = ['Character Selection', 'Comparison']
            print("\nYou can type 'q' at any time to quit the app. Menu:")
            for i in self.m:
                print(f'\t{i}')
            self.main_selector = input('\nPlease choose an option: \n')
            if self.main_selector == 'q':
                break
            if self.main_selector.capitalize() == self.m[0].capitalize():
                self.show_characters()
                self.character_selection()
            else:
                self.show_characters()
                self.compare()





access = BDOaccesslink(URL, BASE_URL)
access.access_driver()
access.menu()