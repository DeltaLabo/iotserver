import requests
import time

from secrets import aio_api_key, alertzy_account_keys


aio_url = "https://io.adafruit.com/api/v2/delta_lab/feeds/rsim-v3-max-peralta.equivalent-noise-level/data/last"

aio_headers = {
    "X-AIO-Key": aio_api_key
}

alertzy_url = "https://alertzy.app/send"

alertzy_data = {
    "accountKey": alertzy_account_keys,
    "title": "RSIM Sala de Geriatría",
    "message": "Ruido alto: {} dBA"
}


aio_last_id = ""

while True:
    response = requests.get(aio_url, headers=aio_headers)

    if response.status_code == 200:
        data = response.json()

        if (data["id"] != aio_last_id) and (aio_last_id != ""):
            dBA_value = float(data["value"])

            if dBA_value > 70.0:
                dBA_value = int(round(dBA_value, 0))
                alertzy_data["message"] = f"Ruido alto: {dBA_value} dBA"

                requests.post(alertzy_url, data=alertzy_data)

            aio_last_id = data["id"]

        elif aio_last_id == "":
            aio_last_id = data["id"]

    time.sleep(20)
