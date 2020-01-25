import hashlib

#  IDをセット
def set_id(user_id, date, purpose):
    key = '%s%s%s' % (user_id, date, purpose)
    return hashlib.md5(key.encode()).hexdigest()