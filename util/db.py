import pymysql.cursors

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='forgotten',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
    )