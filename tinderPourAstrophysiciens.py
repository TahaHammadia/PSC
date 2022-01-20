from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from sys import path

ad_may="A:/Travail/X/PSC/python"
ad_taha="C:/Users/hp 650 G3/Documents/GitHub/PSC"

#ad=ad_may
ad=ad_taha

path.append(ad)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pyautogui
from time import sleep

from t_ClWeb import t_ClWeb

xPath_T1T2 = "/html/body/table/tbody/tr[3]/td[3]/table/tbody/tr[11]/td/table/tbody/tr/td/div"   # bon X Path
xPath_beg = "/html/body/table/tbody/tr[3]/td[2]/div[1]/form/table[2]/tbody/tr[1]/td[2]/input"   # bon X Path
xPath_end = "/html/body/table/tbody/tr[3]/td[2]/div[1]/form/table[3]/tbody/tr[1]/td[2]/input"   # bon X Path
xPath_OK = "/html/body/table/tbody/tr[3]/td[2]/div[1]/form/table[6]/tbody/tr/td[1]/font/input"  # bon X Path

def pic(driver, beg, end):

    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, xPath_T1T2))).click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xPath_beg))).clear()
    driver.find_element_by_xpath(xPath_beg).send_keys(beg)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xPath_end))).clear()
    driver.find_element_by_xpath(xPath_end).send_keys(end)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPath_OK))).click()

    sleep(2)
    screen = pyautogui.screenshot()
    screen.save("C:/Users/hp 650 G3/Documents/GitHub/PSC/data/Pics0"+ beg + "__" + end + ".png")


def hotPics():

    try:

        driver = webdriver.Chrome("C:\\Program Files (x86)\\chromedriver.exe")
        driver.get("http://clweb.irap.omp.eu/cl/clweb.php")
        input("")
        sleep(5)
        times = []
        with open("C:/Users/hp 650 G3/Documents/GitHub/PSC/resMayTa.txt") as f:
            times = f.readlines()
        times_beg = [t_ClWeb(elt) for elt in times]
        times_end = [t_ClWeb(elt) for elt in times]
        for i in range(len(times_beg)):
            times_beg[i].ajouter(-120)
            times_end[i].ajouter(120) # on prend des images qui s'étalent sur 4 min
            print(times[i], times_beg[i], times_end[i], "\n")
            pic(driver, str(times_beg[i]), str(times_end[i]))

    except NoSuchElementException:
        print("Il y a un élément qui manque")

