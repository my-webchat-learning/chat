import {send} from '@/utils/socketio'


// 获取房间信息接口
export function roomGet (data) {
    let reqData = {
        'c':'RoomService',
        'a':'get',
        'data':data
    }
    return send('send', reqData, 'api')
}

// 删除房间
export function roomDel(data){
    let reqData = {
        'c':'RoomService',
        'a':'delete',
        'data':data
    }
    return send('send', reqData, 'api')
}

//获取房间聊天记录
export function getCloudRoomMsg(data){
    let reqData = {
        'c':'RoomService',
        'a':'getMsg',
        'data':data
    }
    return send('send', reqData, 'api')
}

//添加房间聊天记录
export function addCloudRoomMsg(data){
    let reqData = {
        'c':'RoomService',
        'a':'addMsg',
        'data':data
    }
    return send('send', reqData, 'api')
}

//删除房间聊天记录
export function roomMsgDel(data){
    let reqData = {
        'c':'RoomService',
        'a':'delMsg',
        'data':data
    }
    return send('send', reqData, 'api')
}

//更新房间聊天记录
export function updateCloudRoomMsg(data){
    let reqData = {
        'c':'RoomService',
        'a':'updateMsg',
        'data':data
    }
    return send('send', reqData, 'api')
}