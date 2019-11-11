# 返回状态码
CODE = 'code'
# 返回提示
MSG = 'msg'
# 返回数据
DATA = 'data'

SUCCESS_CODE = 0
ERROR_CODE = 1

SUCCESS_MSG = 'success'
ERROR_MSG = 'error'

# 成功结果的封装方法


def success(data, *args):
    ret = {
        CODE: SUCCESS_CODE,
        MSG: SUCCESS_MSG,
        DATA: data,
    }

    if args:
        ret[MSG] = args[0]
    return ret


# 失败结果的封装方法

def error(*args):
    ret = {
        CODE: ERROR_CODE,
        MSG: ERROR_MSG
    }
    if args:
        ret[MSG] = args[0]
    return ret


DB_WEATHER = 'weather'
COLLECTION_WEATHER = 'weathers'
MONGO_ID = '_id'
