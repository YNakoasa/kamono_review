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

# LINEからのWebhook (メッセージ)を受け取るエンドポイント
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature'] 
    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名検証を行い、問題なければhandleに定義されている関数を実行
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        # 署名検証に失敗した場合はエラーを返す
        abort(400)
    return 'OK'

# メッセージイベントを処理するハンドラー
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # ユーザーから送られてきたメッセージの取得
    user_message = event.message.text

    # ここにボットの応答ロジックを記述
    # まずはオウム返しから始めてみましょう
    reply_message = f"「{user_message}」と送ってきましたね！"

    # ユーザーに返信メッセージを送信
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# アプリケーションの起動
if __name__ == "__main__":
    # Flaskアプリケーションをローカルで実行
    # 本番環境ではGunicornなどのWSGIサーバーを使用する
    app.run(port=8000)