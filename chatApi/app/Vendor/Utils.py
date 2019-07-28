'''
@Author: hua
@Date: 2019-02-10 09:55:10
@description: 工具类，封装一些通用方法 
@LastEditors: hua
@LastEditTime: 2019-07-26 13:44:07
'''

from app.env import ALLOWED_EXTENSIONS
from app.Lang.zh_CN.validation import validation
from app.Vendor.Code import Code
import time

class Utils:
    """ 
        获取指定键的值 
        @param string name
        @param list|dict data
        !return list|dict|bool
    """
    @staticmethod
    def getColumn(name, data):
        if isinstance(data, list):
            data_list = []
            for data_dict in data:
                for key, val in data_dict.items():
                    if key == name:
                        data_list.append(val)
            return data_list
        if isinstance(data, dict):
            if name in data.keys():
                return data[name]
            return False
        return False  
    
    """ 
        格式化原生查询结果tuple转dict
        @param list data
        @return list
    """
    @staticmethod
    def db_t_d(data):
        data_list = []
        for val in data:
            val_dict = dict(zip(val.keys(), val.values()))
            data_list.append(val_dict)
        data = {}
        data = data_list
        return data
    
    ''' 
    * 用于sql结果列表对象类型转字典
    * @param list data
    * @return dict
    '''
    @staticmethod
    def db_l_to_d(data):
        data_list = []
        for val in data:
            val_dict = val.to_dict()
            data_list.append(val_dict)
        data = {}
        data = data_list
        return data

    ''' 
    * 用于sql结果对象类型转字典
    * @param object obj
    * @return dict
    '''
    @staticmethod
    def class_to_dict(obj):
        '''把对象(支持单个对象、list、set)转换成字典'''
        is_list = obj.__class__ == [].__class__
        is_set = obj.__class__ == set().__class__
        if is_list or is_set:
            obj_arr = []
            for o in obj:
                # 把Object对象转换成Dict对象
                dict = {}
                dict.update(o.__dict__)
                obj_arr.append(dict)
                return obj_arr
        else:
            dict = {}
            dict.update(obj.__dict__)
            return dict

    """ 验证文件类型
        @param string filename
        return string path
    """
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    """ uuid,唯一id 
        return string id
    """
    @staticmethod
    def unique_id(prefix=''):
        return prefix + hex(int(time.time()))[2:10] + hex(int(time.time() * 1000000) % 0x100000)[2:7]
      
    """ 
    * 格式化返回体
    * @param dict data
    * @return dict
    """
    @staticmethod
    def formatBody(data={}, msg='', show=True):
        dataformat = {}
        dataformat['error_code'] = Code.SUCCESS
        dataformat['data'] = data
        dataformat['msg'] = msg
        dataformat['show'] = show
        return dataformat

    """ 
    * 格式化错误返回体
    * @param int code
    * @param string message
    * @return dict
    """
    @staticmethod
    def formatError(code, message='', show=True):
        body = {}
        body['error'] = True
        body['error_code'] = code
        body['msg'] = message
        body['show'] = show
        return body
    
    """ 
    * 格式化验证错误描述
    * @param string name
    * @param dict rules
    * @param dict msg
    * @return string
    """
    @staticmethod
    def validateMsgFormat(name, rules, msg):
        #根据规则生成返回
        if not msg:
            msgFormat = dict()
            for key in  rules:
                if key == 'required':
                    ruleMsg = ''
                    actionMsg = validation[key][rules[key]]
                elif key == 'maxlength':
                    ruleMsg = validation[key]
                    actionMsg = rules[key]
                elif key == 'minlength': 
                    ruleMsg = validation[key]
                    actionMsg = rules[key]
                else:
                    ruleMsg = validation[key]
                    actionMsg = validation[rules[key]]
                if name in validation.keys():
                    msgFormat[key] = "{} {} {}".format(validation[name], ruleMsg, actionMsg)
                else:
                    return msg
            return msgFormat
        return msg
    