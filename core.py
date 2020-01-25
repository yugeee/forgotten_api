from flask import Flask, session, request, jsonify
from pprint import pprint

import pymysql
from util.val import validate_post
from util.mail import send_mail

from handlers.login import login
from handlers.attendances import attendances
from handlers.attendance_master import attendance_master
from handlers.fares import fares
from handlers.fare_masters import fare_masters
from handlers.submit import submit

# Flask本体
app = Flask(__name__)


# config
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま

# routing　hanlders配下のファイルがコントローラを担当
app.register_blueprint(login)
app.register_blueprint(attendances)
app.register_blueprint(attendance_master)
app.register_blueprint(fares)
app.register_blueprint(fare_masters)
app.register_blueprint(submit)

# セッションを使うための秘密鍵
app.secret_key = 'awoifdhja;sodvjqoirfh@'


# debug
if __name__ == "__main__":
    app.run(debug=True)