import Dexie from 'dexie';

// Declare Database 本地数据库，这是简单使用增删改查例子，并不能直接引入使用
/* 
 *增加申请用户
 *params: obj value
 *return bool
 */

export function addAddressBookBeg(value) {
    //申明数据库
    const db = new Dexie("addressBookBeg");
    //定义字段
    db.version(1).stores({ addressBookBeg: "++id, email, head_img, user_id, nick_name, status, created_at, updated_at" });
    //事务读写
    db.transaction('rw', db.addressBookBeg, async() => {
        if (await db.addressBookBeg.where({'user_id': value.user_id}).count() === 0) {
            await db.addressBookBeg.add(value);
        }


    }).catch(e => {
        console.log(e.stack || e);
        return false
    });
    return true
}

/* 
 *读配置文档
 *return bool
 */
export function getAddressBookBeg() {
    //申明数据库
    const db = new Dexie("addressBookBeg");
    //定义字段
    db.version(1).stores({ addressBookBeg: "++id, email, head_img, user_id, nick_name, status, created_at, updated_at" });
    //事务读写
    return db.transaction('rw', db.addressBookBeg, async() => {

        // Make sure we have something in DB:
        //统计次数
        let data =   await db.addressBookBeg.toArray()
        return data   


    }).catch(e => {
        console.log(e.stack || e);
        return false
    });
}

/* 
 *更新配置文档
 *return bool
 */
export function updateAddressBookBeg(id, status) {
    //申明数据库
    const db = new Dexie("addressBookBeg");
    //定义字段
    db.version(1).stores({ addressBookBeg: "++id, email, head_img, user_id, nick_name, status, created_at, updated_at" });
    //事务读写
    return db.transaction('rw', db.addressBookBeg, async() => {

        // Make sure we have something in DB:
        //更新状态
        let updated = db.addressBookBeg.where("id").equals(id).modify({status: status});
        if (updated){
            let data =   await db.addressBookBeg.toArray()
            return data   
        }
        return Promise.reject('update error') 

    }).catch(e => {
        console.log(e.stack || e);
        return false
    });
}