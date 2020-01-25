import datetime
import sys
import hashlib
from flask import Blueprint, session, request, jsonify, abort, escape
from models.fare_master import Fare_Master
from json import JSONDecodeError

fare_masters = Blueprint("fare_masters", __name__, url_prefix='/api/fare_masters')

#  保存されている運賃マスタ情報を取得する
@fare_masters.route('/', methods=['GET'])
def get():


    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    fare_master_model = Fare_Master()

    try:
        # 運賃マスタ取得
        fare_masters = fare_master_model.get(user["id"])
        
        # 運賃マスタリストを作成してjson化して返却
        fare_masters_dicts = __fare_masters_to_dicts(fare_masters)

        return jsonify(fare_masters_dicts)

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})

    
#  運賃マスタを辞書へ変換
def __fare_masters_to_dicts(fare_masters):
    
    # 空はすぐ返す
    if not fare_masters:
        return []

    dicts = []

    for fare_master in fare_masters:
        
        fare_master_dict = {
                    "fare_master_id": fare_master.fare_master_id,
                    "user_id":        fare_master.user_id,
                    "purpose":        fare_master.purpose,
                    "transportation": fare_master.transportation,
                    "departure":      fare_master.departure,
                    "arrival":        fare_master.arrival,
                    "round_trip":     fare_master.round_trip,
                    "fare":           fare_master.fare
        }

        dicts.append(fare_master_dict)
    
    return dicts

    #  運賃マスタを保存する
@fare_masters.route('/', methods=['POST'])
def save():

    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})

    # リクエストボディがなかった場合
    if not request.json:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    try:
        for req in request.json:

            fare_master = Fare_Master(
                fare_master_id=req['fare_master_id'] if req['fare_master_id'] else set_id(oneday["user_id"], oneday["date"], oneday["purpose"]),
                user_id=req['user_id'],
                purpose=req['purpose'],
                transportation=req['transportation'],
                departure=req['departure'],
                arrival=req['arrival'],
                round_trip=req['round_trip'],
                fare=req['fare']
            )

            fare_master.save()

        return jsonify({})

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})