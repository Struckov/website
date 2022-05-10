import requests

img_data = requests.get('https://avatars.mds.yandex.net/i?id=858a1245dfd640d10b90535eb630b46b-5669136-images-thumbs&n=13').content
with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)