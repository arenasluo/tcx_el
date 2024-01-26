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



# def check_for_error_message(driver, error_message):
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/fieldset/ul/li"))
#     )
#     elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/fieldset/ul/li")
#     for element in elements:
#         if error_message in element.text:
#             return True
#     return False

# def check_for_error_message1(driver, error_message):
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[3]/form/div/div/div[1]/div/div[2]/div/h3"))
#     )
#     elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div[3]/form/div/div/div[1]/div/div[2]/div/h3")
#     for element in elements:
#         if error_message in element.text:
#             return True
#     return False

def check_for_error_message(driver, error_message):
    # Check the first XPath
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/fieldset/ul/li"))
        )
        elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/fieldset/ul/li")
        for element in elements:
            if error_message in element.text:
                return True
    except TimeoutException:
        pass  # If the elements are not found, continue to check the next XPath

    # Check the second XPath
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[3]/form/div/div/div[1]/div/div[2]/div/h3"))
        )
        elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div[3]/form/div/div/div[1]/div/div[2]/div/h3")
        for element in elements:
            if error_message in element.text:
                return True
    except TimeoutException:
        pass  # If the elements are not found, return False

    return False




def read_initial_rows(file_path, num_rows):
    with open(file_path, 'r') as file:
        phone_numbers_row = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][num_rows:]

        # phone number
        process_phone_number = lambda phone: phone.split(' ')[0]
        phone_numbers = [process_phone_number(phone) for phone in phone_numbers_row]

        # zip code 
        process_zip_code = lambda phone: phone.split(' ')[1]
        zip_codes = [process_zip_code(zip_code) for zip_code in phone_numbers_row]
    


    # Initialize WebDriver
    options = webdriver.ChromeOptions()
    options.headless = True
    # options.add_argument('--incognito')  # Add this line for incognito mode
    driver = webdriver.Chrome(options=options)



    driver.get("https://www1.cellcom.com/quikPay.html")

    results = []
    i = 0
    try:
        for phone_number, zip_code in zip(phone_numbers, zip_codes):
            i+=1


            # Wait for the first phone number input field
            primary_phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mobileNumber"))
            )
            primary_phone_input.clear()
            primary_phone_input.send_keys(phone_number)


            # Wait a moment for possible error messages
            time.sleep(2)


            primary_zip_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "zipcode"))
            )
            primary_zip_input.clear()
            primary_zip_input.send_keys(zip_code)            

            # Click continue
            refill_account_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div/fieldset/form/div[4]/div/input[2]"))
            )
            refill_account_element.click()      



            # Wait for possible error messages 
            time.sleep(1)

            # Check for all possible error messages
            if check_for_error_message(driver, "These credentials do not match our records."):
                error_code = 0
                error_message = "Not Cellcom"
                print(i, phone_number, error_code, error_message)

            elif check_for_error_message(driver, "Payment Amount"):
                error_code = 1  # No error found
                error_message = "Yes, prepaid"
                print(i, phone_number, error_code, error_message)
                driver.quit()
                options = webdriver.ChromeOptions()
                options.headless = True
                # options.add_argument('--incognito')  # Add this line for incognito mode
                driver = webdriver.Chrome(options=options)          
                driver.get("https://www1.cellcom.com/quikPay.html")   
            else:
                error_code = 1  # No error found
                error_message = "Yes, prepaid"
                print(i, phone_number, error_code, error_message)


            results.append((phone_number, error_code, error_message))
            with open('Cellcom_query_result.csv', mode='a', newline='') as file:
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


def count_rows_in_file(file_path):
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)

# count how many rows are in the file
file_path = 'cellcom.txt'
total_row_count = count_rows_in_file(file_path)

def main():
    start_row = 0
    total_processed = 0

    while True:

        processed = read_initial_rows('Cellcom_missing_numbers1.txt', start_row + total_processed)
        total_processed += processed
        if total_processed >= total_row_count:
            break  # Exit the loop and end the program

if __name__ == "__main__":
    main()
