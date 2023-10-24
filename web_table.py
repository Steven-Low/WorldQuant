#Imports Packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
#Opens up web driver and goes to Google Images
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# chop = webdriver.ChromeOptions()
# chop.add_extension('D:/Desktop/1.0.8_0.crx')

s=Service('C:/Users/2002l/Desktop/chromedriver.exe')
# create new Chrome driver object with Chrome extension
driver = webdriver.Chrome(service=s)  # options=chop


# driver.get('https://platform.worldquantbrain.com/data/data-sets/fundamental6?delay=1&instrumentType=EQUITY&limit=20&offset=0&order=-userCount&region=USA&universe=TOP3000')
# driver.get('https://platform.worldquantbrain.com/data/data-sets/pv1?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&universe=TOP3000')
# driver.get('https://platform.worldquantbrain.com/data/data-sets/fundamental12?delay=1&instrumentType=EQUITY&limit=20&offset=0&order=-userCount&region=USA&universe=TOP3000')
# driver.get('https://platform.worldquantbrain.com/data/data-sets/news12?delay=1&instrumentType=EQUITY&limit=20&offset=0&region=USA&type=MATRIX&universe=TOP3000')
driver.get('https://platform.worldquantbrain.com/data/data-sets/fundamental6?delay=1&instrumentType=EQUITY&limit=20&offset=0&order=-userCount&region=USA&type=MATRIX&universe=TOP3000')

while(True):
    try:
        name = driver.find_element(By.XPATH, '//*[@id="email"]')
        name.send_keys("eng2109645@xmu.edu.my")
        break
    except:
        time.sleep(1)

# name.send_keys(Keys.ENTER)
password = driver.find_element(By.XPATH,'//*[@id="password"]')
password.send_keys("ENGxmum23")
password.send_keys(Keys.ENTER)

cookie = driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div/div/div/div[2]/button[2]')
cookie.click()


# book.write("Fundamental Data\n\n")

for j in range(4):
    for i in range(1,21):
        while(True):
            try:
                content1 = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/div/div/div[2]/div[3]/div/div/div[1]/div[3]/div['+str(i)+']/div/div[1]/div/div').text
                with open("model_data.txt", "a+", encoding="utf-8") as book:
                    book.write(content1)
                    book.write("\n")
                break
            except:
                time.sleep(1)
                print("sleeping")
        # content2 = driver.find_element(By.XPATH, '//*[@id="root"]/div/section/div/div/div[2]/div[3]/div/div/div[1]/div[3]/div['+str(i)+']/div/div[2]/div').text
        # book.write(": "+content2)                

    nextPage = driver.find_element(By.CSS_SELECTOR,"[data-testid='pagination-next-button']")
    nextPage.click()
    print("next page")
    time.sleep(1)




input()