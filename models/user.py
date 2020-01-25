import requests
import json

class User:

    url = "http://localhost/api/v1/user/"

    # constructor
    def __init__(self, id, name, mail, token):
        self.id    = id
        self.name  = name
        self.mail  = mail
        self.token = token

    # APIを叩いてユーザー情報orエラーメッセージを取得
    @staticmethod
    def exec_login(self, id, pw):
        post = {
            'id'  : id,
            'pass': pw,
            }

        res = requests.post(self.url, data=post)

        # 200以外ならエラー
        if res.status_code != 200:
            return res.status_code, json.loads(res.text)

        # ユーザーを取得した場合
        res_json = json.loads(res.text)

        return res.status_code, User(
            res_json['id'],
            res_json['name'],
            res_json['mail'],
            res_json['token'],
        )


# debug
if __name__ == '__main__':
    User.exec_login(User, "yuge1111", "password")
    
