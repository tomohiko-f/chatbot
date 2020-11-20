import os
import re
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from . import google_calender
from . import settings

app = Flask(__name__)

line_bot_api = LineBotApi(settings.channel_access_token)
handler = WebhookHandler(settings.channel_secret)


@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if re.search('予定|よてい', event.message.text)\
        and re.findall('教えて|知りたい|おしえて|しりたい|は？', event.message.text):
        calender = google_calender.GoogleCalender()
        events = calender.get_events()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="今日の予定はこれだよ、ほらよっ\n"\
                    + result["start"] + " " + result["summary"]
            )
        )


if __name__ == "__main__":
    app.run()