import os
import re
import requests
import time
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

CWD = os.getcwd()
URL = "https://www.allaboutbirds.org/guide/browse/taxonomy"
USER_AGENT_STRING = "https://developers.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes"  # noqa: E501
headers = {'User-Agent': USER_AGENT_STRING}

r = requests.get(URL, headers=headers)
soup = BeautifulSoup(r.text, "lxml")

make_dir("train", CWD)
make_dir("test", CWD)

taxonomy = get_urls(soup)

for family in taxonomy:
    r = requests.get(URL + "/" + family, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    link = soup.find_all("h3")

    make_dir(family, CWD + "\\train\\")
    make_dir(family, CWD + "\\test\\")

    bird_names = [name.text for name in link]

    for bird_name in bird_names:
        make_dir("_".join(bird_name.split()), CWD + "\\train\\")
        make_dir("_".join(bird_name.split()), CWD + "\\test\\")

        birdname = "_".join(bird_name.split())

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

        time.sleep(1)

        show_more_clicks = 0
        while show_more_clicks < 10:
            b = driver.find_elements_by_id("show_more")
            if len(b) <= 0:
                break
            try:
                html = driver.find_element_by_tag_name("html")
                html.send_keys(Keys.END)
                time.sleep(1)
                b[0].click()
                show_more_clicks += 1
            except:
                break

        imgs = driver.find_elements_by_tag_name("img")
        urls = []

        for img in imgs:
            try:
                if not img.get_attribute("src"):
                    continue
            except:
                break
            download_url = img.get_attribute("src")
            if download_url[-3:] != "480":
                continue
            urls.append(download_url)

        decile = len(urls)/10

        bird_name = "_".join(bird_name.split())

        for i in range(len(urls)):
            url = urls[i]
            file_name = "bird" + str(i+1) + ".png"
            if i < decile:
                urlretrieve(url, CWD + "\\test\\" +
                                 bird_name + "\\" + file_name)
            else:
                urlretrieve(url, CWD + "\\train\\" +
                                 bird_name + "\\" + file_name)
