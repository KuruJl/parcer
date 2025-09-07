import time
import random
import json
import os.path
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

# --- КОНФИГУРАЦИЯ ---
RESULT_FILE = 'ssdsata_dns_with_specs.json'
# --------------------

# --- ВСТАВЬ СЮДА СВЕЖИЕ ДАННЫЕ ПЕРЕД ЗАПУСКОМ ---
COOKIE_STRING = """_ab__monthly-payment=monthly-payment_2; rrpvid=904400357880317; IsInterregionalPickupAllowed=true; cartUserCookieIdent_v3=54b8bbf927768d1b397d4ad15f1103743c847333497c2edab33df8b9a24be3c5a%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22b118bfc1-4d82-360c-a695-b9b8a339e40c%22%3B%7D; rcuid=68a16118bd428f86157c5386; _gcl_au=1.1.1809232422.1757163448; _ga=GA1.1.893858812.1757163448; _ymab_param=K5UY-ga7el-20dH6mw3kYoyALJc4mbJo2paCY0T6tKXbgP8s3_M668EI_I73-paSOHPXX3mrN8Kk782fGZuBAKF_Y7E; _ym_uid=1757163448516673077; _ym_d=1757163448; current_path=0a3aa1870e6a388c5e98a8c8bcdf2931714b0cb20946fae5a4264468f117fd25a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A121%3A%22%7B%22city%22%3A%2230b7c1f1-03fb-11dc-95ee-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0418%5Cu0440%5Cu043a%5Cu0443%5Cu0442%5Cu0441%5Cu043a%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D; phonesIdentV2=d4ae6c28-b5d6-450c-a7eb-51072721421e; rsu-id=79897748-5e95-46a0-8e56-457da1ea627b; ab_spa=%7B%22endless-feed-test%22%3A%22list_2%22%7D; _ab__eol_analogs=has_analogs_group; lang=ru; _csrf=f6c1cfd657f0b2956798a2ee62f014539c442cfdbae6f41b6eee08fdeb49fba7a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22pWlhnL-UbcjGain8egw-e59MwwhrWDE9%22%3B%7D; city_path=irkutsk; cookieImagesUploadId=8cbe716b1af7d4552f57fb978b1aa4c0a2b21f3e48a3b6a48ee40df9ea2f97eba%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22cookieImagesUploadId%22%3Bi%3A1%3Bs%3A36%3A%22d69d945e-f5de-497b-80b0-bfc089c6300c%22%3B%7D; _ym_isad=1; PHPSESSID=2cedadc7e6b966fd7096abb74389d229; qrator_ssid2=v2.0.1757256495.785.b030215dKf4QTbrb|avTSNSzeIpICsfhr|89PTLMhu9c9RkkMEBxuvMMjV02XWXLgeeBQYLduJK8i5tKpSO0mrTxbGE62dG/r+/mLWBIUtDreDKoHIS3PyQQ==-ONiPTnYvWCWduOq/TMUQvX4W3uI=; qrator_jsr=v2.0.1757256495.785.b030215dKf4QTbrb|1jPaUnAeb9b2XoAc|/GRFqKEhOQGEUt6MRCtuXCbHWEz/ka2NmnaBv/i+2toj0s40MXi5n4BYyvSz4GE2UxHxkria4b5T3DdTbdvs7Q==-oHDOIXECoIUSI1t1iSZ4dqxSaLU=-00; qrator_jsid2=v2.0.1757256495.785.b030215dKf4QTbrb|LmuBDK3eSRbU0mIJ|MtD7AIstMgP8O1Y63wWCzSMff7rcHjVsV89jagKJb8k8zsmeqSAc/MN1a7IjIqD5buSj2foinJDJNWV7/O3A00wiICxL03+E1nFgAp0y730sEu1CD8Gzme2Q38GcHcjYfkPdDgKP0IS7H2k6TOKi8Q==-afit8nlhUjYdcN6nPtD1s7OIh30=; _ym_visorc=b; rr-testCookie=testvalue; _ga_FLS4JETDHW=GS2.1.s1757256677$o11$g1$t1757256845$j59$l0$h183288007"""
# ----------------------------------------------------

# --- НАСТРОЙКА SELENIUM ---
service = Service(executable_path='chromedriver.exe')
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(120)

stealth(driver, languages=["ru-RU", "ru"], vendor="Google Inc.", platform="Win32",
        webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)
print("Selenium-stealth WebDriver запущен (режим 'Быстрый скроллер').")

def parse_specs_from_product_page(html):
    specs = {}
    soup = BeautifulSoup(html, 'lxml')
    characteristic_rows = soup.find_all('li', class_='product-characteristics__spec')
    for row in characteristic_rows:
        title_tag = row.find('div', class_='product-characteristics__spec-title')
        value_tag = row.find('div', class_='product-characteristics__spec-value')
        if title_tag and value_tag:
            specs[title_tag.get_text(strip=True)] = value_tag.get_text(strip=True)
    return specs

if __name__ == "__main__":
    all_products_info = []
    if os.path.exists(RESULT_FILE):
        print(f"Найден файл '{RESULT_FILE}'. Загружаем данные для продолжения...")
        with open(RESULT_FILE, 'r', encoding='utf-8') as f:
            all_products_info = json.load(f)
        print(f"Загружено {len(all_products_info)} товаров.")
    else:
        print(f"Файл '{RESULT_FILE}' не найден. Сначала запустите create_base_cpu_file.py")
        driver.quit(); exit()

    if all_products_info:
        print("\n--- ЭТАП 4: Сбор подробных характеристик ---")
        driver.get("https://www.dns-shop.ru/")
        cookie_parts = [c.strip().split('=', 1) for c in COOKIE_STRING.split(';') if '=' in c]
        for part in cookie_parts:
            driver.add_cookie({'name': part[0], 'value': part[1], 'domain': '.dns-shop.ru'})
        time.sleep(3)

        processed_count = sum(1 for p in all_products_info if p.get('specifications'))
        print(f"Уже обработано: {processed_count} из {len(all_products_info)} товаров.")

        for i, product in enumerate(all_products_info):
            if product.get('specifications'): continue

            print(f"Обработка товара {i+1}/{len(all_products_info)}: {product['name'][:50]}...")
            try:
                driver.get(product['link'])
                time.sleep(3)
                print("    > Быстрая прокрутка до зоны характеристик...")
                for _ in range(3):
                    driver.execute_script("window.scrollBy(0, 500);"); time.sleep(0.5)
                try:
                    wait = WebDriverWait(driver, 10)
                    expand_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "product-characteristics__expand")))
                    driver.execute_script("arguments[0].click();", expand_button)
                    print(f"    > Кнопка найдена и нажата."); time.sleep(2)
                except Exception:
                    print("    > Кнопка не найдена, продолжаем без клика...")
                
                html = driver.page_source
                specs = parse_specs_from_product_page(html)
                if not specs: print("    ! Характеристики не найдены. Пропускаем.")
                
                product['specifications'] = specs
                
                with open(RESULT_FILE, 'w', encoding='utf-8') as f:
                    json.dump(all_products_info, f, ensure_ascii=False, indent=4)
                
                time.sleep(random.uniform(1, 4)) # <-- Оптимизированное ожидание

            except Exception as e:
                print(f"    ! Критическая ошибка: {e}"); driver.quit(); exit()

        print("\nПОЛНЫЙ УСПЕХ! Все характеристики для процессоров собраны.")
        driver.quit()