import datetime
import requests


def event_all(urls):
    url = f"https://www.afisha.ru{urls}"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Afisha-Layout-Required': 'false',
        'Cookie': '_afuid=1678040942866466812; ruid=ugsAAG7fBGTXL9iuAUm2CwB='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json())


def event_3day(urls):
    date_search = f"{datetime.datetime.now().strftime('%d')}-{datetime.datetime.now().strftime('%m')}_" \
                  f"{int(datetime.datetime.now().strftime('%d')) + 2}-{datetime.datetime.now().strftime('%m')}"
    url = f"https://www.afisha.ru{urls}events/{date_search}/"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'Cookie': '_afuid=1678040942866466812; ruid=ugsAAG7fBGTXL9iuAUm2CwB='
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    all_event_list = []

    for respons_item in response.json()["ScheduleWidget"]["Items"]:
        event_list_genre = []
        event_list_discription = []
        event_list_data = []
        event_list_type = []
        event_list_poster = []
        event_list_url = []
        event_dict = {}

        event_list_url.append(f"https://www.afisha.ru{respons_item['Url']}")

        try:
            event_list_poster.append(respons_item["Image16x9"]["Url"])
        except:
            event_list_poster.append("None")

        if respons_item["Notice"]["Dates"] is None:
            event_list_data.append(respons_item["Notice"]["Places"])
        else:
            event_list_data.append(respons_item["Notice"]["Dates"])

        event_list_discription.append(respons_item["Name"])
        event_list_type.append(respons_item["DisplayType"])

        for genres in respons_item["Genres"]["Links"]:
            event_list_genre.append(genres["Name"])

        try:
            for discription in respons_item["Executors"]["Links"]:
                event_list_genre.append(discription["Name"])
        except:
            pass

        event_dict["data"] = event_list_data
        event_dict["type"] = event_list_type
        event_dict["genre"] = event_list_genre
        event_dict["discription"] = event_list_discription
        event_dict["poster"] = event_list_poster
        event_dict["link"] = event_list_url

        all_event_list.append(event_dict)
    return all_event_list
