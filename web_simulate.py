#Imports Packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pynput.keyboard import Controller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from IPython.display import display
import pandas as pd



# Start Selenium Browser Service
s=Service('C:/Users/2002l/Desktop/chromedriver.exe')
driver = webdriver.Chrome(service=s) 
driver.get('https://platform.worldquantbrain.com/simulate')

# Login the account 
while(True):
    try:
        name = driver.find_element(By.XPATH, '//*[@id="email"]')
        name.send_keys("eng2109645@xmu.edu.my")
        break
    except:
        time.sleep(1)
password = driver.find_element(By.XPATH,'//*[@id="password"]')
password.send_keys("ENGxmum23")
password.send_keys(Keys.ENTER)

# Accept the cookies & Skip tips
cookie = driver.find_element(By.XPATH,'//*[@id="root"]/div[2]/div/div/div/div[2]/button[2]')
cookie.click()
while(True):
    try:
        skip = driver.find_element(By.XPATH,'/html/body/div[6]/div/div[5]/a[1]')
        skip.click()
        break
    except:
        time.sleep(1)

 

# Creating a DataFrame for all Alpha output
data = {'SIMULATOR' : [],
        'PASS' : [],
        'FAIL' : [],
        'PENDING' : [],
        'SHARPE' : [],
        'TURNOVER' : [],
        'FITNESS' : [],
        'RETURNS' : []}

# Calculate the number of alphas in the model file
with open("model_data.txt","r") as size:
    total_length = len(size.readlines())


# ===================================================================================================+
# FUNCTIONS AND MODULES
# ===================================================================================================+

# Use Xpath to locate the "+" simulation button & Click
def click_add_simulation():
    try:
        add = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[2]/div/div/span')
    except:
        add = driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[4]/div/div')
    add.click()
    time.sleep(0.5) # To wait for the animation of new simulation creation

# Double click the text lines interface and type alphas on it
def insert_alpha(line):
    insert = driver.find_element(By.CLASS_NAME,'view-line')
    insert.click()
    insert.click()
    keyboard = Controller()
    keyboard.type(line.strip()) 

# Click the settings of current Simulator
def click_settings():
    # setting = driver.find_element(By.CSS_SELECTOR, '.ui.button.editor-top-bar-left__settings-btn')
    # settings = driver.find_element(By.CLASS_NAME,'intro-step-2')
    settings = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'ui button editor-top-bar-left__settings-btn')]"))
            )
    has_background_image = driver.execute_script(
        'return window.getComputedStyle(arguments[0], "::before").getPropertyValue("background-image") !== "none";',
        settings[1])
    if (has_background_image):
        settings[1].click()

# Change the decay value [should be applied after click_settings()]
def change_decay(n:int):
    try:
        decay = driver.find_element(By.NAME,'decay')
        decay.clear()
        decay.send_keys(n)
    except:
        pass

# Apply the settings [should be applied after click_settings()]
def click_apply():
    try:
        apply = driver.find_element(By.CLASS_NAME, 'button--lg')
        apply.click()
    except:
        pass


# Use Class Name To Locate The Simulate Button & Click 
def click_simulate():
    simulate = driver.find_element(By.CLASS_NAME, 'intro-step-5')  
    simulate.click()
    time.sleep(0.2) 

# Select the Simulator i based on FIFO principle 
def click_simulator(i):
    try:
        simulator = driver.find_element(By.XPATH,"//div[contains(@class, 'editor-tabs__tab-text') and text()='Simulation "+str(i)+"']")
    except:
        try:
            simulator = driver.find_element(By.XPATH,"//div[contains(@class, 'editor-tabs__tab-text tab-text-overflowed') and text()='Simulation "+str(i)+"']")
        except:
            simulator = driver.find_element(By.XPATH,"//div[contains(@class, 'editor-tabs__tab-text-id') and text()=' "+str(i)+"']")
    simulator.click()

# Scanning & extract the IS test and Summary of the completed alpha
def get_output_data():
    iter = 0
    while(True):
        try:
            # The raw "test" data will contain number of pass, fail and pending information
            test = driver.find_element(By.CLASS_NAME,'sumary__testing-checks').text
            # The summary will contains information regarding Sharpe, Turnover, Fitness, Returns ... (We pick 4 for the result)
            summary = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'summary-metrics-info summary-metrics-info--data')]"))
            )
            break
        except:
            time.sleep(3)
            print("loading...")
            iter += 1
            # Delete the simulation if over 1 minute
            if iter >= 20:   
                driver.find_element(By.CLASS_NAME,'editor-tabs__tab-cross').click()
                driver.find_element(By.CLASS_NAME, 'button--primary').click()
                test = ""
                summary = None
                break
    return test,summary


# Update and store the output of completed alphas
def update_data(test,summary,i):
    
    # Process the raw "test" data and move to result dictionary 
    result = dict()
    for line in test.splitlines():
        if len(line) > 0:
            arr = line.split(' ')
            result[arr[-1]] = arr[0] # "7 PASS" to "PASS 7"

    # Process the summary data and move to result dictionary
    if summary != None:
        result['SHARPE'] = summary[0].text
        result['TURNOVER'] = summary[1].text
        result['FITNESS'] = summary[2].text
        result['RETURNS'] = summary[3].text

    # Update the result to the "data" dictionary
    for key in data.keys():
        if key == 'SIMULATOR':
            data[key].append("Simulation "+str(i))
            continue
        if key in result:
            data[key].append(result[key])
        else:
            data[key].append(0)

    # Displaying the DataFrame (optional) & backup the Output data
    df = pd.DataFrame(data)
    # display(df)
    with open("backup.txt","w+") as backup:
        backup.write(df.to_string())

def main():
    print("start...")
    current_alpha = 0 # position index
    with open("model_data.txt", "r", encoding="utf-8") as book:
        for alpha in book:
            current_alpha += 1

            click_add_simulation()
            insert_alpha(alpha)
            click_settings()
            change_decay(6)  
            click_apply()
            click_simulate()

            # When total simulations reach 3; Wait and scan for the results
            if current_alpha % 3 == 0 or current_alpha == total_length:
                for i in range(current_alpha,3+current_alpha):
                    click_simulator(i)
                    test,summary = get_output_data()
                    update_data(test,summary,i)        


if __name__ == "__main__":
    main()
