import requests
import time
from collections import deque

from secrets import aio_api_key, alertzy_account_keys


aio_url_template = "https://io.adafruit.com/api/v2/delta_lab/feeds/rsim-v3-max-peralta.feed_key/data/last"

aio_headers = {
    "X-AIO-Key": aio_api_key
}

alertzy_url = "https://alertzy.app/send"

alertzy_data = {
    "accountKey": alertzy_account_keys,
    "title": "RSIM Sala de Geriatría",
    "message": ""
}


aio_feed_keys = ["equivalent-noise-level", "battery-state"]

aio_last_ids = {x: None for x in aio_feed_keys}
aio_threshold = 75.0
aio_window_size = 3
aio_last_values = deque(maxlen=aio_window_size)
aio_max_charged_state_reminders = 3
aio_last_bat_states = deque(maxlen=aio_max_charged_state_reminders)
aio_first_run = True


while True:
    for feed_key in aio_feed_keys:
        aio_url = aio_url_template.replace("feed_key", feed_key)
        response = requests.get(aio_url, headers=aio_headers)

        if response.status_code == 200:
            data = response.json()

            if (data["id"] not in aio_last_ids.values()) and not aio_first_run:
                print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] [POLLING]: {feed_key}: {response.json()}")

                match feed_key:
                    case "equivalent-noise-level":
                        dBA_value = float(data["value"])
                        aio_last_values.append(dBA_value)

                        if len(aio_last_values) == aio_window_size and all([x > aio_threshold for x in aio_last_values]):
                            dBA_value_rounded = int(round(dBA_value, 0))
                            alertzy_data["message"] = f"Ruido alto: {dBA_value_rounded} dBA"

                            requests.post(alertzy_url, data=alertzy_data)

                            print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] [ALERTS]: High noise level notification sent.")

                    case "battery-state":
                        match int(data["value"]):
                            case 0: # LOW_BATTERY
                                alertzy_data["message"] = "Batería baja. Por favor conecte el cargador."
                                requests.post(alertzy_url, data=alertzy_data)

                                print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] [ALERTS]: Low battery notification sent.")
                            case 3: # CHARGED
                                if len(aio_last_bat_states) == aio_max_charged_state_reminders:
                                    aio_last_bat_states.append(int(data["value"]))

                                    if not all([x == 3 for x in aio_last_bat_states]):
                                        alertzy_data["message"] = "Batería cargada. Opcionalmente, desconecte el cargador."
                                        requests.post(alertzy_url, data=alertzy_data)

                                        print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] [ALERTS]:Charged battery notification sent.")
                                    else:
                                        print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] [ALERTS]: Charged battery notification limit reached.")
                                else:
                                    aio_last_bat_states.append(int(data["value"]))
                                    alertzy_data["message"] = "Batería cargada. Opcionalmente, desconecte el cargador."
                                    requests.post(alertzy_url, data=alertzy_data)

                                    print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] [ALERTS]:Charged battery notification sent.")

                aio_last_ids[feed_key] = data["id"]

            elif aio_first_run:
                aio_last_ids[feed_key] = data["id"]

                if None not in aio_last_ids.values():
                    aio_first_run = False

                    print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [INFO] [POLLING]: Finished first run.")

        else:
            print(f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] [ERROR] [POLLING]: Adafruit IO polling failed, HTTP status code {response.status_code}")

        time.sleep(2)
