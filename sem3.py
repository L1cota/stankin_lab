import re

def get_sku_from_text(text : str) -> list:
    """функция для извлечения SKU из текста"""
    pattern = r'[A-Z]{2}-\d{4}(?:-[A-Z]{3})?|\d{4}-[A-Z]{2}'
    
    skus = []
    lines = text.splitlines()
    
    for line in lines:
        match = re.search(pattern, line)
        if match:
            skus.append(match.group(0))
        else:
            skus.append(None)
            
    return skus

f = open("file.txt", "r")
content = f.read()
f.close()

for sku in get_sku_from_text(content):
    print(sku)