import requests
from bs4 import BeautifulSoup
import json
import time
import random
import re

# --- КОНФИГУРАЦИЯ ---
BASE_URL = 'https://www.dns-shop.ru/catalog/17a8a69116404e77/myshi/'
PAGES_TO_PARSE = 10 
RESULT_FILE = 'mice_dns_with_specs.json'
# --------------------

# --- ВСТАВЬ СЮДА СВЕЖИЕ ДАННЫЕ ПЕРЕД ЗАПУСКОМ ---
COOKIE_STRING = """_ab__monthly-payment=monthly-payment_2; rrpvid=904400357880317; IsInterregionalPickupAllowed=true; cartUserCookieIdent_v3=54b8bbf927768d1b397d4ad15f1103743c847333497c2edab33df8b9a24be3c5a%3A2%3A%7Bi%3A0%3Bs%3A22%3A%22cartUserCookieIdent_v3%22%3Bi%3A1%3Bs%3A36%3A%22b118bfc1-4d82-360c-a695-b9b8a339e40c%22%3B%7D; rcuid=68a16118bd428f86157c5386; _gcl_au=1.1.1809232422.1757163448; _ga=GA1.1.893858812.1757163448; _ymab_param=K5UY-ga7el-20dH6mw3kYoyALJc4mbJo2paCY0T6tKXbgP8s3_M668EI_I73-paSOHPXX3mrN8Kk782fGZuBAKF_Y7E; _ym_uid=1757163448516673077; _ym_d=1757163448; current_path=0a3aa1870e6a388c5e98a8c8bcdf2931714b0cb20946fae5a4264468f117fd25a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22current_path%22%3Bi%3A1%3Bs%3A121%3A%22%7B%22city%22%3A%2230b7c1f1-03fb-11dc-95ee-00151716f9f5%22%2C%22cityName%22%3A%22%5Cu0418%5Cu0440%5Cu043a%5Cu0443%5Cu0442%5Cu0441%5Cu043a%22%2C%22method%22%3A%22manual%22%7D%22%3B%7D; phonesIdentV2=d4ae6c28-b5d6-450c-a7eb-51072721421e; rsu-id=79897748-5e95-46a0-8e56-457da1ea627b; ab_spa=%7B%22endless-feed-test%22%3A%22list_2%22%7D; _ab__eol_analogs=has_analogs_group; cookieImagesUploadId=8cbe716b1af7d4552f57fb978b1aa4c0a2b21f3e48a3b6a48ee40df9ea2f97eba%3A2%3A%7Bi%3A0%3Bs%3A20%3A%22cookieImagesUploadId%22%3Bi%3A1%3Bs%3A36%3A%22d69d945e-f5de-497b-80b0-bfc089c6300c%22%3B%7D; _ym_isad=1; PHPSESSID=2cedadc7e6b966fd7096abb74389d229; lang=ru; _csrf=7087476598ba6877fc14ff9dc7d680458b12d87bf09166501ac8e4d50cfd6ff8a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22XEkcR5lioAgpoMt3xIHMuw0blM2CcOhm%22%3B%7D; city_path=irkutsk; _ym_visorc=w; qrator_jsr=v2.0.1757305380.833.b030215dN2gf7FrT|3e1chos5v8RLtk0U|jodev+TETsHmLtsgLNHeSxB+fCitxbpfuHY78KHU7U2644JyFJs55BcerWyLAkCtA778XqFps96nKPw1dtWdbg==-YsYU8SEFgWU31e6lxEoQ5lcqTVc=-00; qrator_jsid2=v2.0.1757305380.833.b030215dN2gf7FrT|PDRvhJPZFmFKJW6W|7OVhkXjktEdu85Wpq+rxzzMPnNbmzIQHYgo+sHHK/G+uk0tGFgpBC8hBdi8UmJzskH0DRjtdWGMWeNtSN1mquCnjeWcDC/Q/U8V21ZfGCyEKjsBUwAcxeXNZDDjq1/9uLrMfO30hsVLD8stvTn2htQ==-OYJGIr4Mzq/VXiKg3EnbHPcPW2o=; rr-testCookie=testvalue; _ga_FLS4JETDHW=GS2.1.s1757302101$o14$g1$t1757305396$j10$l0$h1551798609"""
CSRF_TOKEN_STRING = "4Xupw9ZidJXQsaPYW_iZJYNhOqrGi1LqSA0Jsm7J9X25PsKghFcY_L_wxKg0te0W-yhy57P8YogkQDvxDYadEA=="
# ----------------------------------------------------

# Используем сессию для удобства
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
    'Cookie': COOKIE_STRING
})

def get_products_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    products = soup.find_all('div', class_='catalog-product')
    page_products = []
    for product in products:
        short_id = product.get('data-code')
        long_id = product.get('data-product')
        if not short_id or not long_id: continue
        name_tag = product.find('a', class_='catalog-product__name')
        name = name_tag.get_text(strip=True) if name_tag else 'N/A'
        link = "https://www.dns-shop.ru" + name_tag['href'] if name_tag and 'href' in name_tag.attrs else 'N/A'
        page_products.append({'short_id': short_id, 'long_id': long_id, 'name': name, 'price': 0, 'link': link, 'specifications': {}})
    return page_products

if __name__ == "__main__":
    API_URL = 'https://www.dns-shop.ru/ajax-state/product-buy/'
    all_products_info = []

    print("--- ЭТАП 1: Сбор ID, названий и ссылок ---")
    for page_num in range(1, PAGES_TO_PARSE + 1):
        url = f"{BASE_URL}?p={page_num}" if page_num > 1 else BASE_URL
        print(f"Парсим страницу {page_num} из {PAGES_TO_PARSE}...")
        try:
            response_get = session.get(url, headers={'Referer': BASE_URL})
            response_get.raise_for_status()
            page_products = get_products_from_html(response_get.text)
            if not page_products: break
            all_products_info.extend(page_products)
            time.sleep(random.uniform(1, 3))
        except Exception as e:
            print(f"Ошибка на странице {page_num}: {e}. Выход."); exit()
    
    if not all_products_info:
        print("Не удалось собрать информацию о товарах. Выход."); exit()
    
    print(f"\n--- ЭТАП 2: Запрос цен через API ---")
    session.headers.update({
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest', 'Referer': BASE_URL,
        'x-csrf-token': CSRF_TOKEN_STRING,
        'content-type': 'application/x-www-form-urlencoded'
    })

    product_short_ids = [p['short_id'] for p in all_products_info]
    prices = {}
    CHUNK_SIZE = 100
    for i in range(0, len(product_short_ids), CHUNK_SIZE):
        chunk = product_short_ids[i:i + CHUNK_SIZE]
        containers = [{"id": f"as-{i}", "data": {"id": pid}} for i, pid in enumerate(chunk)]
        post_data = {'data': json.dumps({"type": "product-buy", "containers": containers})}
        try:
            response = session.post(API_URL, data=post_data)
            response.raise_for_status()
            price_data = response.json()
            if price_data.get('data') and isinstance(price_data['data'].get('states'), list):
                for item in price_data['data']['states']:
                    if not item: continue
                    data_dict = item.get('data')
                    if not data_dict: continue
                    long_id = data_dict.get('id')
                    price_dict = data_dict.get('price')
                    if not long_id or not price_dict: continue
                    current_price = price_dict.get('current')
                    if current_price is not None: prices[long_id] = current_price
            time.sleep(random.uniform(1, 2))
        except Exception as e:
            print(f"Ошибка при запросе порции цен: {e}")
    
    print("\n--- ЭТАП 3: Объединение и сохранение базового файла ---")
    updated_count = 0
    for product in all_products_info:
        if product['long_id'] in prices:
            product['price'] = prices[product['long_id']]; updated_count += 1
    
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_products_info, f, ensure_ascii=False, indent=4)
    
    print(f"\nУСПЕХ! Базовый файл '{RESULT_FILE}' создан.")
    print(f"Всего товаров: {len(all_products_info)}. Цены найдены для {updated_count} товаров.")