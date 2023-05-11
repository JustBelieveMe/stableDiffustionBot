import base64
import requests
import json
import io
import sys

class paintClass():
    def __init__(self):
        self.url_base = "http://localhost:8411"
        self.sdapi = f"{self.url_base}/sdapi/v1"
        self.url_txt2img = f"{self.sdapi}/txt2img"
        self.url_img2img = f"{self.sdapi}/img2img"
        self.url_sampler = f"{self.sdapi}/samplers"

        with open("./payload.json", "r") as payloadFile:
            self.payloadJson = json.load(payloadFile)
        
        with open("./defaultPara.json", "r") as defaultParaFile:
            self.defaultPara = json.load(defaultParaFile)

        self.samplerHandler()

    def samplerHandler(self):
        try:
            response = requests.get(self.url_sampler)
            self.sampler = list()
            for sample_method in response.json():
                self.sampler.append(sample_method['name'])
            return None
        except requests.exceptions.ConnectionError:
            print("ERROR: Stable diffusion webui service is not available")
            sys.exit()
        except ConnectionRefusedError:
            print("ERROR: Stable diffusion webui service refuse connection")
            sys.exit()
        except:
            print("something wrong....")
        else:
            print("sampler loading successfully")

    def easyPaint(self, prompt):
        self.payloadJson["prompt"] = prompt
        self.payloadJson["negative_prompt"] = self.defaultPara["negative_prompt"]
        self.payloadJson["sampler_name"] = self.defaultPara["sampler_name"]
        self.payloadJson["sampler_index"] = self.defaultPara["sampler_index"]
        self.payloadJson["batch_size"] = self.defaultPara["batch_size"]
        self.payloadJson["cfg_scale"] = self.defaultPara["cfg_scale"]
        self.payloadJson["width"] = self.defaultPara["width"]
        self.payloadJson["height"] = self.defaultPara["height"]

        return self.txt2img(self.payloadJson)

    def detailPaint(self, detailJson):
        self.payloadJson["prompt"] = detailJson["prompt"]
        self.payloadJson["negative_prompt"] = detailJson["ng_prompt"]
        self.payloadJson["sampler_name"] = detailJson["sampler"]
        self.payloadJson["sampler_index"] = detailJson["sampler"]
        self.payloadJson["width"] = detailJson["width"]
        self.payloadJson["height"] = detailJson["height"]
        self.payloadJson["cfg_scale"] = detailJson["CFG"]
        self.payloadJson["batch_size"] = self.defaultPara["batch_size"]
        
        return self.txt2img(self.payloadJson)
        
    def txt2img(self, jsonData):
        response = requests.post(self.url_txt2img, json = jsonData)
        imgList = list()
        for base64_img in response.json()['images']:
            imgList.append(self.parseBase64(base64_img))
        return imgList

    def parseBase64(self, base64_img):
        Decoded_image = base64.b64decode(base64_img)
        image_ioObj = io.BytesIO(Decoded_image)
        return image_ioObj

    def getSampler(self):
        return self.sampler

    def getPayload(self):
        return self.payloadJson