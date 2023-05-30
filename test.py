import json
import requests
import io
import base64

from PIL import Image, PngImagePlugin
url = "http://127.0.0.1:5411"

payload = {
    "prompt":"1girl",
    "steps":5
}

response = requests.post(url=f"{url}/sdapi/v1/txt2img", json=payload)
r = response.json()
print(r)

# for i in r['images']:
#     image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

