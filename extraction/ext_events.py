import requests


def event(url):
    url = f"https://www.afisha.ru{url}"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Afisha-Layout-Required': 'false',
        'Cookie': '_afuid=1678040942866466812; ruid=ugsAAG7fBGTXL9iuAUm2CwB='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json())


event("/eee/")