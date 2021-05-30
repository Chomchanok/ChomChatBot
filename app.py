import os
from flask import Flask, request
from linebot.models import *
from linebot import *
import json
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

line_bot_api = LineBotApi(
    'b5jEOAKs0FHY3MkC1fBn/ghTXv0uJBNYDF4ae7FVoGA0OkMhXa3fRSMVEqGiCjArgHXvcUh0KN5P2u+eOn+6dBVt4gwGYRsx6+kwxg2qhjO0GXG8x+9xvNRNt475r91YmgJQCU4aEB1bHrLf2LeMigdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7d2e8f552de39ddd3f60099aa1e0f297')


@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)

    reply(intent, text, reply_token, id, disname)

    return 'OK'


# def reply1(intent, text, reply_token, id, disname):


def reply(intent, text, reply_token, id, disname):

    if intent == 'intent 5':
        text_message = TextSendMessage(text='ทดสอบสำเร็จ')
        line_bot_api.reply_message(reply_token, text_message)

    elif intent == 'findlocation':
        str = text.split()
        amp = str[0]
        tambol = str[1]
        data = requests.get('https://blockage.crflood.com/api/blockage/{}/{}'.format(amp, tambol))
        json_data = json.loads(data.text)
        num = len(json_data)
        blk_tumbol = json_data[0]['blockage_location']['blk_tumbol']
        message = 'สิ่งกีดขวางของตำบล{}\n'.format(blk_tumbol)
        for i in range(num):
            blk_code = json_data[i]['blk_code']
            blk_village = json_data[i]['blockage_location']['blk_village']
            river = json_data[i]['river']['river_name']+"/"+json_data[i]['river']['river_main']
            mess = '{}. รหัสสิ่งกีดขวาง: {} \n ลำน้ำ: {} \nที่อยู่ : {} \n' .format(
                i+1, blk_code, river, blk_village)
            message = message+"\n"+mess
            # text_message = TextSendMessage(text='{}. รหัสสิ่งกีดขวาง: {} \n ที่อยู่ : {} ต.{}\n' .format(i+1,blk_code,blk_village,blk_tumbol))
            # message.append(text_message)
        print(message)
        text_message = TextSendMessage(text=message)
        line_bot_api.reply_message(reply_token, text_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
