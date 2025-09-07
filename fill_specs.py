# Файл: fill_specs.py
import time
import random
import json
# ... (все импорты из v9)

# --- КОНФИГУРАЦИЯ ---
CURRENT_CATEGORY = 'korpus' # <-- Меняй здесь

CONFIG = {
    'videocards': {'output_file': 'gpus_dns_with_specs.json'},
    'processors': {'output_file': 'cpus_dns_with_specs.json'},
    'ram': {'output_file': 'ram_dns_with_specs.json'},
    'block': {'output_file': 'block_dns_with_specs.json'},
    'motherboard': {'output_file': 'motherboard_dns_with_specs.json'},
    'korpus': {'output_file': 'korpus_dns_with_specs.json'},
    'ssdsata': {'output_file': 'ssdsata_dns_with_specs.json'}
}
# -------------------------

# --- ВСТАВЬ СЮДА СВЕЖИЕ ДАННЫЕ ---
COOKIE_STRING = """..."""
# ------------------------------------

# ... (весь остальной код из v9, но RESULT_FILE берется из CONFIG)
if __name__ == "__main__":
    config = CONFIG[CURRENT_CATEGORY]
    RESULT_FILE = config['output_file']
    # ... (дальше все как было)