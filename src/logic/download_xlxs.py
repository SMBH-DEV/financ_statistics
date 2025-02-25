from datetime import date, datetime
import pytz
from src.config.settings import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
from loguru import logger

async def current_date():
    current_utc = datetime.now(pytz.UTC)
    day = current_utc.day
    month = current_utc.strftime('%b')  # Получаем месяц в формате первых трех букв (Jan, Feb, etc.)
    year = current_utc.year
    
    return day, month, year


async def get_data():
    # Создаем путь для сохранения файлов
    download_path = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_path, exist_ok=True)
    
    # Проверяем и форматируем URL
    base_url = settings.URL
    if not base_url.startswith(('http://', 'https://')):
        base_url = f'https://{base_url}'
    
    auth_url = f'{base_url}/auth'
    statistics_url = f'{base_url}/statistics'
    
    # Настройка Chrome
    chrome_options = Options()
    # Добавляем настройки для фонового режима
    chrome_options.add_argument('--headless')  # Запуск в фоновом режиме
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    # Настройки для скачивания файлов
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        # Дополнительные настройки для работы в headless режиме
        "download.default_directory_cleanup": True,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1
    })
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Авторизация
        driver.get(auth_url)
        
        # Находим поле email по атрибуту name и placeholder
        email_input = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "input[name='username'][placeholder='E-mail*']"
        )))
        
        # Находим поле password
        password_input = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            "input[name='password'][placeholder='Enter password']"
        )))
        
        # Вводим данные
        email_input.send_keys(settings.LOGIN)
        password_input.send_keys(settings.PASSWORD)
        
        # Нажимаем кнопку входа, используя текст на кнопке
        login_button = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//button[@type='submit']//span[text()='Log In']/.."
        )))
        login_button.click()
        
        # Ждем редиректа и переходим на страницу статистики
        wait.until(EC.url_changes(auth_url))
        driver.get(statistics_url)
        
        # Ждем загрузки страницы
        # Находим поле Split by по placeholder
        split_by_dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH, 
            "//div[contains(@class, 'dx-dropdowneditor-input-wrapper')]//div[@data-dx_placeholder='Split by']/.."
        )))
        
        # Открываем выпадающий список первый раз
        split_by_dropdown.click()
        
        # Выбор Organization
        organization_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'dx-item-content') and text()='Organization']")))
        organization_option.click()
        
        # Пауза для обработки первого выбора
        time.sleep(2)
        
        # Находим и открываем выпадающий список снова
        split_by_dropdown = wait.until(EC.element_to_be_clickable((
            By.XPATH, 
            "//div[contains(@class, 'dx-dropdowneditor-input-wrapper')]//div[@data-dx_placeholder='Split by']/.."
        )))
        split_by_dropdown.click()
        
        # Выбор Ad object
        ad_object_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'dx-item-content') and text()='Ad object']")))
        ad_object_option.click()
        
        # Нажатие кнопки Get Data
        get_data_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'dx-button-content')]//p[text()='Get Data']")))
        get_data_button.click()
        
        # Ждем 5 секунд, пока данные загрузятся
        time.sleep(5)
        
        # Нажатие кнопки Download Excel
        download_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'dx-button-content')]//p[text()='Download Excel']")))
        download_button.click()
        
        # Ждем загрузки файла
        time.sleep(5)
        
        # Получаем текущую дату для проверки имени файла
        current_utc = datetime.now(pytz.UTC)
        expected_filename = f"Report.xlsx {current_utc.day:02d}.{current_utc.month:02d}.{current_utc.year}.xlsx"
        expected_file = os.path.join(download_path, expected_filename)
        
        # Ждем появления файла
        timeout = time.time() + 30  # ждем максимум 30 секунд
        while not os.path.exists(expected_file):
            if time.time() > timeout:
                raise Exception(f"Файл {expected_filename} не был загружен за отведенное время")
            time.sleep(1)
            
        return expected_file  # Возвращаем полный путь к скачанному файлу
        
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        raise
        
    finally:
        driver.quit()