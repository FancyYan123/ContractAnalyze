# -*- coding = utf-8 -*-
from flask import Flask, request, abort
from flask_restful import Resource, Api
import json
from helper import *
from rules import analyze

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

app = Flask(__name__)
api = Api(app)
Debug = True


class ContractMailbox(Resource):
    def post(self):
        contract_data = json.loads(request.get_data())
        # 解析请求中用户自己选择的字段
        company_name = contract_data['company_name']
        loan_consistent_with_actual = contract_data['loan_consistent_with_actual']
        fake_advertising = contract_data['fake_advertising']

        # 如果用户直接上传的合同文本，直接分析文本
        if contract_data["type"] == 'text':
            # TODO: analyze all_text using detecting rules
            return_obj = analyze(contract_data['text_data'],
                                 company_name,
                                 loan_consistent_with_actual,
                                 fake_advertising, 'text')
            return json.dumps({'result': True, 'reason': '', 'return_object': return_obj})

        # 如果上传的合同图片，先使用腾讯云OCR进行文本提取再分析
        # 图片以base64编码
        elif contract_data["type"] == 'image':
            try:
                text = ''
                for image_data in contract_data['image_base64_data']:
                    cred = credential.Credential("AKIDqvmSxs0v4QaV9ESpPjqtgBrHTO6c8ugV",
                                                 "lMiqZ1IKL7mFXWBZr65pIVWM1RlobGgt")
                    httpProfile = HttpProfile()
                    httpProfile.endpoint = "ocr.tencentcloudapi.com"

                    clientProfile = ClientProfile()
                    clientProfile.httpProfile = httpProfile
                    client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

                    req = models.GeneralBasicOCRRequest()
                    if Debug:
                        params = '{"ImageBase64":"%s"}' % (str(get_image_base64())[2:-1])
                    else:
                        params = '{"ImageBase64":"%s"}' % (str(image_data))
                    req.from_json_string(params)

                    resp = client.GeneralBasicOCR(req)
                    for each in resp.TextDetections:
                        text += each.DetectedText

                # TODO: analyze all_text using detecting rules
                return_obj = analyze(text,
                                     company_name,
                                     loan_consistent_with_actual,
                                     fake_advertising, 'image')
                return json.dumps({'result': True, 'reason': '', 'return_object': return_obj})

            except TencentCloudSDKException as err:
                return json.dumps({'result': False, 'reason': err.get_message(), 'return_object': None})

        # 未知请求，返回报错信息
        else:
            return json.dumps({'result': False, 'reason': 'Unknown data type, you can choose either "text" or "image". ', 'return_object': None})

    def get(self):
        return "You are trying to use GET to visit here. Why not try POST. "


api.add_resource(ContractMailbox, '/contract/analyze')


if __name__ == '__main__':
    app.run(debug=True)
