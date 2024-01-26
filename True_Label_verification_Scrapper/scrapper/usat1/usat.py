#!/usr/bin/env python
# coding: utf-8

# In[14]:


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import random
import csv


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import datetime as dt


def check_for_error_message(driver):
    try:
        # Wait for the element to be present using the correct XPath
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div/div[1]"))
        )
        return True  # Element found

    except TimeoutException:
        return False  # Element not found within the time limit




def read_initial_rows(file_path, num_rows):
    with open(file_path, 'r') as file:
        phone_numbers_row = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][num_rows:]

        # phone number
        process_phone_number = lambda phone: phone.split('\t')[0]
        phone_numbers = [process_phone_number(phone) for phone in phone_numbers_row]

        # zip code 
        process_zip_code = lambda phone: phone.split('\t')[1]
        zip_codes = [process_zip_code(zip_code) for zip_code in phone_numbers_row]
    


    # Initialize WebDriver

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--incognito')  # Add this line for incognito mode
    # options.add_argument("--window-size=1,1")
    # options.add_argument("--window-position=0,0")
    driver = webdriver.Chrome(options=options)



    driver.get("https://www.att.com/acctsvcs/fastpay")

    # Click wireless
    refill_account_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div"))
    )
    refill_account_element.click()   

    results = []
    i = 0
    try:
        for phone_number, zip_code in zip(phone_numbers, zip_codes):
            i+=1


            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "accountNumber"))
            )
            primary_phone_input.clear()
            primary_phone_input.send_keys(phone_number)



            # Wait a moment for possible error messages
            time.sleep(2)


            primary_zip_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "zipCode"))
            )

            primary_zip_input.clear()
            primary_zip_input.send_keys(zip_code)      

            time.sleep(2)

            # Click continue
            refill_account_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[2]/div/div/div[2]/button"))
            )
            driver.execute_script("arguments[0].click();", refill_account_element)  



            # Wait for possible error messages 
            time.sleep(1)

            # Check for all possible error messages
            if check_for_error_message(driver):
                error_code = 0
                error_message = "Not usat post paid"
                print(i, phone_number, zip_code, error_code, error_message)
                
            else:
                error_code = 1  # No error found
                error_message = "Yes, prepaid"
                print(i, phone_number, zip_code, error_code, error_message)


            results.append((phone_number, error_code, error_message))
            with open('usat_query_result.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(results[-1])  # Write the last result
            # Refresh the page to reset state for next input
            time.sleep(2)
            driver.refresh()
            refill_account_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[3]/div[2]/div[2]/div"))
            )
            refill_account_element.click()               

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.refresh()


    finally:
        driver.quit()
        return i


def count_rows_in_file(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)

# count how many rows are in the file
file_path = 'usat.txt'
total_row_count = count_rows_in_file(file_path)

def main():
    start_row = 0
    total_processed = 0

    while True:

        processed = read_initial_rows('usat.txt', start_row + total_processed)
        total_processed += processed
        if total_processed >= total_row_count:
            break  # Exit the loop and end the program

if __name__ == "__main__":
    main()
