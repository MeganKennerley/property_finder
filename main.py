import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

CHROME_WEB_DRIVER = os.environ.get("CHROME_WEBDRIVER")

PROPERTY_WEBSITE = os.environ.get("PROPERTY_WEBSITE")
GOOGLE_FORM = os.environ.get("GOOGLE_FORM")


def get_property_lists():
    global PROPERTY_WEBSITE
    response = requests.get(PROPERTY_WEBSITE)
    soup = BeautifulSoup(response.text, "html.parser")
    properties = soup.find_all(class_="l-searchResult is-list")
    addresses = []
    prices = []
    links = []
    for property in properties:
        address = property.find(class_="propertyCard-address").getText().strip()
        price = property.find(class_="propertyCard-priceValue").getText().split()[0]
        link = property.find("a", attrs={'class': 'propertyCard-priceLink'})["href"]

        addresses.append(address)
        prices.append(price)
        links.append(link)

    return addresses, prices, links


def fill_in_form(addresses, prices, links):
    global CHROME_WEB_DRIVER, GOOGLE_FORM
    service = Service(executable_path=CHROME_WEB_DRIVER)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(GOOGLE_FORM)

    for n in range(len(addresses)):
        address_input = driver.find_element(by=By.XPATH,
                                            value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]"
                                                  "/div/div[1]/input")
        address_input.send_keys(addresses[n])

        price_input = driver.find_element(by=By.XPATH,
                                          value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/"
                                                "div/div[1]/input")
        price_input.send_keys(prices[n])

        link_input = driver.find_element(by=By.XPATH,
                                         value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/"
                                               "div/div[1]/input")
        link_input.send_keys(links[n])

        submit_button = driver.find_element(by=By.XPATH,
                                            value="//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
        submit_button.click()

        submit_another = driver.find_element(by=By.XPATH,
                                             value="/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
        submit_another.click()
        time.sleep(0.5)


def main():
    addresses, prices, links = get_property_lists()
    fill_in_form(addresses, prices, links)


main()
