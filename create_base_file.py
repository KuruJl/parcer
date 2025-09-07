# Файл: create_base_file.py
import requests
from bs4 import BeautifulSoup
import json
import time
import random

# --- КОНФИГУРАЦИЯ ---
CURRENT_CATEGORY = 'ram' # <-- Меняй здесь
# ... (остальной блок CONFIG как выше)

# --- ВСТАВЬ СЮДА СВЕЖИЕ ДАННЫЕ ---
COOKIE_STRING = """..."""
CSRF_TOKEN_STRING = "..."
# ------------------------------------

# ... (Код из скрипта v6, который использует requests и API для цен) ...
# В результате он создает файл, например, cpus_dns_with_specs.json, но со пустыми specifications