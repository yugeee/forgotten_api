from flask import Flask, session, request, jsonify
from pprint import pprint

import pymysql
from util.val import validate_post
from util.mail import send_mail
from util.pdf import write_pdf

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま

def getConnection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='forgotten',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
    )

@app.route('/hello/', methods=['POST', 'GET'])
def hello():

    db = getConnection()
    cur = db.cursor()
    sql = "select * from fare_master"
    cur.execute(sql)
    fm = cur.fetchall()
    cur.close()
    db.close()

    #param = request.form['post'] if request.form['post'] else "POST?"


    #if 'input' in session:
    #    res = {'input':session['input']}

        # セッション破棄
    #    session.pop('input', None)
    #    return jsonify(res)
 
    errors = validate_post(request.form)

    #session['input'] = request.form['post']

    if errors:
        return jsonify(errors)

    data = [
        {"name":"ゆげ"},
        {"age":27}
    ]

    pdf_path = write_pdf(request.form['post'])

    send_mail(request.form['post'], pdf_path)

    return jsonify({
            'status':'OK',
            'data':data,
            'fm':fm,
            'req':request.form['post'],
        })

# セッションを使うための秘密鍵
app.secret_key = 'SIJOIpwijef'

## おまじない
if __name__ == "__main__":
    app.run(debug=True)