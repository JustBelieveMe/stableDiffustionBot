import base64
import requests
import json
import io
import os
import sys
import logging
from PIL import Image, UnidentifiedImageError
logging.basicConfig(level=logging.INFO)

class SDConnecter():
    def __init__(self):
        self.jsonInit()
        self.sd_urlInit()
        self.checkSD()
        self.samplerHandler()
        self.sdModelHandler()
        self.sdOptionHandler()

    def jsonInit(self):
        with open("./jsonfile/t2ipayload.json", "r") as t2ipayloadFile:
            self.t2ipayloadJson = json.load(t2ipayloadFile)

        with open("./jsonfile/i2ipayload.json", "r") as i2ipayloadFile:
            self.i2ipayloadJson = json.load(i2ipayloadFile)
        
        with open("./jsonfile/t2idefaultPara.json", "r") as t2idefaultParaFile:
            self.t2idefaultPara = json.load(t2idefaultParaFile)

        with open("./jsonfile/i2idefaultPara.json", "r") as i2idefaultParaFile:
            self.i2idefaultPara = json.load(i2idefaultParaFile)

    def sd_urlInit(self, baseUrl = "http://localhost:8411"):
        self.url_base = baseUrl
        self.sdapi = f"{self.url_base}/sdapi/v1"
        self.url_txt2img = f"{self.sdapi}/txt2img"
        self.url_img2img = f"{self.sdapi}/img2img"
        self.url_sampler = f"{self.sdapi}/samplers"
        self.url_sdModelList = f"{self.sdapi}/sd-models"
        self.url_options = f"{self.sdapi}/options"

    def checkSD(self):
        try:
            response = requests.get(self.url_base)
            if response.status_code == requests.codes.ok:
                logging.info("Stable diffusion webui service code 200: ok!")
        except requests.exceptions.ConnectionError:
            logging.error("ERROR: Stable diffusion webui service is not available")
            sys.exit()
        except ConnectionRefusedError:
            logging.error("ERROR: Stable diffusion webui service refuse connection")
            sys.exit()
        return True

    def samplerHandler(self):
        if self.checkSD():
            response = requests.get(self.url_sampler)
            self.sampler = dict()
            for sample_method in response.json():
                self.sampler[sample_method['name']] = 0     

    def sdModelHandler(self):
        if self.checkSD():
            response = requests.get(self.url_sdModelList)
            self.sdModels = dict()
            for sd_model in response.json():
                self.sdModels[sd_model['model_name']] = 0

    def sdOptionHandler(self):
        if self.checkSD():
            response = requests.get(self.url_options)
            self.sdoptions = response.json()
            self.currModelName = self.sdoptions["sd_model_checkpoint"]

    async def easyt2iPaint(self, prompt):
        self.t2ipayloadJson["prompt"] = prompt
        self.t2ipayloadJson["negative_prompt"] = self.t2idefaultPara["negative_prompt"]
        self.t2ipayloadJson["sampler_name"] = self.t2idefaultPara["sampler_name"]
        self.t2ipayloadJson["sampler_index"] = self.t2idefaultPara["sampler_index"]
        self.t2ipayloadJson["batch_size"] = self.t2idefaultPara["batch_size"]
        self.t2ipayloadJson["cfg_scale"] = self.t2idefaultPara["cfg_scale"]
        self.t2ipayloadJson["width"] = self.t2idefaultPara["width"]
        self.t2ipayloadJson["height"] = self.t2idefaultPara["height"]
        self.t2ipayloadJson["steps"] = self.t2idefaultPara["steps"]

        return self.txt2img(self.t2ipayloadJson)

    async def detailt2iPaint(self, detailJson):
        self.t2ipayloadJson["prompt"] = detailJson["prompt"]
        self.t2ipayloadJson["negative_prompt"] = detailJson["negative_prompt"]
        self.t2ipayloadJson["sampler_name"] = detailJson["sampler"]
        self.t2ipayloadJson["sampler_index"] = detailJson["sampler"]
        self.t2ipayloadJson["width"] = detailJson["width"]
        self.t2ipayloadJson["height"] = detailJson["height"]
        self.t2ipayloadJson["cfg_scale"] = detailJson["CFG"]

        self.t2ipayloadJson["batch_size"] = self.t2idefaultPara["batch_size"]
        self.t2ipayloadJson["steps"] = self.t2idefaultPara["steps"]
        
        return self.txt2img(self.t2ipayloadJson)
        
    def txt2img(self, jsonData):
        response = requests.post(self.url_txt2img, json = jsonData)
        imgList = list()
        for base64_img in response.json()['images']:
            imgList.append(self.decodeBase64(base64_img))
        return imgList
    
    async def easyi2iPaint(self, jsonData, url):
        self.i2ipayloadJson["init_images"][0] = self.getImageFromUrl(url)
        self.i2ipayloadJson["prompt"] = jsonData["prompt"]
        self.i2ipayloadJson["width"] = jsonData["width"]
        self.i2ipayloadJson["height"] = jsonData["height"]
        self.i2ipayloadJson["denoising_strength"] = jsonData["denoising_strength"]

        self.i2ipayloadJson["negative_prompt"] = self.i2idefaultPara["negative_prompt"]
        self.i2ipayloadJson["sampler_name"] = self.i2idefaultPara["sampler_name"]
        self.i2ipayloadJson["sampler_index"] = self.i2idefaultPara["sampler_index"]
        self.i2ipayloadJson["cfg_scale"] = self.i2idefaultPara["cfg_scale"]
        self.i2ipayloadJson["batch_size"] = self.i2idefaultPara["batch_size"]
        self.i2ipayloadJson["steps"] = self.i2idefaultPara["steps"]
        return self.img2img(self.i2ipayloadJson)

    async def detaili2iPaint(self, jsonData, url):
        self.i2ipayloadJson["init_images"][0] = self.getImageFromUrl(url)
        self.i2ipayloadJson["denoising_strength"] = jsonData["denoising_strength"]

        self.i2ipayloadJson["prompt"] = jsonData["prompt"]
        self.i2ipayloadJson["negative_prompt"] = jsonData["negative_prompt"]
        self.i2ipayloadJson["sampler_name"] = jsonData["sampler"]
        self.i2ipayloadJson["sampler_index"] = jsonData["sampler"]
        self.i2ipayloadJson["width"] = jsonData["width"]
        self.i2ipayloadJson["height"] = jsonData["height"]
        self.i2ipayloadJson["cfg_scale"] = jsonData["CFG"]

        self.i2ipayloadJson["batch_size"] = self.i2idefaultPara["batch_size"]
        self.i2ipayloadJson["steps"] = self.i2idefaultPara["steps"]

        return self.img2img(self.i2ipayloadJson)
    
    def img2img(self, jsonData):
        jsonData["init_images"] = [self.encodeBase64(jsonData["init_images"][0]).decode('utf-8')]
        response = requests.post(self.url_img2img, json = jsonData)
        if "error" in response.json():
            print(response.json())
        imgList = list()
        for base64_img in response.json()['images']:
            imgList.append(self.decodeBase64(base64_img))
        return imgList

    def changeSDModel(self, modelName):
        if self.checkSD():
            response = requests.post(self.url_options, json={"sd_model_checkpoint":modelName})
            self.currModelName = modelName
            logging.info(f"model change: {modelName}")

    def encodeBase64(self, image_io):
        encode_image = base64.b64encode(image_io.getvalue())
        return encode_image

    def decodeBase64(self, base64_img):
        decoded_image = base64.b64decode(base64_img)
        image_io = io.BytesIO(decoded_image)
        return image_io
    
    def getImageFromUrl(self, url):
        response = requests.get(url)
        image_io = io.BytesIO(response.content)
        return image_io
    
    def checkImage(self, byteioObj, height_limit=1024, width_limit=1024):
        try:
            width, height = Image.open(byteioObj).size
            if width > width_limit or width < 0 or height > height_limit or height < 0:
                return [1, width, height]
        except UnidentifiedImageError:
            return [2]
        else:
            return [0, width, height]

    def getSampler(self):
        return self.sampler.keys()

    def gett2iPayload(self):
        return self.t2ipayloadJson
    
    def geti2iPayload(self):
        return self.i2ipayloadJson

    def getSDmodel(self):
        return self.sdModels.keys()

    def getCurrModelName(self):
        return self.currModelName

    def getOptions(self):
        return self.sdoptions