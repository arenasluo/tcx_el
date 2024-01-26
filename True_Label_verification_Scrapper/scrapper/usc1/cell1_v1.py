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

URL = "https://selfcare.mycellularone.com/#/quickTopUp"

def check_for_error_message(driver, error_message):
    # Check the first XPath
    try:
        WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/p")))
        elements = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[2]/div/div/div/p")
        for element in elements:
            if error_message in element.text:
                return True
    except TimeoutException:
        pass  # If the elements are not found, continue to check the next XPath

    # Check the second XPath
    try:
        WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div[1]/app-accept-payment/div/div[1]/div/order-summary-component/div[1]/div/label")))
        elements = driver.find_elements(By.XPATH, "/html/body/div/div[2]/div[1]/app-accept-payment/div/div[1]/div/order-summary-component/div[1]/div/label")
        for element in elements:
            if error_message in element.text:
                return True
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



    driver.get(URL)

    results = []
    i = 0
    try:
        for phone_number in phone_numbers:
            i+=1

            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "balance_topup_linenumber"))
            )
            primary_phone_input.clear()
            primary_phone_input.send_keys(phone_number)



            # Select the second option from the dropdown
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/section/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[1]/div/div[4]/select"))
            )
            Select(dropdown).select_by_index(1)  # Index starts from 0, so 1 is the second option



            # Wait a moment for possible error messages
            time.sleep(0.5)


            # Click an empty space 
            refill_account_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div/section/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/button"))
            )
            refill_account_element.click()      



            # Wait for possible error messages 
            time.sleep(0.5)

            # time.sleep(random.uniform(0.3, 0.5))

            # Check for all possible error messages
            if check_for_error_message(driver, "Please check the entered Phone Number"):
                error_code = 0
                error_message = "Not CellularOne"
                print(i, phone_number, error_code, error_message)
            elif check_for_error_message(driver, "Order Summary"):
                error_code = 1  # No error found
                error_message = "Yes, prepaid"
                print(i, phone_number, error_code, error_message)
                driver.quit()
                options = webdriver.ChromeOptions()
                options.headless = True
                # options.add_argument('--incognito')  # Add this line for incognito mode
                driver = webdriver.Chrome(options=options)          
                driver.get(URL)   
            else:
                error_code = 1  # No error found
                error_message = "Yes, prepaid"
                print(i, phone_number, error_code, error_message)



            results.append((phone_number, error_code, error_message))
            with open('CellularOne_query_result.csv', mode='a', newline='') as file:
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
    start_row = 19279
    total_processed = 0

    while True:
        processed = read_initial_rows('CellularOne_numbers.txt', start_row + total_processed)
        total_processed += processed


if __name__ == "__main__":
    main()
