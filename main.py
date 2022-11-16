from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
BASE_URL = 'https://www.finam.ru/quotes/stocks/russia/'
driver.get(BASE_URL)


def get_next_page():
    """
    Функция для перехода на следующую страницу
    """
    elem = driver.find_element(
        By.CSS_SELECTOR, 'li.index__paginationItemContainer--2PC:nth-child(11) > a:nth-child(1)')
    driver.execute_script('arguments[0].click();', elem)
    return True if elem else False


def get_shares() -> dict:
    """
    Функция для сбора информации об акциях в России
    """
    columns = driver.find_elements(By.CLASS_NAME, 'QuoteTable__tableHead--33b')
    column_names = {column.text: [] for column in columns}

    while get_next_page():
        sleep(2)  # задержка, чтобы DOM прогрузиться успел
        data_with_row = driver.find_elements(
            By.CLASS_NAME, 'QuoteTable__tableRow--1f0')
        data_from_cells = [
            [
                cell.text
                for cell in cell.find_elements(By.CLASS_NAME, 'QuoteTable__tableCell--151')
            ]
            for cell in data_with_row]

        counter = 0
        for row in data_from_cells:
            for key in column_names.keys():
                for _ in range(0, len(row)):
                    column_names[key].append(row[counter])
                    counter += 1
                    break
            counter = 0

        if 'index__disabled--2v5' in driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div[2]/div/div/div[6]/div/div/ul/li[11]/a'
            ).get_attribute('class'):
            return column_names

        data_with_row = []
        data_from_cells = []
    return column_names


# Сохранение результата в excel
result = get_shares()
result = pd.DataFrame(result)
result.to_excel('./result.xlsx')
