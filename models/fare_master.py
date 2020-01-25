import pymysql.cursors
from util.db import get_connection

class Fare_Master():

    # constructor
    def __init__(self, fare_master_id = "", user_id = "", purpose = "", transportation = "", departure = "", arrival = "", round_trip = "", fare = ""):
        self.conn           = get_connection()
        self.fare_master_id = fare_master_id
        self.user_id        = user_id
        self.purpose        = purpose
        self.transportation = transportation
        self.departure      = departure
        self.arrival        = arrival
        self.round_trip     = round_trip
        self.fare           = fare

    #  ユーザIDと運賃マスタを取得
    def get(self, user_id):

        # 運賃マスタ取得
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM fare_master WHERE user_id = %s "
                cursor.execute(sql, user_id)
                results = cursor.fetchall()
        finally:
            self.conn.close()

        if not results:
            return []

        fare_masters = []

        for result in results:

            #  運賃マスタをリストに入れる
            fare_master = Fare_Master(
                fare_master_id=result['fare_master_id'],
                user_id=result['user_id'],
                purpose=result['purpose'],
                transportation=result['transportation'],
                departure=result['departure'],
                arrival=result['arrival'],
                round_trip=result['round_trip'],
                fare=result['fare']
                )
            fare_masters.append(fare_master)

        return fare_masters

    #  運賃マスタを保存
    def save(self):

        # 存在チェック
        check = self.check_fare_master(self.fare_master_id)
        
        try:
            with self.conn.cursor() as cursor:

                # 勤怠がなかった場合はinsertする
                if not check:
                    # insert
                    sql = "INSERT INTO fare_master (`fare_master_id`, `user_id`, `purpose`, `transportation`, `departure`, `arrival`, `round_trip`, `fare`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.fare_master_id, self.user_id, self.purpose, self.transportation, self.departure, self.arrival, self.round_trip, self.fare))
                    self.conn.commit()
                else:
                    # update
                    sql = "UPDATE fare_master SET `fare_master_id`= %s, `user_id`= %s, `purpose`= %s, `transportation`= %s, `departure`= %s, `arrival`= %s, `round_trip`= %s, `fare`= %s WHERE fare_master_id = %s"
                    cursor.execute(sql, (self.fare_master_id, self.user_id, self.purpose, self.transportation, self.departure, self.arrival, self.round_trip, self.fare, self.fare_master_id))
                    self.conn.commit()
                    print(sql)
        finally:
            self.conn.close()
        

    # 運賃マスタの存在チェック
    def check_fare_master(self, fare_master_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM fare_master WHERE fare_master_id = %s"
            cursor.execute(sql, fare_master_id)
            result = cursor.fetchone()

            if not result:
                return False

            return True