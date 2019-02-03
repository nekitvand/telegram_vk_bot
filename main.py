from flask import Flask
from flask import request
from flask import jsonify
from flask import json
import requests


from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

telegram_bot = "55555555555555555555555555" # токен вашего бота
name_group = "@AAAAAAAAAA" # название вашего канала\группы
URL = f'https://api.telegram.org/bot{telegram_bot}/' # полная ссылка на обращение к телеграмм боту
vk_access_token = "555555555555555555555555" # сервисый клюк вашей группы в вк (узнать через апи приложение)
vk_owner_id = "-555555555" # номер вашего api приложения
vk_version_api = "5.92" # версия api к которому обращаетесь
count_posts = "20" # выводимое кол-во постов за раз

def write_json(data, filename='answer.json'):
    """Метод считывает json от телеги"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id , text):
    """Метод отсылает сообщение в чат"""
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url , json=answer)
    return r.json()

def vk_wall_get():
    """Метод получает посты со стены"""
    url_vk = "https://api.vk.com/method/wall.get"
    params =  {f"access_token":{vk_access_token},"owner_id":{vk_owner_id},"v":{vk_version_api},"count":{count_posts}}
    r = requests.get(url_vk,params=params).json()
    wall_post = r['response']['items'][0]['text']
    return wall_post


@app.route(f'/{telegram_bot}', methods=['POST', 'GET'])
def index():
    """Считывает данные приходящие с телеги и отправляет по команде боту"""
    if request.method == 'POST':
              r = request.get_json()
              chat_id = r['message']['chat']['id']
              message = r['message']['text']
              if "post" in message:
                  first_group_post = vk_wall_get()
                  send_message(chat_id=name_group, text=first_group_post)
              return jsonify(r)
    return '<h1>Hello my friend!</h1>'



if __name__ == '__main__':
    app.run()
