import base64
import requests
import json
import io
import sys
import logging
logging.basicConfig(level=logging.INFO)

class sdConnecter():
    def __init__(self):
        with open("./payload.json", "r") as payloadFile:
            self.payloadJson = json.load(payloadFile)
        
        with open("./defaultPara.json", "r") as defaultParaFile:
            self.defaultPara = json.load(defaultParaFile)
        self.sd_urlInit()
        self.checkSD()
        self.samplerHandler()
        self.sdModelHandler()
        self.sdOptionHandler()

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

    async def easyPaint(self, prompt):
        self.payloadJson["prompt"] = prompt
        self.payloadJson["negative_prompt"] = self.defaultPara["negative_prompt"]
        self.payloadJson["sampler_name"] = self.defaultPara["sampler_name"]
        self.payloadJson["sampler_index"] = self.defaultPara["sampler_index"]
        self.payloadJson["batch_size"] = self.defaultPara["batch_size"]
        self.payloadJson["cfg_scale"] = self.defaultPara["cfg_scale"]
        self.payloadJson["width"] = self.defaultPara["width"]
        self.payloadJson["height"] = self.defaultPara["height"]
        self.payloadJson["steps"] = self.defaultPara["steps"]

        return self.txt2img(self.payloadJson)

    async def detailPaint(self, detailJson):
        self.payloadJson["prompt"] = detailJson["prompt"]
        self.payloadJson["negative_prompt"] = detailJson["negative_prompt"]
        self.payloadJson["sampler_name"] = detailJson["sampler"]
        self.payloadJson["sampler_index"] = detailJson["sampler"]
        self.payloadJson["width"] = detailJson["width"]
        self.payloadJson["height"] = detailJson["height"]
        self.payloadJson["cfg_scale"] = detailJson["CFG"]

        self.payloadJson["batch_size"] = self.defaultPara["batch_size"]
        self.payloadJson["steps"] = self.defaultPara["steps"]
        
        return self.txt2img(self.payloadJson)
        
    def txt2img(self, jsonData):
        response = requests.post(self.url_txt2img, json = jsonData)
        imgList = list()
        for base64_img in response.json()['images']:
            imgList.append(self.parseBase64(base64_img))
        return imgList

    def changeSDModel(self, modelName):
        if self.checkSD():
            response = requests.post(self.url_options, json={"sd_model_checkpoint":modelName})
            self.currModelName = modelName
            logging.info(f"model change: {modelName}")

    def parseBase64(self, base64_img):
        Decoded_image = base64.b64decode(base64_img)
        image_ioObj = io.BytesIO(Decoded_image)
        return image_ioObj

    def getSampler(self):
        return self.sampler.keys()

    def getPayload(self):
        return self.payloadJson

    def getSDmodel(self):
        return self.sdModels.keys()

    def getCurrModelName(self):
        return self.currModelName

    def getOptions(self):
        return self.sdoptions