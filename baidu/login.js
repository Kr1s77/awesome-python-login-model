/**
 * Created by resolvewang on 2017/4/15.
 */
function getGid() {
    return "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (e) {
        var t = 16 * Math.random() | 0, n = "x" == e ? t : 3 & t | 8;
        return n.toString(16)
    }).toUpperCase()
}

function  getCallback() {
    return "bd__cbs__" + Math.floor(2147483648 * Math.random()).toString(36)
}

