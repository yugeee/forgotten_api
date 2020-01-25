import sys
from flask import Blueprint, session, request, jsonify, abort
from models.user import User
from json import JSONDecodeError

login = Blueprint("login", __name__)

# ログイン実行
@login.route('/api/login/', methods=['POST'])
def exec_login():

    # params
    id = request.form['id'] if 'id' in request.form else ""
    pw = request.form['pass'] if 'pass' in request.form else ""

    try:
        # ログイン実行
        status, result = User.exec_login(User, id, pw)

        # ログイン失敗はメッセージ返却
        if status != 200:
            return jsonify(result)

        # 200だった場合はセッション開始
        user = {
            'id':    result.id,
            'name':  result.name,
            'mail':  result.mail,
            'token': result.token,
        }

        session['user'] = []
        session['user'] = user

        return jsonify(user)

    except JSONDecodeError:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})