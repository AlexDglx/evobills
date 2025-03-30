from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from tqdm import tqdm
import os
import random
import time
import json
download_directory = "/Users/adegallaix/Downloads/Bills/"
# Configure download directory
def main():
    
    user_agent = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Linux: X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Android: Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        # Add more User-Agent strings as needed
    ]
    # Set up WebDriver options to automatically download files to a specified location
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    rand_user_agent = random.choice(user_agent)
    service = Service()
    options = Options()
    #options.add_argument("--headless")
    #options.add_argument("--incognito")
    options.add_argument("--force-dark-mode")
    #options.add_argument(f'--load-extension={extension_file}')
    options.add_argument(f"--user-agent={rand_user_agent}")
    options.add_experimental_option("prefs", prefs)
    # Initialize the WebDriver
    driver = webdriver.Chrome(
        service=service,
        options=options
        )
    # Navigate to the login page
    driver.get("https://evo-fo.vulog.center/login")  # Replace with actual login page
    driver.maximize_window()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="Selenium-usernameOrEmail"]')))
    # Log in (replace with actual selectors and credentials)
    username = driver.find_element(By.XPATH, f'//*[@id="Selenium-usernameOrEmail"]')
    password = driver.find_element(By.XPATH, f'//*[@id="Selenium-passWord"]')
    
    auth_login = []
    with open("auth.json", 'r') as f :
        auth_login.append(json.load(f))
        
    username.send_keys(auth_login['authentification']['password'])      # Enter your username
    password.send_keys(auth_login['authentification']['password'])
    
    # Enter your password
    driver.find_element(By.ID, "Selenium-buttonSubmitLogin").click()
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'#Selenium-NavBarItem-Billing')))
    #driver.find_element(By.CSS_SELECTOR, f'#Selenium-NavBarItem-Billing').click()
    time.sleep(3)
    
    driver.get("https://evo-fo.vulog.center/billing")
    time.sleep(3)
    # Wait until the page is loaded after login
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "mui-component-select-year")))
    driver.find_element(By.ID, "mui-component-select-year").click()
    time.sleep(2)
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.MuiButtonBase-root:nth-child(11)')))
    element = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(11)")
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
                                                
    # Locate the combobox for selecting the month
    #combo_box_year = Select(driver.find_element(By.CSS_SELECTOR, f'#mui-component-select-year'))  # Adjust the ID to the actual combo box ID
    #combo_box_year.select_by_visible_text("2024")
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, f'mui-component-select-month')))
    driver.find_element(By.ID, f'mui-component-select-month').click()
    months = driver.find_elements(By.TAG_NAME,"li")
    months_result = []
    [months_result.append(x.text) for x in months ]
    time.sleep(2)
    for index, month in enumerate(months_result,1):
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, f'mui-component-select-month')))
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,f'//*[@id="menu-month"]/div[3]/ul/li[{3}]')))
        driver.find_element(By.XPATH,f'//*[@id="menu-month"]/div[3]/ul/li[{index}]').click()
        time.sleep(5)
        #[@id="menu-month"]/div[3]/ul/li[4]
        driver.find_element(By.ID, f'mui-component-select-month').click()
        print((index,month))
        if month != "": # if month dropdown is not empty
            #//*[@id="root"]/div[2]/div[2]/div/div/div[2]/div/div
            #//*[@id="root"]/div[2]/div[2]/div/div/div[2]
            try:
                bills_container = driver.find_element(By.CLASS_NAME, "infinite-scroll-component__outerdiv")
                # in bills container div
                print("element exists")
                # in div container get every button
                previous_item_count = 0
                driver.find_element(By.TAG_NAME, f'body').click()
                while True:
                    time.sleep(2)
                    bills = bills_container.find_elements(By.TAG_NAME, "button")
                    current_item_count = len(bills)
                    if current_item_count == previous_item_count:
                        break
                    previous_item_count=current_item_count
                    #scroll_element = driver.find_element(By.CSS_SELECTOR, ".infinite-scroll-component")
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    #driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", bills_container)
                    time.sleep(5)
                driver.execute_script("window.scrollTo(0, 0)")
                driver.find_element(By.ID, f'mui-component-select-month').click()
                print(f'Number of bills : {current_item_count}')
                time.sleep(3)

                print(bills)

                for index,bill in enumerate(bills):
                    #download bill 
                    #make directory
                    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, f'#Selenium-MyTripsTable-download-{index}'))
                    time.sleep(3)

                    driver.find_element(By.CSS_SELECTOR, f'#Selenium-MyTripsTable-download-{index} > .MuiButton-label').click()

                    time.sleep(3)
            except NoSuchElementException:
                print("element not found")
            
    driver.quit()

def wait_for_download_and_rename(download_path, expected_filename, new_filename):
    while True:
        files = os.listdir(download_path)
        if expected_filename in files:
            os.rename(
                os.path.join(download_path, expected_filename),
                os.path.join(download_path, new_filename)
            )
            break
        time.sleep(1)


    #//*[@id="mui-component-select-month"]

if __name__ == "__main__":
    main()

#
#
#    # Select the month in the combo box
#    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f'mui-component-select-month')))
#    #driver.find_element(By.XPATH, f'//*[@id="Selenium-BillingTrips-SelectMonth-Select"]').click()
#    #driver.find_element(By.ID, f'mui-component-select-month').click() 
#
#    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "li")))
#    # Wait for the invoices list to load
#
#    driver.find_element(By.ID, f'mui-component-select-month').click()
#  
#    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.MuiListItem-root:nth-child({x})'))) 
#    driver.find_element(By.CSS_SELECTOR, "body").click()
#    month=driver.find_element(By.CSS_SELECTOR,f'.MuiListItem-root:nth-child({x})')
#    actions = ActionChains(driver)
#    actions.move_to_element(month).click().perform()
#    time.sleep(4)
#   
#    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.MuiGrid-root'))) 
#
#    bill_page = driver.find_elements(By.CSS_SELECTOR, f'.MuiGrid-root')
#
#    if (len(bill_page)>0):
#        for bill in bill_page:
#            buttons_list = bill.find_elements(By.CLASS_NAME, 'MuiButtonBase-root')
#            time.sleep(1)
#            driver.find_element(By.CSS_SELECTOR, "body").click()
#            print("Downloading bills")
#            for button in tqdm(buttons_list, desc="Downloading bills..."):
#                time.sleep(4)
#                actions = ActionChains(driver)
#                actions.move_to_element(button).click().perform()
#
#                #button.click()
#                time.sleep(4)
#                scroll_element = driver.find_element(By.CLASS_NAME, ".MuiGrid-root")
#                scroll_origin = ScrollOrigin.from_element(scroll_element)
#                ActionChains(driver)\
#                    .scroll_from_origin(scroll_origin, 0, 200)\
#                    .perform()
#                actions = ActionChains(driver)
#                actions.move_to_element(button).click().perform()
#                #button.click()
#                time.sleep(2)  # Pause briefly to ensure the download starts
#    else:
#        print("No bills detected.")
#
#        # Optional: wait until downloads finish before proceeding to the next month
#    time.sleep(2)
#print("All bills downloaded.")

# Close the driver after all invoices are downloaded
