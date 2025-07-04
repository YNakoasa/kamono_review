#これが開発の核となるファイルです
# 必要なライブラリをインポート
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# LINE Botのチャンネルアクセストークンとチャンネルシークレットを環境変数から取得
# ここに実際の値を直接書くのはセキュリティ上推奨されません
# 後ほど、環境変数として設定することをお勧めします
CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN" # ここに取得したアクセストークンを貼り付ける
CHANNEL_SECRET = "YOUR_CHANNEL_SECRET" # ここに取得したチャンネルシークレットを貼り付ける

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)