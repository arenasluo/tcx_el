#!/usr/bin/env python
# coding: utf-8

# In[14]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
import random
import csv


def check_for_error_message(driver, error_message):
    # WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/form/div[1]/div[2]")))
    # elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[2]/div/form/div[1]/div[2]")
    # for element in elements:
    #     if error_message in element.text:
    #         return True



    # Check the second XPath
    
    try:
        element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/form/div[1]/div[2]"))
        )
        # Check if the element's text matches the error_message
        return element.text == error_message
    
    except TimeoutException:
        pass  # If the elements are not found, return False    

    try:
        element = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[3]/div/form/div[1]/p/span/text()"))
        )
        # Check if the element's text matches the error_message
        return element.text == error_message
    
    except TimeoutException:
        pass  # If the elements are not found, return False  



    return False

def read_initial_rows(file_path, num_rows):
    with open(file_path, 'r') as file:
        phone_numbers = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][num_rows:]
    phone_numbers[0]
    

    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    options.headless = True
    # options.add_argument('--incognito')  # Add this line for incognito mode
    driver = webdriver.Chrome(options=options)



    driver.get("https://id.boostmobile.com/")
    # WebDriverWait(driver, 5).until(
    #     EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    # ).click()
    results = []
    i = 0
    try:
        for phone_number in phone_numbers:
            i+=1


            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "user-text-field"))
            )
            primary_phone_input.clear()
            primary_phone_input.send_keys(phone_number)
            # for digit in phone_number:
            #     primary_phone_input.send_keys(digit)
            #     time.sleep(random.uniform(0.1, 0.3))


# <input id="user-text-field" placeholder="" class="BoostPassComp_prim-input__RFt64" name="email" type="email" size="35" autocomplete="username" data-gtm-form-interact-field-id="0">

# <input _ngcontent-prl-c10="" autocomplete="off" class="form-control ng-pristine ng-valid validation-error ng-touched" tmoallowedinput="" tmoautofocus="" tmosetfocus="" type="text" id="tmo-input-default-17" placeholder="Enter T-Mobile® phone number" tabindex="0" aria-label="Enter T-Mobile® phone number" aria-labelledby="" minlength="14" maxlength="14" pattern="\d">

            # Wait a moment for possible error messages
            time.sleep(random.uniform(0.3, 0.5))


            # Click an empty space 
            refill_account_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/form/button"))
            )
            refill_account_element.click()      



            # Wait for possible error messages 
            time.sleep(2)

            # time.sleep(random.uniform(0.3, 0.5))

            # Check for all possible error messages
            if check_for_error_message(driver, "Oops something is wrong. Please try again later."):
                error_code = 0
                error_message = "Not Boost"
                print(i, phone_number, error_code, error_message)
            if check_for_error_message(driver, "A message with your one time passcode was just sent to"):
                error_code = 1
                error_message = "Boost prepaid"
                print(i, phone_number, error_code, error_message)                
            else:
                error_code = 2  # No error found
                error_message = "Not sure"
                print(i, phone_number, error_code, error_message)


            results.append((phone_number, error_code, error_message))
            with open('Boost_query_result.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(results[-1])  # Write the last result
            # Refresh the page to reset state for next input
            time.sleep(random.uniform(0.3, 1))
            driver.refresh()

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.refresh()


    finally:
        driver.quit()
        return i


def main():
    start_row = 2116
    total_processed = 0

    while True:
        processed = read_initial_rows('Boost_numbers1.txt', start_row + total_processed)
        total_processed += processed


if __name__ == "__main__":
    main()
