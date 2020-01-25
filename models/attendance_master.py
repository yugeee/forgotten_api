import pymysql.cursors
from util.db import get_connection

class Attendance_Master:

    # constructor
    def __init__(self, user_id = "", summary = "", start_time = "", end_time = "", rest_time = "", work_time = ""):
        self.conn       = get_connection()
        self.user_id    = user_id
        self.summary    = summary
        self.start_time = start_time
        self.end_time   = end_time
        self.rest_time  = rest_time
        self.work_time  = work_time
        
    #  ユーザIDで勤怠マスタを取得
    def get_by_id(self, user_id):

        # 勤怠マスタ取得
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM attendance_master WHERE user_id = %s"
                cursor.execute(sql, user_id)
                result = cursor.fetchone()
        finally:
            self.conn.close()

        # 勤怠マスタがない場合はデフォルト値をセット
        if not result:
            return Attendance_Master(
                user_id=user_id,
                summary="作業",
                start_time="09:00",
                end_time="18:00",
                rest_time="01:00",
                work_time="08:00"
            )
            
        #  勤怠マスタを返却
        return Attendance_Master(
            user_id=result['user_id'],
            summary=result['summary'],
            start_time=result['start_time'],
            end_time=result['end_time'],
            rest_time=result['rest_time'],
            work_time=result['work_time']
        )

    #  ユーザIDで勤怠マスタを取得
    def save(self):

        # 勤怠の存在チェック
        check = self.check_attendance_master(self.user_id)

        # 勤怠マスタ取得
        try:
            with self.conn.cursor() as cursor:

                # 勤怠がなかった場合はinsertする
                if not check:
                    # insert
                    sql = "INSERT INTO attendance_master (`user_id`, `summary`, `start_time`, `end_time`, `rest_time`, `work_time`) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.user_id, self.summary, self.start_time, self.end_time, self.rest_time, self.work_time))
                    self.conn.commit()
                else:
                    # update
                    sql = "UPDATE attendance_master SET `user_id`= %s, `summary`= %s, `start_time`= %s, `end_time`= %s, `rest_time`= %s, `work_time`= %s WHERE user_id = %s"
                    cursor.execute(sql, (self.user_id, self.summary, self.start_time, self.end_time, self.rest_time, self.work_time, self.user_id))
                    self.conn.commit()
        finally:
            self.conn.close()

    # 勤怠マスタの存在チェック
    def check_attendance_master(self, user_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM attendance_master WHERE user_id = %s"
            cursor.execute(sql, user_id)
            result = cursor.fetchone()

            if not result:
                return False

            return True
