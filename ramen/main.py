#これが開発の核となるファイルです
# 必要なライブラリをインポート
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ラーメン屋のデータ
RAMEN_SHOPS = [
    {"name": "魂心家",
     "area": "〒920-0064 石川県金沢市南新保町ト２３−１",
     "type": "家系",
     "price_range": "830-1130円",
     "toppings": ["チャーシュー", "ほうれん草", "海苔", "ネギ", "野菜盛り", "味玉", "うずら"],
     "map_url": "https://www.google.com/maps/place/%E6%A8%AA%E6%B5%9C%E5%AE%B6%E7%B3%BB%E3%83%A9%E3%83%BC%E3%83%A1%E3%83%B3+%E9%87%91%E6%B2%A2+%E9%AD%82%E5%BF%83%E5%AE%B6/@36.5947142,136.6356219,17z/data=!3m1!4b1!4m6!3m5!1s0x5ff9cccc1b7bf9f1:0x23df69073d72f517!8m2!3d36.5947142!4d136.6356219!16s%2Fg%2F11byx84tzn?authuser=0&hl=ja&entry=ttu&g_ep=EgoyMDI1MDcwNi4wIKXMDSoASAFQAw%3D%3D"},
    # 他のラーメン屋はあとで順次追加していく
     ]

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

# handle_message関数がいつ動くか。この場合メッセージが届いた（MessageEvent）かつテキストである（message=Textmessage）とき実行する
@handler.add(MessageEvent, message=TextMessage)
# 実際に関数が実行される。eventという箱にユーザーからのメッセージ情報が入る
# ユーザーが送った具体的なメッセージをeventから取り出し、user_messageに格納し、メッセージを小文字に変換。検索で大文字小文字を区別しないようにするため
def handle_message(event):
    user_message = event.message.text.lower()  
    # 返信メッセージの初期値がこれ。お店が見つからなかった場合は魂心家をおすすめするゾ
    reply_message = f"それなら、魂心家がおすすめです"

    found_shops = []

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
    
