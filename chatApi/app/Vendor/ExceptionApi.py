'''
@Author: hua
@Date: 2019-05-30 10:41:29
@LastEditors: hua
@LastEditTime: 2019-06-11 16:28:29
'''
from flask import jsonify, make_response
from app.Vendor.Log import log
from app.Vendor.Utils import Utils
import traceback,sys

def ExceptionApi(code, e):
    """ 接口异常处理 """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    log().exception(e)
    body = {}
    body['error_code'] = code
    body['error'] = True
    body['show'] = False
    body['debug_id'] = Utils.unique_id()
    #这里exc_type 和exc_value信息重复，所以不打印
    body['traceback'] = traceback.format_exception([], exc_value, exc_traceback)
    return make_response(jsonify(body))