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

URL = "https://www.xfinity.com/mobile/my-account/quickpay/start"


def check_for_error_message(driver, error_message):
    # Check the second XPath
    
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-no-balance-due/section/xm-quickpay-shared-error/section/p"))
        )
        # Check if the element's text matches the error_message
        return element.text == error_message
    
    except TimeoutException:
        pass  # If the elements are not found, return False    

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-amount/section/xm-quickpay-shared-amount/section/xm-quickpay-summary/section/p[1]"))
        )
        # Check if the element's text matches the error_message
        return element.text == error_message
    
    except TimeoutException:
        pass  # If the elements are not found, return False    

    # Check the third XPath
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-no-account-found/section/xm-quickpay-shared-error/section/p"))
        )
        # Check if the element's text matches the error_message
        return element.text == error_message
            
    except TimeoutException:
        pass  # If the elements are not found, continue to check the next XPath

    # Check the fourth XPath
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-no-account-found/section/xm-quickpay-shared-error/section/p"))
        )
        # Check if the element's text matches the error_message
        return element.text == error_message
            
    except TimeoutException:
        pass  # If the elements are not found, continue to check the next XPath


    # Check the fifth XPath
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-multi-account-mdn/section/xm-quickpay-shared-error/section/p"))
        )
        # Check if the element's text matches the error_message
        return element.text == error_message

    except TimeoutException:
        pass  # If the elements are not found, return False

    return False


def read_initial_rows(file_path, start_row , total_processed):
    start_row , total_processed
    num_rows = start_row + total_processed

    with open(file_path, 'r') as file:
        phone_numbers_row = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][num_rows:]

        # phone number
        process_phone_number = lambda phone: phone.split()[0]
        phone_numbers = [process_phone_number(phone) for phone in phone_numbers_row]

        # zip code 
        process_zip_code = lambda phone: phone.split()[1]
        zip_codes = [process_zip_code(zip_code) for zip_code in phone_numbers_row]
    
    file_len = len(zip_codes)

    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    options.headless = True
    # options.add_argument('--incognito')  # Add this line for incognito mode
    driver = webdriver.Chrome(options=options)



    driver.get(URL)

    results = []
    i = 0
    try:
        for phone_number, zip_code in zip(phone_numbers, zip_codes):
            i+=1

            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-start/section/xm-quickpay-shared-start/section/form/fieldset/xm-validation[1]/section/input"))
            )
            primary_phone_input.clear()
            primary_phone_input.send_keys(phone_number)


            # Wait a moment for possible error messages
            time.sleep(1)


            primary_zip_input = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-start/section/xm-quickpay-shared-start/section/form/fieldset/xm-validation[2]/section/input"))
            )
            primary_zip_input.clear()
            primary_zip_input.send_keys(zip_code)            

            # Click continue
            refill_account_element = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/xm-app/ui-view/xm-base/div/ui-view/xm-quickpay-start/section/xm-quickpay-shared-start/section/div/button"))
            )
            refill_account_element.click()      



            # Wait for possible error messages 
            time.sleep(1)

            # Check for all possible error messages
            if check_for_error_message(driver, "This account has no balance due"):
                error_code = 1  # No error found
                error_message = "Yes, xfinity prepaid"
                print(i, phone_number, zip_code, error_code, error_message)
                driver.quit()
                options = webdriver.ChromeOptions()
                options.headless = True
                # options.add_argument('--incognito')  # Add this line for incognito mode
                driver = webdriver.Chrome(options=options)          
                driver.get(URL)   
            elif check_for_error_message(driver, "TOTAL AMOUNT DUE"):
                error_code = 1  # No error found
                error_message = "Yes, xfinity prepaid"
                print(i, phone_number, zip_code, error_code, error_message)
                driver.quit()
                options = webdriver.ChromeOptions()
                options.headless = True
                # options.add_argument('--incognito')  # Add this line for incognito mode
                driver = webdriver.Chrome(options=options)          
                driver.get(URL)   
            elif check_for_error_message(driver, "We can’t find an account associated with that number"):
                error_code = 0
                error_message = "phone number and zip code doesn't match xfinity records, not usxf postpaid customer"
                print(i, phone_number, zip_code, error_code, error_message)
                driver.get(URL)        
            elif check_for_error_message(driver, "We’re having trouble identifying this particular account"):
                error_code = 0
                error_message = "Cannot verify if this is a usxf postpaid customer"
                print(i, phone_number, zip_code, error_code, error_message)
                driver.get(URL)                           
            elif check_for_error_message(driver, "The information you entered doesn't match our records. Please try again."):
                error_code = 0  
                error_message = "phone number and zip code doesn't match xfinity records, not usxf postpaid customer"
                print(i, phone_number, zip_code, error_code, error_message)
                driver.quit()
                options = webdriver.ChromeOptions()
                options.headless = True
                # options.add_argument('--incognito')  # Add this line for incognito mode
                driver = webdriver.Chrome(options=options)          
                driver.get(URL)              
            else:
                error_code = 0  # No error found
                error_message = "not usxf postpaid customer"
                print(i, phone_number, zip_code, error_code, error_message)

            results.append((phone_number, error_code, error_message))
            with open('usxf_query_result.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(results[-1])  # Write the last result
            # Refresh the page to reset state for next input
            time.sleep(1)
            driver.refresh()
            if file_len == i:
                driver.quit()
                return i

    except Exception as e:
        print(f"An error occurred: {e}")
        i=i-1
        driver.quit()
        options = webdriver.ChromeOptions()
        options.headless = True
        # options.add_argument('--incognito')  # Add this line for incognito mode
        driver = webdriver.Chrome(options=options)          
        driver.get(URL)  


    finally:
        driver.quit()
        return i


def count_rows_in_file(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)


def main():
    # count how many rows are in the file
    file_path = 'usxf_numbers_zipcode.txt'
    total_row_count = count_rows_in_file(file_path)

    start_row = 3025
    total_processed = 0

    while True:

        processed = read_initial_rows(file_path, start_row , total_processed)
        total_processed += processed
        if processed >= total_row_count:
            break  # Exit the loop and end the program

if __name__ == "__main__":
    main()
