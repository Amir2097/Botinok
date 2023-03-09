import requests


def rec_db_cityes():
    url = "https://www.afisha.ru/ufa/"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Afisha-Layout-Required': 'true',
        'Cookie': '_afuid=1678040942866466812; ruid=ugsAAG7fBGTXL9iuAUm2CwB='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    for liter in response.json()["Layout"]["CitySelector"]["OnLetterNamedCityGroups"]:
        for liters in liter["Cities"]:
            return liters

print(rec_db_cityes())