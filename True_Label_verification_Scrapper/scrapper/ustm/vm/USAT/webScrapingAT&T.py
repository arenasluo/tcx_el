from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import os

# Build scraper for AT&T phone numbers

def main(url, number):
    # Set up
    driver = webdriver.Firefox()
    driver.get(url)

    # Set the 'amount' input field
    amount = driver.find_element(By.ID, 'amount')
    amount.send_keys(10)

    # Find the phone number input field
    number_input = driver.find_element(By.ID, 'pin-request-phone-phone-number')
    # number_input.clear()  
    number_input.send_keys(number)

    # Click continue button
    press_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "quickpayConfirmation_0"))
    )
    time.sleep(2)  # Before click to allow values to be set in
    press_button.click()

    # Check for error after page submission to ouput if prepaid or not
    landing_html = driver.page_source
    soup = bs(landing_html, 'html.parser')
    
    driver.quit()
    payment_section = soup.find('div', id='appMessage')
    if payment_section:
        error_section = payment_section.find('section', id='error')
        if error_section:
            return (number, 1)
        else:
            return (number, 0)
    else:
        return (number, 2)


if __name__ == "__main__":
    # 200 results/hour
    # Read in file
    # with open(r"C:\Users\angel\Documents\test_panel_porting_usat.txt", 'r') as file:
    #     number_lst = [line.strip()[1:] if line.strip().startswith('1') else line.strip() for line in file][:3300]

    # print(number_lst)
    number_lst = ['6179910927','2029753009','8648679095','2093167838','5189020694']
    url = 'https://www.paygonline.com/websc/quickpay.html'
    df = pd.DataFrame(columns = ['phone', 'nuance','prepaid'])

    count = 1
    for number in number_lst:
        result = main(url, number)
        if result[1] > 0:
            ohe = 1
        else: 
            ohe = 0
        df = df._append({'phone': number, 'nuance': result[1], 'prepaid': ohe}, ignore_index=True)
        # Gradually add to file
        df.to_excel(r'C:\Users\Administrator\Desktop\USAT\test.xlsx', sheet_name='USAT', index=False)

        print(count)
        count+=1


    df.to_excel(r'C:\Users\Administrator\Desktop\USAT\test.xlsx', sheet_name='USAT', index=False)

