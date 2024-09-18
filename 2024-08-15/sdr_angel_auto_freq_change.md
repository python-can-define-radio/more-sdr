Explanation should go here. Hack RF, SDR Angel ...

<details><summary>Expand for in-progress attempt</summary>

```python3
#!/usr/bin/env python

## Source: https://github.com/f4exb/sdrangel/blob/master/swagger/sdrangel/examples/
## License is GPL-3.0 as required

import json
import time

import requests

base_url = "http://127.0.0.1:8091/sdrangel"



def prettyResp(response: requests.Response) -> str:
    """Prints json with proper indentation.
    Prints others directly."""
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        return json.dumps(response.json(), indent=4, sort_keys=True)
    else:
        return response.text


def was_success(r: requests.Response) -> bool:
    return 200 <= r.status_code < 300


def set_freq(freq: int):
    base_url = "http://127.0.0.1:8091/sdrangel"
    desired_settings = {
        "deviceHwType": "HackRF",
        "direction": 1,
        "hackRFOutputSettings": {
            "centerFrequency": freq,
        }
    }
    response = requests.patch(
        base_url + "/deviceset/0/device/settings",
        desired_settings
    )
    print("Response status code:", response.status_code)
    if was_success(response):
        j = response.json()
        print(json.dumps(j, indent=4, sort_keys=True))
    else:
        print(prettyResp(response))


if __name__ == "__main__":
    while True:
        set_freq(int(105.3e6))
        time.sleep(2)
        set_freq(int(104.7e6))
        time.sleep(2)
```
</details>

<details><summary>Expand for original code</summary>

```python3
#!/usr/bin/env python

import time
import requests, json, traceback, sys
from optparse import OptionParser

base_url = "http://127.0.0.1:8091/sdrangel"

requests_methods = {
    "GET": requests.get,
    "PATCH": requests.patch,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete
}


# ======================================================================
def getInputOptions():

    parser = OptionParser(usage="usage: %%prog [-t]\n")
    parser.add_option("-a", "--address", dest="address", help="address and port", metavar="ADDRESS", type="string")

    (options, args) = parser.parse_args()

    if (options.address == None):
        options.address = "127.0.0.1:8091"

    return options


# ======================================================================
def printResponse(response):
    content_type = response.headers.get("Content-Type", None)
    if content_type is not None:
        if "application/json" in content_type:
            print(json.dumps(response.json(), indent=4, sort_keys=True))
        elif "text/plain" in content_type:
            print(response.text)


# ======================================================================
def callAPI(url, method, params, json, text):
    request_method = requests_methods.get(method, None)
    if request_method is not None:
        r = request_method(url=base_url + url, params=params, json=json)
        if r.status_code / 100 == 2:
            print(text + " succeeded")
            printResponse(r)
            return r.json()  # all 200 yield application/json response
        else:
            print(text + " failed")
            printResponse(r)
            return None


# ======================================================================
def set_freq(freq: int):
#     try:
#     options = getInputOptions()

    global base_url
    base_url = "http://127.0.0.1:8091/sdrangel"

    desired_settings = {
            "deviceHwType": "HackRF",
            "direction": 1,
            "hackRFOutputSettings": {
                "centerFrequency": freq,
            }
        }
    settings = callAPI(
        "/deviceset/0/device/settings",
        "PATCH",
        None,
        desired_settings,
        "doing the thing")
        
        
#         if settings is None:
#             exit(-1)
# 
#         settings["NFMDemodSettings"]["inputFrequencyOffset"] = 12500
#         settings["NFMDemodSettings"]["afBandwidth"] = 5000
# 
#         r = callAPI("/deviceset/0/channel/0/settings", "PATCH", None, settings, "Change NFM demod")
#         if r is None:
#             exit(-1)
# 
#         r = callAPI("/deviceset", "POST", {"direction": 1}, None, "Add Tx device set")
#         if r is None:
#             exit(-1)
# 
#         settings = callAPI("/deviceset/1/channel", "POST", None, {"channelType": "NFMMod", "direction": 1}, "Create NFM mod")
#         if settings is None:
#             exit(-1)
# 
#         settings["NFMModSettings"]["inputFrequencyOffset"] = 12500
#         settings["NFMModSettings"]["cwKeyer"]["text"] = "VVV DE F4EXB  "
#         settings["NFMModSettings"]["cwKeyer"]["loop"] = 1
#         settings["NFMModSettings"]["cwKeyer"]["mode"] = 1  # text
#         settings["NFMModSettings"]["modAFInput"] = 4  # CW text
# 
#         r = callAPI("/deviceset/1/channel/0/settings", "PATCH", None, settings, "Change NFM mod")
#         if r is None:
#             exit(-1)

#     except Exception as ex:
#         tb = traceback.format_exc()
#         print >> sys.stderr, tb


if __name__ == "__main__":
    while True:
        set_freq(int(105.3e6))
        time.sleep(2)
        set_freq(int(104.7e6))
        time.sleep(2)

```
</details>
