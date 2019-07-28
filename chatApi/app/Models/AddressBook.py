'''
@Author: hua
@Date: 2019-02-14 11:11:29
@LastEditors: hua
@LastEditTime: 2019-07-28 10:48:50
'''
import time, math

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import  relationship, foreign, remote
from sqlalchemy import desc, asc
from app import dBSession
from app.Models.Base import Base
from app.Models.Model import HtAddressBook
from app.Models.Room import Room
from app.Models.Users import Users
from app.Vendor.Decorator import classTransaction, transaction
from app.Vendor.Utils import Utils


class AddressBook(HtAddressBook, Base, SerializerMixin):
    users = relationship('Users', uselist=False, primaryjoin=foreign(HtAddressBook.focused_user_id) == remote(Users.id))
    room = relationship('Room', uselist=False, primaryjoin=foreign(HtAddressBook.room_uuid) == remote(Room.room_uuid))
    be_users = relationship('Users', uselist=False, primaryjoin=foreign(HtAddressBook.be_focused_user_id) == remote(Users.id))
    """ 
        列表
        @param set filters 查询条件
        @param obj order 排序
        @param tuple field 字段
        @param int offset 偏移量
        @param int limit 取多少条
        @return dict
    """
    def getList(self, filters, order, field=(), offset = 0, limit = 15):
        res = {}
        res['page'] ={}
        res['page']['count'] = dBSession.query(AddressBook).filter(*filters).count()
        res['list'] = []
        res['page']['total_page'] = self.get_page_number(res['page']['count'], limit)
        res['page']['current_page'] = offset
        if offset != 0:
            offset = (offset - 1) * limit

        if res['page']['count'] > 0:
            res['list'] = dBSession.query(AddressBook).filter(*filters)
            res['list'] = res['list'].order_by(order).offset(offset).limit(limit).all()
        if not field:
            res['list'] = [c.to_dict() for c in res['list']]
        else:
            res['list'] = [c.to_dict(only=field) for c in res['list']]
        return res

    """
        查询全部
        @param set filters 查询条件
        @param obj order 排序
        @param tuple field 字段
        @param int $limit 取多少条
        @return dict
    """
    def getAll(self, filters, order, field = (), limit = 0):
        if not filters:
            res = dBSession.query(AddressBook)
        else:   
            res = dBSession.query(AddressBook).filter(*filters)
        if limit != 0:
            res = res.limit(limit)
        order = order.split(' ')
        if order[1] == 'desc':
            res = res.order_by(desc(order[0])).all()
        else:
            res = res.order_by(asc(order[0])).all()
        if not field:
            res = [c.to_dict() for c in res]
        else:
            res = [c.to_dict(only=field) for c in res]
        return res


    
    """
        获取一条
        @param set filters 查询条件
        @param obj order 排序
        @param tuple field 字段
        @return dict
    """
    def getOne(self, filters, order = 'id desc', field = ()):
        res = dBSession.query(AddressBook).filter(*filters)
        order = order.split(' ')
        if order[1] == 'desc':
            res = res.order_by(desc(order[0])).first()
        else:
            res = res.order_by(asc(order[0])).first()
        if res == None:
            return None
        if not field:
            res = res.to_dict()
        else:
           res = res.to_dict(only=field) 
        return res
  
    """
        添加
        @param obj data 数据
        @return bool
    """
    @classTransaction
    def add(self, data):
        dBSession.add(AddressBook(**data))
        return True

    
    """
        修改
        @param dict data 数据
        @param set filters 条件
        @return bool
    """
    @classTransaction
    def edit(self, data, filters):
        dBSession.query(AddressBook).filter(*filters).update(data, synchronize_session=False)
        return True
    
    """
        删除
        @paramset filters 条件
        @return bool
    """
    @classTransaction
    def delete(self, filters):
        dBSession.query(AddressBook).filter(*filters).delete(synchronize_session=False)
        return True
    
    """
        统计数量
        @param set filters 条件
        @param obj field 字段
        @return int
    """  
    def getCount(self, filters, field = None):
        if field == None:
            return dBSession.query(AddressBook).filter(*filters).count()
        else:
            return dBSession.query(AddressBook).filter(*filters).count(field)
        
    @staticmethod
    def get_page_number(count, page_size):
        count = float(count)
        page_size = abs(page_size)
        if page_size != 0:
            total_page = math.ceil(count / page_size)
        else:
            total_page = math.ceil(count / 5)
        return total_page


    """ 转服务层 """

    @staticmethod
    def getAdddressBookByFocusedUserId(focused_user_id, be_focused_user_id):
        filters = {
            AddressBook.focused_user_id==focused_user_id,
            AddressBook.be_focused_user_id==be_focused_user_id
        }       
        data = dBSession.query(AddressBook).filter(*filters).first()
        return data
    # 增加用户
    @staticmethod
    @transaction
    def addRoomAndAddressBook(room_uuid, focused_user_id, be_focused_user_id):
        roomData = {
            'room_uuid': room_uuid,
            'last_msg': '',
            'user_id': focused_user_id
        }
        room = Room.insertRoomData(roomData)
        addressBook = AddressBook(
            focused_user_id=focused_user_id,
            be_focused_user_id=be_focused_user_id,
            room_uuid=room_uuid,
            unread_number=0,
            is_alert=1,
            created_at=time.time(),
            updated_at=time.time()
        )
        dBSession.add(addressBook)
        addressBook = AddressBook(
            focused_user_id=be_focused_user_id,
            be_focused_user_id=focused_user_id,
            room_uuid=room_uuid,
            unread_number=0,
            is_alert=1,
            created_at=time.time(),
            updated_at=time.time()
        )
        dBSession.add(addressBook)
        return True

    @staticmethod
    def get(room_uuid):
        return dBSession.query(AddressBook).filter(AddressBook.room_uuid == room_uuid).all()

    # 获取列表
    @staticmethod
    def rawGetList(page_no, per_page, filters):
        dataObj = dBSession.query(AddressBook).order_by(AddressBook.created_at.desc()).filter(*filters).all()
        addressBookList = Utils.db_l_to_d(dataObj)
        data = Base.formatBody(
            {"addressBookList": addressBookList})
        return data

    # 获取消息房间列表
    @staticmethod
    def getRoomList(user_id):
        filters = {
            AddressBook.be_focused_user_id == user_id
        }
        data = dBSession.query(AddressBook).order_by(AddressBook.updated_at.desc()).filter(*filters).all()
        data = Base.formatBody(Utils.db_l_to_d(data))
        return data

     # 更新关注者未读消息
    @staticmethod
    @transaction
    def updateUnreadNumber(room_uuid, user_id):
        filter = {
            AddressBook.be_focused_user_id != user_id,
            AddressBook.room_uuid == room_uuid
        }
        dBSession.query(AddressBook).filter(*filter).update({
            AddressBook.unread_number: AddressBook.unread_number+1,
            AddressBook.updated_at: time.time()
        })
        return dBSession.commit()

    # 清除关注者未读消息次数
    @staticmethod
    @transaction
    def cleanUnreadNumber(room_uuid, user_id):
        filter = {
            AddressBook.be_focused_user_id == user_id,
            AddressBook.room_uuid == room_uuid
        }
        dBSession.query(AddressBook).filter(
            *filter).update({'unread_number': 0, 'updated_at': time.time()})
        return dBSession.commit()
