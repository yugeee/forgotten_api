import pymysql.cursors
from util.db import get_connection

class Fare():

    #round_trip_ja = ['片', '往']

    # constructor
    def __init__(self, fare_id = "", date = "", user_id = "", purpose = "", transportation = "", departure = "", arrival = "", round_trip = "", fare = ""):
        self.conn           = get_connection()
        self.fare_id        = fare_id
        self.date           = date
        self.user_id        = user_id
        self.purpose        = purpose
        self.transportation = transportation
        self.departure      = departure
        self.arrival        = arrival
        self.round_trip     = round_trip
        self.fare           = fare

    #  ユーザIDと年月で運賃情報を取得
    def get_by_year_month(self, user_id, year, month):

        year_month = "%s-%s" % (year, month)

        # 運賃一覧取得
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM fare WHERE user_id = %s AND date LIKE %s ORDER BY DATE ASC"
                cursor.execute(sql, (user_id, "%s%%" % year_month))
                results = cursor.fetchall()
        finally:
            self.conn.close()

        if not results:
            return []

        fares = []

        fare_total = 0

        for result in results:

            #  運賃クラスをリストに入れる
            fare = Fare(
                fare_id=result['fare_id'],
                date=result['date'],
                user_id=result['user_id'],
                purpose=result['purpose'],
                transportation=result['transportation'],
                departure=result['departure'],
                arrival=result['arrival'],
                round_trip=result['round_trip'],
                fare=result['fare']
                )
            fares.append(fare)

            fare_total += result['fare']

        return fares, fare_total

    #  運賃情報を保存
    def save(self):

        # 存在チェック
        check = self.check_fare(self.fare_id)
        
        try:
            with self.conn.cursor() as cursor:

                # 勤怠がなかった場合はinsertする
                if not check:
                    # insert
                    sql = "INSERT INTO fare (`fare_id`, `date`, `user_id`, `purpose`, `transportation`, `departure`, `arrival`, `round_trip`, `fare`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (self.fare_id, self.date, self.user_id, self.purpose, self.transportation, self.departure, self.arrival, self.round_trip, self.fare))
                    self.conn.commit()
                else:
                    # update
                    sql = "UPDATE fare SET `fare_id`= %s, `date`= %s, `user_id`= %s, `purpose`= %s, `transportation`= %s, `departure`= %s, `arrival`= %s, `round_trip`= %s, `fare`= %s WHERE fare_id = %s"
                    cursor.execute(sql, (self.fare_id, self.date, self.user_id, self.purpose, self.transportation, self.departure, self.arrival, self.round_trip, self.fare, self.fare_id))
                    self.conn.commit()
        finally:
            self.conn.close()
        

    # 運賃の存在チェック
    def check_fare(self, fare_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM fare WHERE fare_id = %s"
            cursor.execute(sql, fare_id)
            result = cursor.fetchone()

            if not result:
                return False

            return True