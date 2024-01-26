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

def get_row_count(file_path):
    """
    Counts the number of rows in the specified file.

    :param file_path: Path to the file.
    :return: Number of rows in the file.
    """
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)

def check_for_error_message(driver, error_message):
    elements = driver.find_elements(By.TAG_NAME, 'p') + driver.find_elements(By.TAG_NAME, 'li')
    for element in elements:
        if error_message in element.text:
            return True
    return False

def check_for_error_message1(driver, error_message):
    elements = driver.find_elements(By.XPATH, "/html/body/tmo-root/main/div/tmo-directto-account/section/div[1]/div[2]/p")
    for element in elements:
        if error_message in element.text:
            return True
    return False

def read_initial_rows(file_path, num_rows):
    with open(file_path, 'r') as file:
        phone_numbers = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][num_rows:]
    phone_numbers[0]
    

    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--incognito')  # Add this line for incognito mode
    driver = webdriver.Chrome(options=options)



    driver.get("https://prepaid.t-mobile.com/direct-to-account?icid=MGPR_TMO_C_CUSTSUPT_PE7I1K07DR3HZU5OA19473")
    # WebDriverWait(driver, 5).until(
    #     EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    # ).click()
    results = []
    i = 0
    try:
        for phone_number in phone_numbers:
            i+=1

            # if i % 600 == 0:
            #     print(f"Pausing for 10 minutes after processing {i} phone numbers.")
            #     driver.quit()
            #     time.sleep(600)  # Sleep for 600 seconds (10 minutes)
            #     driver = webdriver.Chrome(options=options)
            #     driver.get("https://prepaid.t-mobile.com/direct-to-account?icid=MGPR_TMO_C_CUSTSUPT_PE7I1K07DR3HZU5OA19473")

            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tmo-input-default-17"))
            )
            primary_phone_input.clear()
            for digit in phone_number:
                primary_phone_input.send_keys(digit)
                time.sleep(random.uniform(0.1, 0.3))

            # Wait a moment for possible error messages
            time.sleep(random.uniform(0.3, 0.5))

            # Check for the confirmation checkmark
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "i.fa.fa-check.def.active.m-r-sm"))
            )

            # Enter the phone number again 
            confirm_phone_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "tmo-input-default-18"))
            )
            confirm_phone_input.clear()
            for digit in phone_number:
                confirm_phone_input.send_keys(digit)
                time.sleep(random.uniform(0.3, 0.5))  # Small delay between each character

            # Click an empty space 
            refill_account_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//h2[contains(@class,'ng-star-inserted') and contains(text(), 'Refill this account')]"))
            )
            refill_account_element.click()      

            # Wait for possible error messages 
            time.sleep(random.uniform(0.3, 0.5))

            # Check for all possible error messages
            if check_for_error_message(driver, "Refills and Payments are not allowed on the Tourist rate plan"):
                error_code = 3
                error_message = "Refills and Payments are not allowed on the Tourist rate plan"
                print(i, phone_number, error_code, error_message)
            elif check_for_error_message(driver, "Oops! Refills and Payments are not allowed on the Tourist rate plan. Please visit a T-Mobile Retail Store for further details"):
                error_code = 3
                error_message = "Oops! Refills and Payments are not allowed on the Tourist rate plan. Please visit a T-Mobile Retail Store for further details"
                print(i, phone_number, error_code, error_message)
            elif check_for_error_message(driver, "Mobile number is invalid. Please try again."):
                error_code = 2
                error_message = "Mobile number is invalid. Please try again."
                print(i, phone_number, error_code, error_message)
            elif check_for_error_message(driver, "Mobile number is invalid."):
                error_code = 1
                error_message = "Mobile number is invalid."
                print(i, phone_number, error_code, error_message)
            elif check_for_error_message(driver, "To Refill your account using a Voucher please dial 611 from your handset or register for an online account with T-Mobile."):
                error_code = 0  # No error found
                error_message = "No error found, prepaid"
                print(i, phone_number, error_code, error_message)
            else:
                if check_for_error_message1(driver, "Oops! Refills and Payments are not allowed on the Tourist rate plan. Please visit a T-Mobile Retail Store for further details"):
                    error_code = 3
                    error_message = "Tourist plan"
                    print(i, phone_number, error_code, error_message)
                else:
                    error_code = 0  # No error found
                    error_message = "No error found, prepaid"
                    print(i, phone_number, error_code, error_message)


            results.append((phone_number, error_code, error_message))
            with open('ustm_query_result.csv', mode='a', newline='') as file:
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
    start_row = 0
    total_processed = 0

# Usage
    file_path = 'test_panel_porting_ustm1.txt'
    row_count = get_row_count(file_path)
    print(f"The file {file_path} has {row_count} rows.")

    while True:
        processed = read_initial_rows('test_panel_porting_ustm1.txt', start_row + total_processed) 
        total_processed += processed  
        if start_row + total_processed >= row_count:  # Break the loop if no more rows are processed
            break


if __name__ == "__main__":
    main()
