import datetime
import sys
from flask import Blueprint, session, request, jsonify, abort, escape
from models.attendance import Attendance
from models.calendar_api import Calendar_API
from models.attendance_master import Attendance_Master
from json import JSONDecodeError

attendances = Blueprint("attendances", __name__, url_prefix='/api/attendances')

#  保存されている勤怠情報を取得する
@attendances.route('/<int:year>/<int:month>/', methods=['GET'])
def get_by_year_month(year, month):


    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    attendance_model = Attendance()
    
    #  文字列にして右寄せ2桁までを0埋めする 2 -> 02
    month = str(month).zfill(2)

    try:
        # 勤怠取得
        attendances, work_time_total = attendance_model.get_by_year_month(user["id"], year, month)

        status = 200

        if len(attendances) == 0:
            status = 404

        # 勤怠リストを作成してjson化して返却
        attendances_dict = __attendances_to_dict(attendances)

        req = {
            'work_time_total':work_time_total,
            'attendances':attendances_dict
            }
        
        return jsonify(req), status

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})

# 勤怠クラスを辞書へ変換
def __attendances_to_dict(attendances):
    
    # 空はすぐ返す
    if not attendances:
        return []

    dicts = []

    for attendance in attendances:
        attendance_dict = {
                    "date":       attendance.date.strftime("%Y-%m-%d"),
                    "user_id":    attendance.user_id,
                    "weekday":    attendance.weekday,
                    "summary":    attendance.summary,
                    "holiday":    attendance.holiday,
                    "start_time": attendance.start_time,
                    "end_time":   attendance.end_time,
                    "rest_time":  attendance.rest_time,
                    "work_time":  attendance.work_time
        }

        dicts.append(attendance_dict)
    
    return dicts


#  新しい勤怠情報を取得する
@attendances.route('/new/<int:year>/<int:month>/', methods=['GET'])
def new(year, month):

    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    # 現在の年月を取得
    #now = datetime.date.today()
    #year = now.year
    #month = now.month

    try:
        # カレンダー情報を取得
        status, calendar = Calendar_API.get_calendar(year, month)

        # 取得失敗はメッセージ返却
        if status != 200:
            return jsonify(result)

        attendance_master_model = Attendance_Master()
        attendance_master = attendance_master_model.get_by_id(user["id"])

        new_attendance_dicts = __new_attendance_to_dict(calendar, attendance_master)

        req = {
            'work_time_total':"0:00",
            'attendances':new_attendance_dicts
        }

        return jsonify(req), 200

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})


# カレンダーと勤怠マスタを辞書へ変換
def __new_attendance_to_dict(calendar, attendance_master):
    
    # 空はすぐ返す
    if not calendar and attendance_master:
        return []

    dicts = []

    for oneday in calendar:
        attendance_dict = {
                    "date":       oneday["date"],
                    "user_id":    attendance_master.user_id,
                    "weekday":    oneday["weekday"],
                    "summary":    (
                        oneday["holiday"] if oneday["holiday"] else # 祝日はなんの日であるか入れる
                        "" if __is_holiday(oneday) else # 土日
                        attendance_master.summary
                    ),
                    "holiday":    (
                        #  土日祝は1をたてる
                        1 if __is_holiday(oneday) else
                        0),
                    "start_time": (
                        # 土日祝は 00:00 をセット
                        "00:00" if __is_holiday(oneday) else
                        attendance_master.start_time
                    ),
                    "end_time":   (
                        # 土日祝は 00:00 をセット
                        "00:00" if __is_holiday(oneday) else
                        attendance_master.end_time
                    ),
                    "rest_time":  (
                        # 土日祝は 00:00 をセット
                        "00:00" if __is_holiday(oneday) else
                        attendance_master.rest_time
                    ),
                    "work_time":  (
                        # 土日祝は 00:00 をセット
                        "00:00" if __is_holiday(oneday) else
                        attendance_master.work_time
                    )
        }

        dicts.append(attendance_dict)
    
    return dicts

# 休日であるかチェック
def __is_holiday(oneday):

    if oneday["weekday"] == '6' or oneday["weekday"] == '0' or oneday["holiday"]:
        return True
    
    return False


#  勤怠情報を保存する
@attendances.route('/', methods=['POST'])
def save():

    # リクエストボディがなかった場合
    if not request.json:
        # TODO エラーメッセージ abort
        return jsonify({})

    try:
        for oneday in request.json:

            attendance = Attendance(
                date       = oneday["date"], 
                user_id    = oneday["user_id"], 
                weekday    = oneday["weekday"], 
                summary    = oneday["summary"], 
                holiday    = oneday["holiday"], 
                start_time = oneday["start_time"], 
                end_time   = oneday["end_time"], 
                rest_time  = oneday["rest_time"], 
                work_time  = oneday["work_time"]
            )

            attendance.save()

        # 空配列を返却
        return jsonify([])
            
    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})