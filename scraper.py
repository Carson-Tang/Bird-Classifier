import os
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from typing import List
from urllib.request import urlretrieve


def get_urls(soup: BeautifulSoup) -> List[str]:
    urls = [re.findall('\\((.*?)\\)', str(s)) for s in soup.select("a span")]
    urls = list(filter(None, urls))
    urls = [s[0].title() for s in urls]
    return urls


def make_dir(dir_name: str, path: str) -> None:
    if not os.path.exists(path + "/" + dir_name):
        os.mkdir(path + "/" + dir_name)


driver = webdriver.Chrome()
URL = "https://www.allaboutbirds.org/guide/browse/taxonomy"
USER_AGENT_STRING = "https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes"  # noqa: E501
headers = {'User-Agent': USER_AGENT_STRING}
r = requests.get(URL, headers=headers)
soup = BeautifulSoup(r.text, "lxml")
make_dir("BirdImages", os.getcwd())

taxonomy = get_urls(soup)

for family in taxonomy:
    r = requests.get(URL + "/" + family, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    link = soup.find_all("h3")
    bird_names = [name.text for name in link]
    bird_urls = [tag.a.get("href") for tag in link]
    for bird_name, bird_url in zip(bird_names, bird_urls):
        make_dir("_".join(bird_name.split()), os.getcwd() + "\\BirdImages\\")
        driver.get("https://www.macaulaylibrary.org/")
        try:
            element_present = EC.presence_of_element_located((
                              By.ID, "hero-search"))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        element = driver.find_element_by_id("hero-search")
        element.send_keys(bird_name)

        try:
            element_present = EC.presence_of_element_located((
                              By.CLASS_NAME, "Suggestion-text"))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        element.send_keys(u'\ue007')

        try:
            element_present = EC.presence_of_element_located((
                              By.CLASS_NAME, "RadioGroup-secondary"))
            WebDriverWait(driver, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        driver.find_element_by_class_name("RadioGroup-secondary").click()
