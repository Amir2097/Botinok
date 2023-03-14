import datetime
import requests
from Database import return_url


def event_all(ids):
    url = return_url(ids)
    url = f"https://www.afisha.ru{url}"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Afisha-Layout-Required': 'false',
        'Cookie': '_afuid=1678040942866466812; ruid=ugsAAG7fBGTXL9iuAUm2CwB='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json())


def event_3day(ids):
    url = return_url(ids)
    date_search = f"{datetime.datetime.now().strftime('%d')}-{datetime.datetime.now().strftime('%m')}_" \
                  f"{int(datetime.datetime.now().strftime('%d')) + 2}-{datetime.datetime.now().strftime('%m')}"
    url = f"https://www.afisha.ru{url}events/{date_search}/"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Afisha-Layout-Required': 'false',
        'Cookie': '_afuid=1678040942866466812; ruid=ugsAAG7fBGTXL9iuAUm2CwB='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    all_event_list = []

    for respons_item in response.json()["ScheduleWidget"]["Items"]:
        event_list = []
        for genres in respons_item["Genres"]["Links"]:
            event_list.append(genres["Name"])

        try:
            for discription in respons_item["Executors"]["Links"]:
                event_list.append(discription["Name"])
        except:
            pass

        # print(respons_item)

        all_event_list.append(event_list)

    print(all_event_list)


event_3day(858035466)
