import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from config import DING_TALK, IS_CONFIG_DINGTALK
from shared.logger import default_logger as logger


def generate_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret = secret
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return sign


def send_link_dingtalk(title, text, message_url):
    if IS_CONFIG_DINGTALK is False:
        print('没有配置钉钉机器人')
        logger.warn('没有配置钉钉机器人')
        return
    # 1. 定义请求的url
    DINGTALK_TOKEN = DING_TALK.get('token')
    DINGTALK_SECRET = DING_TALK.get('secret')
    url = (f"https://oapi.dingtalk.com/robot/send?"
           f"access_token={DINGTALK_TOKEN}"
           f"&timestamp={str(round(time.time() * 1000))}"
           f"&sign={generate_sign(DINGTALK_SECRET)}")
    # 2. 定义请求头
    headers = {
        'Content-Type': 'application/json'
    }
    # 3. 定义请求体
    data = {
        "msgtype": "link",
        "link": {
            "text": text,
            "title": title,
            "messageUrl": message_url
        }
    }
    # 4. 发送请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    return response.text


def send_message_dingtalk(content):
    if IS_CONFIG_DINGTALK is False:
        print('没有配置钉钉机器人')
        logger.warn('没有配置钉钉机器人')
        return
    # 1. 定义请求的url
    DINGTALK_TOKEN = DING_TALK.get('token')
    DINGTALK_SECRET = DING_TALK.get('secret')
    url = (f"https://oapi.dingtalk.com/robot/send?"
           f"access_token={DINGTALK_TOKEN}"
           f"&timestamp={str(round(time.time() * 1000))}"
           f"&sign={generate_sign(DINGTALK_SECRET)}")
    # 2. 定义请求头
    headers = {
        'Content-Type': 'application/json'
    }
    # 3. 定义请求体
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "代码片段变化",
            "text": content
        }
    }
    # 4. 发送请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
    return response.text
