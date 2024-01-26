#!/usr/bin/env python
# coding: utf-8

# In[14]:
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
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
    time.sleep(5)
    try:
        element =  WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/form/prism-text[2]")))
        # Check if the element's text matches the error_message
        return element.text == error_message
    
    except TimeoutException:
        pass  # If the elements are not found, return False    

def safe_click(driver, xpath):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
    except StaleElementReferenceException:
        # If the element is stale, re-locate it and then click
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()

def check_for_error_message1(driver, error_message):
    time.sleep(5)
    try:
        element =      WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/form/prism-text[2]")))
        # Check if the element's text matches the error_message
        return element.text == error_message
    
    except TimeoutException:
        pass  # If the elements are not found, return False    



def read_initial_rows(file_path, num_rows):
    with open(file_path, 'r') as file:
        next(file)  # Skip the header
        phone_numbers = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][num_rows:]

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--incognito')  # Add this line for incognito mode
    driver = webdriver.Chrome(options=options)

    #url = 'https://login.xfinity.com/login?c_ds_na=c_ds_na%2Cc_ds_no%2Cc_ds_ts%2Cclient_id%2Ccontinue%2Cr%2CreqId%2Cs&c_ds_no=D278FFE36C90FB72A884FEA793AFC78D&c_ds_ts=1700757551&c_ds_val=ACD387F70C8E5B64C79FD2DC27EF2F02C92DCD8C53C2113DF1A35CF0DBEA9A25&client_id=xm-d2c-web&continue=https%3A%2F%2Foauth.xfinity.com%2F%2Foauth%2Fauthorize%3Fclient_id%3Dxm-d2c-web%26redirect_uri%3Dhttps%253A%252F%252Fwww.xfinity.com%252Fmobile%252Fmy-account%252Flogin%26response_type%3Dcode%26response%3D1%26reqId%3D999a2ca1-4218-46d7-9e35-85b174630fb0&r=comcast.net&reqId=d2a4043d-e312-42e1-a907-5e3f6c9e6365&s=oauth'
    url = 'https://login.xfinity.com/login'

    driver.get(url)
    time.sleep(2)
    press_button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/a[2]'))
    )
    press_button.click()

    output = []
    i = 0
    try:
        for number in phone_numbers:
            i+=1
            print(number, i )

            # Wait for the first phone number input field
            number_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="user"]'))
            )
            number_input.clear()
            number_input.send_keys(number)

            time.sleep(2)
            # press_button = WebDriverWait(driver, 1).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="sign_in"]'))
            # )
            safe_click(driver, '//*[@id="sign_in"]')


            if check_for_error_message(driver, "Enter your password"): 
                output.append((number, 1))
                print('Yes, prepaid (maybe)')

            elif check_for_error_message1(driver, "The Xfinity ID or password you entered was incorrect. Please try again."):
                output.append((number, 0))
                print('Not prepaid')

            else:
                output.append((number, 0))
                print('Not prepaid')

            with open(r'usxf_check.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(output[-1])  


            # Refresh the page to reset state for next input
            time.sleep(1)
            driver.get(url)

    except Exception as e:
        print(f"An error occurred: {e}")
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument('--incognito')  # Add this line for incognito mode
        driver = webdriver.Chrome(options=options)        
        driver.get(url)
        i-=1


    finally:
        driver.quit()
        return i


def main():
    start_row = 0
    total_processed = 0
    file_path = r"C:\Users\ericluo\Desktop\test\usxf_test.txt"
    while True:
        processed = read_initial_rows(file_path, start_row + total_processed)
        total_processed += processed


if __name__ == "__main__":
    main()
