import datetime
import sys
from flask import Blueprint, session, request, jsonify, abort, escape
from models.fare import Fare
from models.attendance import Attendance
from util.pdf import write_attendance_pdf,write_fare_pdf
from util.mail import send_mail
from json import JSONDecodeError

submit = Blueprint("submit", __name__, url_prefix='/api/submit')

#   年と月を指定、勤怠と交通費をPDFにしてメール提出
@submit.route('/<int:year>/<int:month>/', methods=['POST'])
def submit_by_year_month(year, month):


    if not 'user' in session:
        # TODO エラーメッセージ abort
        return jsonify({})
    
    user = session['user']

    fare_model = Fare()
    attendance_model = Attendance()
    
    #  文字列にして右寄せ2桁までを0埋めする 2 -> 02
    month = str(month).zfill(2)

    try:
        # 勤怠取得
        attendances, work_time_total = attendance_model.get_by_year_month(user["id"], year, month)

        # 運賃取得
        fares, fare_total = fare_model.get_by_year_month(user["id"], year, month)

        # 勤怠情報をPDF化
        attendance_pdf_path = write_attendance_pdf(user, year, month, attendances, work_time_total)

        #  運賃情報をPDF化
        fare_pdf_path = write_fare_pdf(user, year, month, fares, fare_total)

        send_mail(user, attendance_pdf_path, fare_pdf_path)

        if not attendances or not fares:
            return jsonify({})


        return "1"

    except Exception:
        print(sys.exc_info())
        return abort(500, {'error': "エラーが起きました。"})