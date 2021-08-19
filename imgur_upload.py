## upload image from local path, adjusted from imgurpython example
from imgurpython import ImgurClient
# import import_ipynb
from config import *
from datetime import datetime

def upload(client_data, local_img_file, album_id, name, title ):
    config = {
        'album':  album_id,
        'name': name,
        'title': title,
        'description': f'Upload-time : {datetime.now()}'
    }

    print("Uploading image... ")
    image = client_data.upload_from_path(local_img_file, config=config, anon=False)
    print("Done")

    return image


if __name__ == "__main__":
#     client_id ='YOUR CLIENT ID'
#     client_secret = 'YOUR CLIENT SECRET'
#     access_token = "YOUR ACCESS TOKEN"
#     refresh_token = "YOUR REFRESH TOKEN"
#     album = "YOUR ALBUM ID"
#     from ipynb.fs.full.config import *

    local_img_file = "./static/ZnfFPnTS.jpg"
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    image = upload(client, local_img_file, album_id,name='123',title='456')
    print(f"Imgur Url: {image['link']}")