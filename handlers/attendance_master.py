import sys
from flask import Blueprint, session, request, jsonify, abort, escape
from models.attendance_master import Attendance_Master
from json import JSONDecodeError

attendance_master = Blueprint("attendance_master", __name__, url_prefix='/api/attendance_master')

#  勤怠マスタを取得
@attendance_master.route('/', methods=['GET'])
def get():

    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    try:
        attendance_master_model = Attendance_Master()
        attendance_master = attendance_master_model.get_by_id(user["id"])

        return jsonify({
            "user_id":    attendance_master.user_id,
            "summary":    attendance_master.summary,
            "start_time": attendance_master.start_time,
            "end_time":   attendance_master.end_time,
            "rest_time":  attendance_master.rest_time,
            "work_time":  attendance_master.work_time,
            })

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})

@attendance_master.route('/', methods=['POST'])
def post():

    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    # リクエストボディがなかった場合
    if not request.json:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    try:
        attendance_master_model = Attendance_Master(
            user_id    = user["id"],
            summary    = request.json["summary"],
            start_time = request.json["start_time"],
            end_time   = request.json["end_time"],
            rest_time  = request.json["rest_time"],
            work_time  = request.json["work_time"],
        )
        
        attendance_master_model.save()

        # 空配列を返却
        return jsonify({})

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})