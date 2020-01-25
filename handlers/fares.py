import datetime
import sys
from flask import Blueprint, session, request, jsonify, abort, escape
from models.fare import Fare
from util.common import set_id
from json import JSONDecodeError

fares = Blueprint("fares", __name__, url_prefix='/api/fares')

#  保存されている運賃情報を取得する
@fares.route('/<int:year>/<int:month>/', methods=['GET'])
def get_by_year_month(year, month):


    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    fare_model = Fare()
    
    #  文字列にして右寄せ2桁までを0埋めする 2 -> 02
    month = str(month).zfill(2)

    try:
        # 運賃取得
        fares, fare_total = fare_model.get_by_year_month(user["id"], year, month)

        if not fares:
            return 404, jsonify({})
        
        # 運賃リストを作成してjson化して返却
        fares_dict = __fares_to_dict(fares)

        req = {
            'fare_total':fare_total,
            'fares':fares_dict
            }

        return jsonify(req)

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})


#  運賃を辞書へ変換
def __fares_to_dict(fares):
    
    # 空はすぐ返す
    if not fares:
        return []

    dicts = []

    for fare in fares:
        
        fare_dict = {
                    "fare_id":        fare.fare_id,
                    "date":           fare.date,
                    "user_id":        fare.user_id,
                    "purpose":        fare.purpose,
                    "transportation": fare.transportation,
                    "departure":      fare.departure,
                    "arrival":        fare.arrival,
                    "round_trip":     fare.round_trip,
                    "fare":           fare.fare
        }

        dicts.append(fare_dict)
    
    return dicts


#  運賃情報を保存する
@fares.route('/', methods=['POST'])
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
        for oneday in request.json:

            fare = Fare(
                fare_id        = oneday["fare_id"] if oneday["fare_id"] else set_id(oneday["user_id"], oneday["date"], oneday["purpose"]), 
                date           = oneday["date"], 
                user_id        = oneday["user_id"] if oneday["user_id"] else user["id"],
                purpose        = oneday["purpose"], 
                transportation = oneday["transportation"], 
                departure      = oneday["departure"], 
                arrival        = oneday["arrival"], 
                round_trip     = oneday["round_trip"], 
                fare           = oneday["fare"]
            )

            fare.save()


        return jsonify({})

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})