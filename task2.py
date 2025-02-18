from io import BytesIO

import requests
from PIL import Image

from app.geocode import get_ll, get_spn, get_org, get_distance

toponym_to_find = 'Тольятти, Ленинский, 20'
toponym_long, toponym_lat = get_ll(toponym_to_find)
delta = "0.005,0.005"
address_ll = f"{toponym_long},{toponym_lat}"

organization = get_org(address_ll, delta, 'аптека')
print(organization)
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = f"{point[0]},{point[1]}"
apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": delta,
    "apikey": apikey,
    # добавим точку, чтобы указать найденную аптеку
    "pt": f'{org_point},pm2dgl~{address_ll},pm2rdl',

}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()

org_time = organization["properties"]["CompanyMetaData"]["Hours"]['text']
a = (float(toponym_long), float(toponym_lat))
b = (float(point[0]), float(point[1]))
distance = f'Расстояние:\t{get_distance(a, b)} км.'
name = f'Название:\t{org_name}'
adress = f'Адрес:\t{org_address}'
time = f'Время работы:\t{org_time}'
print(name, adress, time, distance, sep='\n')
