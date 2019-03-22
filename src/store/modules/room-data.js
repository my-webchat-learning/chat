/**
 * 作者：hua
 * 时间：2019-03-15
 * 聊天数据临时管理
 */
export default {
    state: {
        msgList:[]//聊天数据

    },
    getters:{
        msgList(state){
        return state.msgList
        }
    },

    actions: {
        //提交穿过来的参数 以及突变给mutations
        updateMsgList({commit}, msgList) {
        commit("updateMsgList", msgList);
        }
    },

    mutations: {
        //修改仓库值
        updateMsgList(state, msgList){
        state.msgList = msgList
        },
    }
}