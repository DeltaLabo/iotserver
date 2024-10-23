import requests
import time
from collections import deque

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
aio_threshold = 75.0
aio_window_size = 3
aio_last_values = deque(maxlen=aio_window_size)


while True:
    response = requests.get(aio_url, headers=aio_headers)

    if response.status_code == 200:
        data = response.json()

        if (data["id"] != aio_last_id) and (aio_last_id != ""):
            dBA_value = float(data["value"])
            aio_last_values.append(dBA_value)

            if len(aio_last_values) == aio_window_size and all([x > aio_threshold for x in aio_last_values]):
                dBA_value_rounded = int(round(dBA_value, 0))
                alertzy_data["message"] = f"Ruido alto: {dBA_value_rounded} dBA"

                requests.post(alertzy_url, data=alertzy_data)

            aio_last_id = data["id"]

        elif aio_last_id == "":
            aio_last_id = data["id"]

    time.sleep(1)
