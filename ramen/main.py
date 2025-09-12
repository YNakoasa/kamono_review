from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ラーメン屋のデータ
import csv #ラーメン屋情報いれたcsvファイルを読み込むためのやつ
CSV_FILE_PATH="ramen_list.csv"

def load_ramen_list_from_csv(file_path):
    ramen_shops = []
    try:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader: 
                if 'toppings' in row and row['toppings']:
                    row['toppings'] = [t.strip() for t in row['toppings'].split(',')]
                else:
                    row['toppings'] = []

                if 'notes' in row:
                    del row['notes']

                ramen_shops.append(row)
    except FileNotFoundError:
        print(f"エラー: CSVファイルが見つかりません。パスを確認してください: {file_path}")
    except Exception as e:
        print(f"エラー: CSVファイルの読み込み中に問題が発生しました: {e}")
    return ramen_shops

RAMEN_SHOPS = load_ramen_list_from_csv(CSV_FILE_PATH)


app = Flask(__name__)


CHANNEL_ACCESS_TOKEN = "d5OWpzpXaII/6zbgSs9VBvbtrhLXsxwu2XhG4wc0bOZVqtIEuqlm/s4wobWG8EYJQRc3U6r0DgB5S9RDelyeM7shusJBAJZaRTw0JBw5OdOsdcVzqhxmY3ncj4XzXos842Vw/wq2kmx0Nfe8CpzzdAdB04t89/1O/w1cDnyilFU=" # ここに取得したアクセストークンを貼り付ける
CHANNEL_SECRET = "fd4b9c96ec6bdc2a9c2ce53d6c8934d8" # ここに取得したチャンネルシークレットを貼り付ける

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature'] 
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

  # 返信メッセージの初期値がこれ。お店が見つからなかった場合は魂心家をおすすめする
    reply_message = f"それなら、魂心家がおすすめです"

    found_shops = []

    for shop in RAMEN_SHOPS:
        area_match = shop["area"].lower() in user_message
        type_match = shop["type"].lower() in user_message
        if area_match or type_match:
            found_shops.append(shop)

    if found_shops:
        reply_message = "以下のラーメン屋がおすすめです:\n\n"
        for shop in found_shops:
            reply_message += f"店名: {shop['name']}\n"
            reply_message += f"エリア: {shop['area']}\n"
            reply_message += f"種類: {shop['type']}\n"
            reply_message += f"価格帯: {shop['price_range']}\n"
            reply_message += "トッピング: " + ", ".join(shop["toppings"]) + "\n"
            reply_message += f"地図リンク: {shop['map_url']}\n\n"
    else:
        reply_message = "( ﾟДﾟ)"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# アプリケーションの起動
if __name__ == "__main__":
    # Flaskアプリケーションをローカルで実行
    # 本番環境ではGunicornなどのWSGIサーバーを使用する
    app.run(port=8000)
    
