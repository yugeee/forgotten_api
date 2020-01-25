import requests
import json
from models.attendance import Attendance

class Calendar_API:

    # カレンダー取得
    @staticmethod
    def get_calendar(year, month):
        base_url = "http://calendar-service.net/cal?start_year=%s&start_mon=%s&end_year=&end_mon=&year_style=normal&month_style=numeric&wday_style=ja&format=csv&zero_padding=1"
        url = base_url % (year, month)
        
        # カレンダーAPIからカレンダー情報を取得
        res = requests.get(url)

        # 200以外ならエラー
        if res.status_code != 200:
            return res.status_code, json.loads(res.text)

        calendar_csv = res.text

        calendar = []

        # csvを配列にして返却
        calendar_array = calendar_csv.split('\n')

        # 最初はヘッダなので削除しておく 
        calendar_array.pop(0)

        for cal in calendar_array:
            cal_array = cal.split(',')

            # 要素が空の場合は飛ばす
            if len(cal_array) != 8:
                continue
            
            oneday = {
                "date":    "%s-%s-%s" % (cal_array[0],cal_array[1].zfill(2),cal_array[2].zfill(2)),
                "weekday": Attendance.weekday_ja[int(cal_array[6])],
                "holiday": cal_array[7]
            }
            calendar.append(oneday)

        return res.status_code, calendar


# debug
if __name__ == "__main__":
    status_code, calendar = Calendar_API.get_calendar("2019", "05")
    print(calendar)