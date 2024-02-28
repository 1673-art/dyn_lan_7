import requests
from bs4 import BeautifulSoup
import json

url = "https://auto.drom.ru/all/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

cars = []

prices = soup.find_all('span', {'data-ftid': 'bull_price'})
car_info_tags = soup.find_all('img', alt=True)

for i, car_info_tag in enumerate(car_info_tags[:20]):
    car_info = car_info_tag['alt']
    car_price = prices[i].text.strip().replace('\xa0', '')  # Удаляем пробелы и символы неразрывного пробела из цены
    car = {'марка': car_info.split(',')[0], 'цена': car_price}
    cars.append(car)

with open('cars.json', 'w', encoding='utf-8') as f:
    json.dump(cars, f, ensure_ascii=False, indent=4)

print("Информация о первых 20 машинах была записана в файл cars.json")
