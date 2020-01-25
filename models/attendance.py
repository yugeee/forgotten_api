import pymysql.cursors
from util.db import get_connection

class Attendance:

    weekday_ja = ['日', '月', '火', '水', '木', '金', '土']

    # constructor
    def __init__(self, date = "", user_id = "", weekday = "", summary = "", holiday = "", start_time = "", end_time = "", rest_time = "", work_time = ""):
        self.conn       = get_connection()
        self.date       = date
        self.user_id    = user_id
        self.weekday    = weekday
        self.summary    = summary
        self.holiday    = holiday
        self.start_time = start_time
        self.end_time   = end_time
        self.rest_time  = rest_time
        self.work_time  = work_time

    #  ユーザIDと年月で勤怠情報を取得
    def get_by_year_month(self, user_id, year, month):

        # 返却値初期化
        attendances = []
        work_time_total = "00:00"

        year_month = "%s-%s" % (year, month)

        # 勤怠一覧取得
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM attendance WHERE user_id = %s AND date LIKE %s"
                cursor.execute(sql, (user_id, "%s%%" % year_month))
                results = cursor.fetchall()
        finally:
            self.conn.close()

        if not results:
            return [], work_time_total

        for result in results:
            #  勤怠クラスをリストに入れる
            attendance = Attendance(
                date=result['date'],
                user_id=result['user_id'],
                weekday=Attendance.weekday_ja[result['weekday']],
                summary=result['summary'],
                holiday=result['holiday'],
                start_time=result['start_time'],
                end_time=result['end_time'],
                rest_time=result['rest_time'],
                work_time=result['work_time']
                )
            attendances.append(attendance)

        work_time_total = self.sum_work_time(attendances)

        return attendances, work_time_total

    # 勤怠情報を保存
    def save(self):

        # 勤怠の存在チェック
        check = self.check_attendance(self.user_id, self.date)

        try:
            with self.conn.cursor() as cursor:

                # 曜日は数字に変換しておく
                weekday = self.weekday_ja.index(self.weekday)

                # 勤怠がなかった場合はinsertする
                if not check:
                    # insert
                    sql = "INSERT INTO attendance (`date`, `user_id`, `weekday`, `summary`, `holiday`, `start_time`, `end_time`, `rest_time`, `work_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.date, self.user_id, weekday, self.summary, self.holiday, self.start_time, self.end_time, self.rest_time, self.work_time))
                    self.conn.commit()
                else:
                    # update
                    sql = "UPDATE attendance SET `date`= %s, `user_id`= %s, `weekday`= %s, `summary`= %s, `holiday`= %s, `start_time`= %s, `end_time`= %s, `rest_time`= %s, `work_time`= %s WHERE user_id = %s AND date = %s"
                    cursor.execute(sql, (self.date, self.user_id, weekday, self.summary, self.holiday, self.start_time, self.end_time, self.rest_time, self.work_time, self.user_id, self.date))
                    self.conn.commit()
        finally:
            self.conn.close()
        

    # 勤怠の存在チェック
    def check_attendance(self, user_id, date):
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM attendance WHERE user_id = %s AND date = %s"
            cursor.execute(sql, (user_id, date))
            result = cursor.fetchone()

            if not result:
                return False

            return True

    #  勤務時間を算出
    def sum_work_time(self, attendances):

        seconds = 0

        for attendance in attendances:
            
            work_time = attendance.work_time

            work_time_arr = work_time.split(':')

            hour = int(work_time_arr[0]) * 60 * 60
            minute = int(work_time_arr[1]) * 60

            seconds += hour + minute

        hour_sum = round(seconds / 3600)

        minute_sum = str(round( (seconds - (hour_sum * 60 * 60)) / 60)).zfill(2)

        return str(hour_sum) + ":" + minute_sum