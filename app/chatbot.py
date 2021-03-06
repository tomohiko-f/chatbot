import os
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

from . import settings

app = Flask(__name__)

line_bot_api = LineBotApi(settings.channel_access_token)
handler = WebhookHandler(settings.channel_secret)


# @app.route("/")
# def test():
#     return "OK"

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
    # if event.message.text == "予定":
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="今日の予定はこれだよ、ほれっ")
    )


if __name__ == "__main__":
    app.run()