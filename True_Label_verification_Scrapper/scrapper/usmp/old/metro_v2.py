#!/usr/bin/env python
# coding: utf-8

# In[14]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import random
import csv

URL = "https://www.metrobyt-mobile.com/guestpay/landing"

def check_for_error_message(driver, error_message):
    # # Check the first XPath
    # try:
    #     WebDriverWait(driver, 10).until(
    #                 EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/tmo-root/div[2]/div/tmo-express-pay-wrapper/tmo-theme/div/ng-component/div/tmo-view-component/div/tmo-core-container-element/div/div[2]/div/div[2]/metro-express-pay-landing-element/div/form/div[1]/div/div/mat-error/")))
    #     elements = driver.find_elements(By.XPATH, "/html/body/div[1]/tmo-root/div[2]/div/tmo-express-pay-wrapper/tmo-theme/div/ng-component/div/tmo-view-component/div/tmo-core-container-element/div/div[2]/div/div[2]/metro-express-pay-landing-element/div/form/div[1]/div/div/mat-error/")
    #     for element in elements:
    #         if error_message in element.text:
    #             return True
    # except TimeoutException:
    #     pass  # If the elements are not found, continue to check the next XPath



    # Check the first XPath
    try:
        WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/tmo-root/div[2]/div/tmo-express-pay-wrapper/tmo-theme/div/ng-component/div/tmo-view-component/div/tmo-core-container-element/div/div[2]/div/div/metro-express-bill-pay-element/div/div/h3")))
        elements = driver.find_elements(By.XPATH, "/html/body/div[1]/tmo-root/div[2]/div/tmo-express-pay-wrapper/tmo-theme/div/ng-component/div/tmo-view-component/div/tmo-core-container-element/div/div[2]/div/div/metro-express-bill-pay-element/div/div/h3")
        for element in elements:
            if error_message in element.text:
                return True
    except TimeoutException:
        pass  # If the elements are not found, continue to check the next XPath

    return False




def read_initial_rows(file_path, num_rows):
    with open(file_path, 'r') as file:
        phone_numbers = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][num_rows:]
    
    # # Initialize WebDriver
    # options = webdriver.ChromeOptions()
    # options.headless = True
    # # options.add_argument('--incognito')  # Add this line for incognito mode
    # driver = webdriver.Chrome(options=options)

    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\ericluo\AppData\Local\Google\Chrome\User Data')
    options.add_argument("--profile-directory=Default")
    driver = webdriver.Chrome(options=options)


    driver.get(URL)
    time.sleep(2)
    results = []
    i = 0
    try:
        for phone_number in phone_numbers:
            i+=1

            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "phonenum-input"))
            )
            primary_phone_input.clear()
            primary_phone_input.send_keys(phone_number)


            # Continue
            refill_account_element = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "confirm-input"))
            )
            refill_account_element.click()    


            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "confirm-input"))
                #EC.presence_of_element_located((By.ID, "/html/body/div[1]/tmo-root/div[2]/div/tmo-express-pay-wrapper/tmo-theme/div/ng-component/div/tmo-view-component/div/tmo-core-container-element/div/div[2]/div/div[2]/metro-express-pay-landing-element/div/form/div[1]/div/mat-form-field[2]/div/div[1]/div[3]/input"))
            )
            primary_phone_input.clear()
            primary_phone_input.send_keys(phone_number)

            # # Click recaptcha checkbox
            # refill_account_element = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "/html/body/section/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div[1]/form/div[6]/div"))
            # )
            # refill_account_element.click()    

            time.sleep(5)

            # Continue
            refill_account_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/tmo-root/div[2]/div/tmo-express-pay-wrapper/tmo-theme/div/ng-component/div/tmo-view-component/div/tmo-core-container-element/div/div[2]/div/div[2]/metro-express-pay-landing-element/div/form/div[3]/div/button"))
            )
            refill_account_element.click()      



            # Wait for possible error messages 
            time.sleep(2)

            # time.sleep(random.uniform(0.3, 0.5))


            # Check for all possible error messages
            # if check_for_error_message(driver, "Sorry, the phone number does not match our records. Please try again with a correct Metro by T-Mobile phone number"):
            #     error_code = 0
            #     error_message = "Not Metro"
            #     print(i, phone_number, error_code, error_message)
            #     driver.get(URL)
            if check_for_error_message(driver, "Pay as a guest"):
                error_code = 1
                error_message = "Metro prepaid"
                print(i, phone_number, error_code, error_message)
                driver.get(URL)                
            else:
                error_code = 2  # No error found
                error_message = "Not prepaid"
                print(i, phone_number, error_code, error_message)
                driver.get(URL)


            results.append((phone_number, error_code, error_message))
            with open('metro_query_result.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(results[-1])  # Write the last result
            # Refresh the page to reset state for next input
            time.sleep(random.uniform(0.3, 1))
            

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.get(URL)


    finally:
        driver.quit()
        return i


def main():
    start_row = 91
    total_processed = 0

    while True:
        processed = read_initial_rows('TangoMetroNumbers_subset.txt', start_row + total_processed)
        total_processed += processed


if __name__ == "__main__":
    main()
