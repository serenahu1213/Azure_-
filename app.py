from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
    )
from linebot.exceptions import (
    InvalidSignatureError
    )
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
    )
import tempfile, os, random, string
from datetime import datetime
from config import *
from imgur_upload import *
# upload(client_data, local_img_file, album_id, name, title )

import emotion as e
import sqlite3
import randomselect as r


app = Flask(__name__)

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

image_tmp_path = os.path.join(os.getcwd(), 'static')


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



@handler.add(MessageEvent, message=(TextMessage,ImageMessage))
def handle_message(event):
    if event.message.type=='image':
        connect = sqlite3.connect('linedata.db')
        cursor = connect.cursor()
        # base on Line_bot_api website example
        message_content = line_bot_api.get_message_content(event.message.id)
        image_name = ''.join(random.choice(string.ascii_letters + string.digits) for A in range(8)) + '.jpg'
        image_path = image_tmp_path + '\\' + image_name
        
        user_id = event.source.user_id
        user_name = line_bot_api.get_profile(user_id).display_name
        
        with open(image_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
        try:  
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            image = upload(client, image_path, album_id, image_name.split('.')[0], ''.join(['Image Name ', image_name.split('.')[0]]))
            print(f"Imgur URL : {image['link']}")
            print(user_id)
            os.remove(image_path)
            emotion = e.emotion(image['link'])
            print(emotion)
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text = f'猜測您現在的心情是{emotion}'),
                TextSendMessage(text = '您想要來首歌還是詩?')])        
            
            rows = cursor.execute("SELECT * FROM emotion where user_id = ?", (user_id,))
            found = False
            for data in rows : 
                cursor.execute("UPDATE emotion \
                        SET emotion = ? \
                        WHERE user_id = ? ", (emotion, user_id))
                connect.commit()
                found =  True
            if found == False : 
                cursor.execute("INSERT INTO emotion(user_id, emotion) \
                    VALUES (?,?)",(user_id,emotion))
                connect.commit()

        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = '表情辨識失敗QQ，請上傳一張清晰個人照片'))
        return 0
    elif event.message.type=='text':
        user_id = event.source.user_id
        user_name = line_bot_api.get_profile(user_id).display_name
        msg = event.message.text
        connect = sqlite3.connect('linedata.db')
        cursor = connect.cursor()
        emotiondata = cursor.execute("SELECT * FROM emotion where user_id = ?", (user_id,))
        found = False
        for i in emotiondata:
            emotion = i[1]
        found = True
        recomm = r.result(emotion,msg)
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text = '為您推薦....'),
            TextSendMessage(text = f'{recomm[0]}'),
            TextSendMessage(text = f'{recomm[1]}')])                
    

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='12345')