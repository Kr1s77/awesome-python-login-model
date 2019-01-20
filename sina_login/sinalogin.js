/**
 * Created by rookiecoder on 2016/4/29.
 */
function SSOController() {
    var undefined;
    var me = this;
    var updateCookieTimer = null;
    var updateCookieTimeHardLimit = 1800;
    var cookieExpireTimeLength = 3600 * 24;
    var crossDomainForward = null;
    var crossDomainTimer = null;
    var crossDomainTime = 3;
    var autoLoginCallBack2 = null;
    var ssoCrosssDomainUrl = "http://login.sina.com.cn/sso/crossdomain.php";
    var ssoLoginUrl = "http://login.sina.com.cn/sso/login.php";
    var ssoLogoutUrl = "http://login.sina.com.cn/sso/logout.php";
    var ssoUpdateCookieUrl = "http://login.sina.com.cn/sso/updatetgt.php";
    var ssoPreLoginUrl = "http://login.sina.com.cn/sso/prelogin.php";
    var pincodeUrl = "http://login.sina.com.cn/cgi/pin.php";
    var vfValidUrl = "http://weibo.com/sguide/vdun.php";
    var generateVisitorUrl = "http://passport.weibo.com/visitor/visitor";
    var crossDomainUrlList = null;
    var loginMethod = "";
    var ssoServerTimeTimer = null;
    var ssoLoginTimer = null;
    var loginByConfig = null;
    var loginMethodCheck = null;
    var https = 1;
    var rsa = 2;
    var wsse = 4;
    var pcid = "";
    var tmpData = {};
    var preloginTimeStart = 0;
    var preloginTime = 0;
    var callbackLogoutStatus;
    this.https = 1;
    this.rsa = 2;
    this.wsse = 4;
    this.name = "sinaSSOController";
    this.loginFormId = "ssoLoginForm";
    this.scriptId = "ssoLoginScript";
    this.ssoCrossDomainScriptId = "ssoCrossDomainScriptId";
    this.loginFrameName = "ssoLoginFrame";
    this.appLoginURL = {"weibo.com": "https://passport.weibo.com/wbsso/login"};
    this.appDomainService = {"weibo.com": "miniblog"};
    this.loginExtraQuery = {};
    this.setDomain = false;
    this.feedBackUrl = "";
    this.service = "sso";
    this.domain = "sina.com.cn";
    this.from = "";
    this.pageCharset = "GB2312";
    this.useTicket = false;
    this.isCheckLoginState = false;
    this.isUpdateCookieOnLoad = true;
    this.useIframe = true;
    this.noActiveTime = 7200;
    this.autoUpdateCookieTime = 1800;
    this.loginType = rsa;
    this.timeoutEnable = false;
    this.loginTimeout = 5000;
    this.crossDomain = true;
    this.scriptLoginHttps = false;
    this.allowAutoFoundServerTime = false;
    this.allowAutoFoundServerTimeError = true;
    this.calcServerTimeInterval = 2000;
    this.servertime = null;
    this.nonce = null;
    this.rsaPubkey = null;
    this.rsakv = null;
    this.loginExtraFlag = {};
    this.cdult = false;
    this.crossDomainTime = 5;
    this.failRedirect = false;
    this.isGenerateVisitor = true;
    this.generateVisitorProbability = 1;
    this.generateVisitorDelay = 6;
    this.generateVisitorDomain = ["^.*sina.com.cn$"];
    this.getVersion = function () {
        return "ssologin.js(v1.4.18) 2014-06-12"
    };
    this.getEntry = function () {
        return me.entry
    };
    this.getClientType = function () {
        return me.getVersion().split(" ")[0]
    };
    this.init = function () {
        if (getType(arguments[0]) === "object") {
            return customPrepare(arguments[0])
        }
        me.setLoginType(me.loginType);
        var ssoConfig = window.sinaSSOConfig;
        if (typeof ssoConfig != "object") {
            ssoConfig = {}
        }
        var name;
        for (name in ssoConfig) {
            me[name] = ssoConfig[name]
        }
        if (!me.entry) {
            me.entry = me.service
        }
        if (me.isUpdateCookieOnLoad) {
            setTimeout(me.name + ".updateCookie()", 10000)
        }
        if (me.isGenerateVisitor) {
            if (self === top && Math.random() < me.generateVisitorProbability && location.protocol !== "https:") {
                setTimeout(me.name + ".generateVisitor()", me.generateVisitorDelay * 1000)
            }
        }
        if (me.isCheckLoginState) {
            addEventListener(window, "load", function () {
                me.checkLoginState()
            })
        }
        if (me.allowAutoFoundServerTime && ssoLoginServerTime) {
            me.setServerTime(ssoLoginServerTime)
        }
        me.customInit()
    };
    this.getLoginInfo = function () {
        var sso_info = getCookie("sso_info");
        if (!sso_info) {
            return {}
        }
        try {
            return parse_str(sinaSSOEncoder.Cookie.decode(sso_info))
        } catch (e) {
            return {}
        }
    };
    this.customInit = function () {
    };
    this.customUpdateCookieCallBack = function (result) {
    };
    this.customLoginCallBack = function (loginStatus) {
    };
    this.customLogoutCallBack = function (result) {
        me.customLoginCallBack({result: false})
    };
    var customLogin, customPrepare, customLogout;
    (function () {
        var $empty = function () {
        }, loginParam = {
            username: "",
            password: "",
            savestate: 0,
            vsnf: 0,
            vsnval: "",
            door: "",
            setCookie: 1,
            ssoSimpleLogin: 0,
            onComplete: $empty,
            onSuccess: $empty,
            onFailure: $empty
        }, logoutParam = {onComplete: $empty, onSuccess: $empty, onFailure: $empty}, hashExtra = {
            vsnf: "vsnf",
            vsnval: "vsnval",
            door: "door",
            setCookie: "s",
            ssoSimpleLogin: "ssosimplelogin"
        }, loginOptions = {}, logoutOptions = {};
        var parseParam = function (original, spec) {
            var key, param = {};
            original = original || {};
            spec = spec || {};
            objMerge(param, original);
            for (key in spec) {
                if (original.hasOwnProperty(key)) {
                    param[key] = spec[key]
                }
            }
            return param
        };
        var callback = function (options, name, loginStatus) {
            if (typeof(options[name]) === "function") {
                options[name](loginStatus)
            }
        };
        this.callbackLoginStatus = function (loginStatus) {
            me.customLoginCallBack(loginStatus);
            callback(loginOptions, "onComplete", loginStatus);
            if (loginStatus && loginStatus.result === true) {
                callback(loginOptions, "onSuccess", loginStatus)
            } else {
                callback(loginOptions, "onFailure", loginStatus)
            }
        };
        callbackLogoutStatus = function (logoutStatus) {
            me.customLogoutCallBack(logoutStatus);
            callback(logoutOptions, "onComplete", logoutStatus);
            if (logoutStatus && logoutStatus.result === true) {
                callback(logoutOptions, "onSuccess", logoutStatus)
            } else {
                callback(logoutOptions, "onFailure", logoutStatus)
            }
        };
        customPrepare = function (spec) {
            var key;
            spec = spec || {};
            loginOptions = objMerge({
                entry: "sso",
                useTicket: false,
                service: "sso",
                domain: "sina.com.cn",
                feedBackUrl: "",
                setDomain: false,
                crossDomain: true,
                name: "sinaSSOController"
            }, loginParam);
            loginOptions = parseParam(loginOptions, spec);
            window[loginOptions.name] = window[loginOptions.name] || me;
            for (key in loginOptions) {
                if (!loginParam.hasOwnProperty(key)) {
                    me[key] = loginOptions[key]
                }
            }
            me.loginExtraQuery = {};
            objMerge(me.loginExtraQuery, loginOptions.loginExtraQuery);
            for (key in hashExtra) {
                if (loginOptions.hasOwnProperty(key)) {
                    me.loginExtraQuery[hashExtra[key]] = loginOptions[key]
                }
            }
        };
        customLogin = function (spec) {
            spec = spec || {};
            customPrepare(spec);
            me.login(loginOptions.username, loginOptions.password, loginOptions.savestate)
        };
        customLogout = function (spec) {
            spec = spec || {};
            logoutOptions = objMerge({}, logoutParam);
            logoutOptions = parseParam(logoutOptions, spec);
            me.logout()
        }
    }).apply(this);
    this.login = function (username, password, savestate) {
        if (getType(arguments[0]) === "object") {
            return customLogin(arguments[0])
        }
        if (!ssoLoginTimer) {
            ssoLoginTimer = new prototypeTimer(me.timeoutEnable)
        } else {
            ssoLoginTimer.clear()
        }
        ssoLoginTimer.start(me.loginTimeout, function () {
            ssoLoginTimer.clear();
            me.callbackLoginStatus({
                result: false,
                errno: -1,
                reason: unescape("%u767B%u5F55%u8D85%u65F6%uFF0C%u8BF7%u91CD%u8BD5")
            })
        });
        savestate = savestate == undefined ? 0 : savestate;
        tmpData.savestate = savestate;
        loginByConfig = function () {
            if (!me.feedBackUrl && loginByXMLHttpRequest(username, password, savestate)) {
                return true
            }
            if (me.useIframe && (me.setDomain || me.feedBackUrl)) {
                if (me.setDomain) {
                    document.domain = me.domain;
                    if (!me.feedBackUrl && me.domain != "sina.com.cn") {
                        me.feedBackUrl = makeURL(me.appLoginURL[me.domain], {domain: 1})
                    }
                }
                loginMethod = "post";
                var result = loginByIframe(username, password, savestate);
                if (!result) {
                    loginMethod = "get";
                    if (me.scriptLoginHttps) {
                        me.setLoginType(me.loginType | https)
                    } else {
                        me.setLoginType(me.loginType | rsa)
                    }
                    loginByScript(username, password, savestate)
                }
            } else {
                loginMethod = "get";
                loginByScript(username, password, savestate)
            }
            me.nonce = null
        };
        loginMethodCheck = function () {
            if ((me.loginType & wsse) || (me.loginType & rsa)) {
                if (me.servertime) {
                    if (!me.nonce) {
                        me.nonce = makeNonce(6)
                    }
                    loginByConfig();
                    return true
                }
                me.getServerTime(username, loginByConfig)
            } else {
                loginByConfig()
            }
        };
        loginMethodCheck();
        return true
    };
    this.prelogin = function (config, callback) {
        var url = location.protocol == "https:" ? ssoPreLoginUrl.replace(/^http:/, "https:") : ssoPreLoginUrl;
        var username = config.username || "";
        username = sinaSSOEncoder.base64.encode(urlencode(username));
        delete config.username;
        var arrQuery = {entry: me.entry, callback: me.name + ".preloginCallBack", su: username, rsakt: "mod"};
        url = makeURL(url, objMerge(arrQuery, config));
        me.preloginCallBack = function (result) {
            if (result && result.retcode == 0) {
                me.setServerTime(result.servertime);
                me.nonce = result.nonce;
                me.rsaPubkey = result.pubkey;
                me.rsakv = result.rsakv;
                pcid = result.pcid;
                preloginTime = (new Date()).getTime() - preloginTimeStart - (parseInt(result.exectime, 10) || 0)
            }
            if (typeof callback == "function") {
                callback(result)
            }
        };
        preloginTimeStart = (new Date()).getTime();
        excuteScript(me.scriptId, url)
    };
    this.getServerTime = function (username, callback) {
        if (me.servertime) {
            if (typeof callback == "function") {
                callback({retcode: 0, servertime: me.servertime})
            }
            return true
        }
        me.prelogin({username: username}, callback)
    };
    this.logout = function () {
        try {
            if (getType(arguments[0]) === "object") {
                return customLogout(arguments[0])
            }
            var request = {entry: me.getEntry(), callback: me.name + ".ssoLogoutCallBack"};
            try {
                request.sr = window.screen.width + "*" + window.screen.height
            } catch (e) {
            }
            var url = location.protocol == "https:" ? ssoLogoutUrl.replace(/^http:/, "https:") : ssoLogoutUrl;
            url = makeURL(url, request);
            excuteScript(me.scriptId, url)
        } catch (e) {
        }
        return true
    };
    this.ssoLogoutCallBack = function (result) {
        if (result.arrURL) {
            me.setCrossDomainUrlList(result)
        }
        me.crossDomainAction("logout", function () {
            callbackLogoutStatus({result: true})
        })
    };
    this.updateCookie = function () {
        try {
            if (me.autoUpdateCookieTime > 5) {
                if (updateCookieTimer != null) {
                    clearTimeout(updateCookieTimer)
                }
                updateCookieTimer = setTimeout(me.name + ".updateCookie()", me.autoUpdateCookieTime * 1000)
            }
            var cookieExpireTime = me.getCookieExpireTime();
            var now = (new Date()).getTime() / 1000;
            var result = {};
            if (cookieExpireTime == null) {
                result = {retcode: 6102}
            } else {
                if (cookieExpireTime < now) {
                    result = {retcode: 6203}
                } else {
                    if (cookieExpireTime - cookieExpireTimeLength + updateCookieTimeHardLimit > now) {
                        result = {retcode: 6110}
                    } else {
                        if (cookieExpireTime - now > me.noActiveTime) {
                            result = {retcode: 6111}
                        }
                    }
                }
            }
            if (result.retcode !== undefined) {
                me.customUpdateCookieCallBack(result);
                return false
            }
            var url = location.protocol == "https:" ? ssoUpdateCookieUrl.replace(/^http:/, "https:") : ssoUpdateCookieUrl;
            url = makeURL(url, {entry: me.getEntry(), callback: me.name + ".updateCookieCallBack"});
            excuteScript(me.scriptId, url)
        } catch (e) {
        }
        return true
    };
    this.setCrossDomainUrlList = function (urlList) {
        crossDomainUrlList = urlList
    };
    this.checkAltLoginName = function () {
        return true
    };
    this.callFeedBackUrl = function (loginStatus) {
        try {
            var request = {callback: me.name + ".feedBackUrlCallBack"};
            if (loginStatus.ticket) {
                request.ticket = loginStatus.ticket
            }
            if (loginStatus.retcode !== undefined) {
                request.retcode = loginStatus.retcode
            }
            var url = makeURL(me.feedBackUrl, request);
            excuteScript(me.scriptId, url)
        } catch (e) {
        }
        return true
    };
    this.loginCallBack = function (result) {
        try {
            if (me.timeoutEnable && !ssoLoginTimer.isset()) {
                return
            }
            ssoLoginTimer.clear();
            me.loginExtraFlag = {};
            var loginStatus = {};
            var st = result.ticket;
            var uid = result.uid;
            if (uid) {
                loginStatus.result = true;
                loginStatus.retcode = 0;
                loginStatus.userinfo = {uniqueid: result.uid};
                if (st) {
                    loginStatus.ticket = st
                }
                if (result.cookie) {
                    loginStatus.cookie = result.cookie
                }
                if (me.feedBackUrl) {
                    if (me.crossDomain) {
                        me.crossDomainAction("login", function () {
                            me.callFeedBackUrl(loginStatus)
                        })
                    } else {
                        me.callFeedBackUrl(loginStatus)
                    }
                } else {
                    if (me.crossDomain) {
                        if (result.crossDomainUrlList) {
                            me.setCrossDomainUrlList({retcode: 0, arrURL: result.crossDomainUrlList})
                        }
                        me.crossDomainAction("login", function () {
                            if (st && me.appLoginURL[me.domain]) {
                                me.appLogin(st, me.domain, me.name + ".callbackLoginStatus")
                            } else {
                                loginStatus.userinfo = objMerge(loginStatus.userinfo, me.getSinaCookie());
                                me.callbackLoginStatus(loginStatus)
                            }
                        })
                    } else {
                        me.callbackLoginStatus(loginStatus)
                    }
                }
            } else {
                if (loginMethodCheck && result.retcode == "2092" && me.allowAutoFoundServerTimeError) {
                    me.setServerTime(0);
                    me.loginExtraFlag = objMerge(me.loginExtraFlag, {wsseretry: "servertime_error"});
                    loginMethodCheck();
                    loginMethodCheck = null;
                    return false
                }
                loginStatus.result = false;
                loginStatus.errno = result.retcode;
                if (loginStatus.errno == "4069") {
                    var reason = result.reason.split("|");
                    loginStatus.reason = reason[0];
                    if (reason.length == 2) {
                        loginStatus.rurl = reason[1]
                    }
                    if (loginStatus.rurl) {
                        try {
                            top.location.href = loginStatus.rurl;
                            return
                        } catch (e) {
                        }
                    }
                } else {
                    loginStatus.reason = result.reason
                }
                me.callbackLoginStatus(loginStatus)
            }
        } catch (e) {
        }
        return true
    };
    this.updateCookieCallBack = function (result) {
        if (result.retcode == 0) {
            me.crossDomainAction("update", function () {
                me.customUpdateCookieCallBack(result)
            })
        } else {
            me.customUpdateCookieCallBack(result)
        }
    };
    this.feedBackUrlCallBack = function (result) {
        if (loginMethod == "post" && me.timeoutEnable && !ssoLoginTimer.isset()) {
            return
        }
        if (result.errno == "2092") {
            me.setServerTime(0)
        }
        if (loginMethodCheck && (result.errno == "2092") && me.allowAutoFoundServerTimeError) {
            me.loginExtraFlag = objMerge(me.loginExtraFlag, {wsseretry: "servertime_error"});
            loginMethodCheck();
            loginMethodCheck = null;
            return false
        } else {
            ssoLoginTimer && ssoLoginTimer.clear()
        }
        if (result.errno == "4069") {
            var reason = result.reason.split("|");
            result.reason = reason[0];
            if (reason.length == 2) {
                result.rurl = reason[1];
                try {
                    top.location.href = result.rurl;
                    return
                } catch (e) {
                }
            }
        }
        me.callbackLoginStatus(result);
        removeNode(me.loginFrameName)
    };
    this.doCrossDomainCallBack = function (result) {
        me.crossDomainCounter++;
        if (result) {
            removeNode(result.scriptId)
        }
        if (me.crossDomainCounter == me.crossDomainCount) {
            clearTimeout(crossDomainTimer);
            me.crossDomainResult()
        }
    };
    this.crossDomainCallBack = function (result) {
        removeNode(me.ssoCrossDomainScriptId);
        if (!result || result.retcode != 0) {
            return false
        }
        var arrURL = result.arrURL;
        var url, scriptId;
        var request = {callback: me.name + ".doCrossDomainCallBack"};
        me.crossDomainCount = arrURL.length;
        me.crossDomainCounter = 0;
        if (arrURL.length == 0) {
            clearTimeout(crossDomainTimer);
            me.crossDomainResult();
            return true
        }
        for (var i = 0; i < arrURL.length; i++) {
            url = arrURL[i];
            scriptId = "ssoscript" + i;
            request.scriptId = scriptId;
            url = makeURL(url, request);
            if (isSafari()) {
                excuteIframe(scriptId, url)
            } else {
                excuteScript(scriptId, url)
            }
        }
    };
    this.crossDomainResult = function () {
        crossDomainUrlList = null;
        if (typeof crossDomainForward == "function") {
            crossDomainForward()
        }
    };
    this.crossDomainAction = function (action, callback) {
        crossDomainTimer = setTimeout(me.name + ".crossDomainResult()", crossDomainTime * 1000);
        if (typeof callback == "function") {
            crossDomainForward = callback
        } else {
            crossDomainForward = null
        }
        if (crossDomainUrlList) {
            me.crossDomainCallBack(crossDomainUrlList);
            return false
        }
        var domain = me.domain;
        if (action == "update") {
            action = "login";
            domain = "sina.com.cn"
        }
        var request = {
            scriptId: me.ssoCrossDomainScriptId,
            callback: me.name + ".crossDomainCallBack",
            action: action,
            domain: domain,
            sr: window.screen.width + "*" + window.screen.height
        };
        var url = makeURL(ssoCrosssDomainUrl, request);
        excuteScript(me.ssoCrossDomainScriptId, url)
    };
    this.checkLoginState = function (callback) {
        if (callback) {
            me.autoLogin(callback)
        } else {
            me.autoLogin(function (cookieinfo) {
                var loginStatus = {};
                if (cookieinfo !== null) {
                    var userinfo = {displayname: cookieinfo.nick, uniqueid: cookieinfo.uid, userid: cookieinfo.user};
                    loginStatus.result = true;
                    loginStatus.userinfo = userinfo
                } else {
                    loginStatus.result = false;
                    loginStatus.reason = ""
                }
                me.callbackLoginStatus(loginStatus)
            })
        }
    };
    this.getCookieExpireTime = function () {
        return getCookieExpireTimeByDomain(me.domain)
    };
    this.getSinaCookie = function (strict) {
        var sup = urldecode(getCookie("SUP"));
        if (!sup && !urldecode(getCookie("ALF"))) {
            return null
        }
        if (!sup) {
            sup = urldecode(getCookie("SUR"))
        }
        if (!sup) {
            return null
        }
        var arrSup = parse_str(sup);
        if (strict && arrSup.et && (arrSup.et * 1000 < (new Date()).getTime())) {
            return null
        }
        return arrSup
    };
    this.get51UCCookie = function () {
        return me.getSinaCookie()
    };
    this.isPreLoginState = function () {
        var subp = getCookie("SUBP");
        if (!subp) {
            return false
        }
        var subp_obj = sinaSSOEncoder.getSUBPCookie.decode(subp);
        if (subp_obj && subp_obj.status == "40") {
            return true
        }
        return false
    };
    this.isVisitor = function () {
        var subp = getCookie("SUBP");
        if (!subp) {
            return false
        }
        var subp_obj = sinaSSOEncoder.getSUBPCookie.decode(subp);
        if (subp_obj && subp_obj.status == "20") {
            return true
        }
        return false
    };
    this.autoLogin = function (callback, strict) {
        if (me.domain == "sina.com.cn") {
            if (getCookie("SUP") === null && getCookie("ALF") !== null) {
                sinaAutoLogin(callback);
                return true
            }
        } else {
            if (getCookie("SUP") === null && (strict || getCookie("SSOLoginState") !== null || getCookie("ALF") !== null)) {
                sinaAutoLogin(callback);
                return true
            }
        }
        callback(me.getSinaCookie());
        return true
    };
    this.autoLoginCallBack2 = function (result) {
        try {
            autoLoginCallBack2(me.getSinaCookie())
        } catch (e) {
        }
        return true
    };
    this.appLogin = function (ticket, domain, callback) {
        var savestate = tmpData.savestate ? parseInt((new Date()).getTime() / 1000 + tmpData.savestate * 86400) : 0;
        var alf = getCookie("ALF") ? getCookie("ALF") : 0;
        var request = {callback: callback, ticket: ticket, ssosavestate: savestate || alf};
        var appLoginURL = me.appLoginURL[domain];
        var url = makeURL(appLoginURL, request);
        excuteScript(me.scriptId, url, "gb2312");
        return true
    };
    this.autoLoginCallBack3 = function (result) {
        if (result.retcode != 0) {
            me.autoLoginCallBack2(result);
            return false
        }
        var domain = me.domain == "sina.com.cn" ? "weibo.com" : me.domain;
        me.appLogin(result.ticket, domain, me.name + ".autoLoginCallBack2");
        return true
    };
    this.setLoginType = function (loginType) {
        var https = location.protocol == "https:" ? me.https : 0;
        if (https) {
            me.crossDomain = false
        }
        me.loginType = loginType | https;
        return true
    };
    this.setServerTime = function (servertime) {
        if (!ssoServerTimeTimer) {
            ssoServerTimeTimer = new prototypeTimer(true)
        }
        if (servertime == 0) {
            ssoServerTimeTimer.clear();
            me.servertime = servertime;
            return true
        }
        if (servertime < 1294935546) {
            return false
        }
        var calcServerTime = function () {
            if (me.servertime) {
                me.servertime += me.calcServerTimeInterval / 1000;
                ssoServerTimeTimer.start(me.calcServerTimeInterval, calcServerTime)
            }
        };
        me.servertime = servertime;
        ssoServerTimeTimer.start(me.calcServerTimeInterval, calcServerTime)
    };
    this.getPinCodeUrl = function (size) {
        if (size == undefined) {
            size = 0
        }
        if (pcid) {
            me.loginExtraQuery.pcid = pcid
        }
        var url = location.protocol == "https:" ? pincodeUrl.replace(/^http:/, "https:") : pincodeUrl;
        return url + "?r=" + Math.floor(Math.random() * 100000000) + "&s=" + size + (pcid.length > 0 ? "&p=" + pcid : "")
    };
    this.showPinCode = function (id) {
        me.$(id).src = me.getPinCodeUrl()
    };
    this.isVfValid = function () {
        return me.getSinaCookie(true)["vf"] != 1
    };
    this.getVfValidUrl = function () {
        return vfValidUrl
    };
    this.enableFailRedirect = function () {
        me.failRedirect = true
    };
    var makeNonce = function (len) {
        var x = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        var str = "";
        for (var i = 0; i < len; i++) {
            str += x.charAt(Math.ceil(Math.random() * 1000000) % x.length)
        }
        return str
    };
    var sinaAutoLogin = function (callback) {
        autoLoginCallBack2 = callback;
        var request = {
            entry: me.getEntry(),
            service: me.service,
            encoding: "UTF-8",
            gateway: 1,
            returntype: "TEXT",
            from: me.from
        };
        if (me.domain == "sina.com.cn") {
            request.callback = me.name + ".autoLoginCallBack3";
            request.service = "miniblog";
            request.useticket = 1
        } else {
            request.callback = me.name + ".autoLoginCallBack3";
            request.useticket = 1
        }
        var url = location.protocol == "https:" ? ssoLoginUrl.replace(/^http:/, "https:") : ssoLoginUrl;
        url = makeURL(url, request);
        excuteScript(me.scriptId, url, "gb2312");
        return true
    };
    var getCookieExpireTimeByDomain = function (domain) {
        var expireTime = null;
        var cookie = null;
        cookie = me.getSinaCookie();
        if (cookie) {
            expireTime = cookie.et
        }
        return expireTime
    };
    var addEventListener = function (dom, eventName, fn) {
        if (dom.addEventListener) {
            dom.addEventListener(eventName, fn, false)
        } else {
            if (dom.attachEvent) {
                dom.attachEvent("on" + eventName, fn)
            } else {
                dom["on" + eventName] = fn
            }
        }
    };
    var prototypeTimer = function (enable) {
        var mytimer = false;
        this.start = function (timeout, callback) {
            if (enable) {
                mytimer = setTimeout(callback, timeout)
            }
        };
        this.clear = function (name) {
            if (enable) {
                clearTimeout(mytimer);
                mytimer = false
            }
        };
        this.isset = function () {
            return mytimer !== false
        }
    };
    var excuteScript = function (id, scriptSource, charset) {
        removeNode(id);
        var head = document.getElementsByTagName("head")[0];
        var newScript = document.createElement("script");
        newScript.charset = charset || "gb2312";
        newScript.id = id;
        newScript.type = "text/javascript";
        newScript.src = makeURL(scriptSource, {client: me.getClientType(), _: (new Date()).getTime()});
        head.appendChild(newScript)
    };
    var excuteIframe = function (id, url) {
        removeNode(id);
        var bodyel = document.getElementsByTagName("body")[0];
        var new_iframe = document.createElement("iframe");
        new_iframe.style.display = "none";
        new_iframe.src = makeURL(url, {client: me.getClientType(), _: (new Date()).getTime()});
        new_iframe.isReady = false;
        addEventListener(new_iframe, "load", function () {
            if (new_iframe.isReady) {
                return
            }
            new_iframe.isReady = true;
            me.doCrossDomainCallBack({scriptId: id})
        });
        bodyel.appendChild(new_iframe)
    };
    var makeRequest = function (username, password, savestate) {
        var request = {
            entry: me.getEntry(),
            gateway: 1,
            from: me.from,
            savestate: savestate,
            useticket: me.useTicket ? 1 : 0
        };
        if (me.failRedirect) {
            me.loginExtraQuery.frd = 1
        }
        request = objMerge(request, {pagerefer: document.referrer || ""});
        request = objMerge(request, me.loginExtraFlag);
        request = objMerge(request, me.loginExtraQuery);
        request.su = sinaSSOEncoder.base64.encode(urlencode(username));
        if (me.service) {
            request.service = me.service
        }
        if ((me.loginType & rsa) && me.servertime && sinaSSOEncoder && sinaSSOEncoder.RSAKey) {
            request.servertime = me.servertime;
            request.nonce = me.nonce;
            request.pwencode = "rsa2";
            request.rsakv = me.rsakv;
            var RSAKey = new sinaSSOEncoder.RSAKey();
            RSAKey.setPublic(me.rsaPubkey, "10001");
            password = RSAKey.encrypt([me.servertime, me.nonce].join("\t") + "\n" + password)
        } else {
            if ((me.loginType & wsse) && me.servertime && sinaSSOEncoder && sinaSSOEncoder.hex_sha1) {
                request.servertime = me.servertime;
                request.nonce = me.nonce;
                request.pwencode = "wsse";
                password = sinaSSOEncoder.hex_sha1("" + sinaSSOEncoder.hex_sha1(sinaSSOEncoder.hex_sha1(password)) + me.servertime + me.nonce)
            }
        }
        request.sp = password;
        try {
            request.sr = window.screen.width + "*" + window.screen.height
        } catch (e) {
        }
        return request
    };
    var loginByXMLHttpRequest = function (username, password, savestate) {
        if (typeof XMLHttpRequest == "undefined") {
            return false
        }
        var xhr = new XMLHttpRequest();
        if (!"withCredentials" in xhr) {
            return false
        }
        var request = makeXMLRequestQuery(username, password, savestate);
        var url = (me.loginType & https) ? ssoLoginUrl.replace(/^http:/, "https:") : ssoLoginUrl;
        url = makeURL(url, {client: me.getClientType(), _: (new Date()).getTime()});
        try {
            xhr.open("POST", url, true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.withCredentials = true;
            xhr.onreadystatechange = function () {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    me.loginCallBack(parseJSON(xhr.responseText))
                }
            };
            xhr.send(httpBuildQuery(request))
        } catch (e) {
            return false
        }
        return true
    };
    var makeXMLRequestQuery = function (username, password, savestate) {
        if (me.appLoginURL[me.domain]) {
            me.useTicket = 1;
            me.service = me.appDomainService[me.domain] || me.service
        }
        var cdult = 0;
        if (me.domain) {
            cdult = 2
        }
        if (!me.appLoginURL[me.domain]) {
            cdult = 3
        }
        if (me.cdult !== false) {
            cdult = me.cdult
        }
        if (cdult == 3) {
            crossDomainTime = me.crossDomainTime;
            delete me.appLoginURL[me.domain]
        }
        var request = makeRequest(username, password, savestate);
        return objMerge(request, {
            encoding: "UTF-8",
            cdult: cdult,
            domain: me.domain,
            useticket: me.appLoginURL[me.domain] ? 1 : 0,
            prelt: preloginTime,
            returntype: "TEXT"
        })
    };
    var loginByScript = function (username, password, savestate) {
        var request = makeXMLRequestQuery(username, password, savestate);
        request = objMerge(request, {callback: me.name + ".loginCallBack"});
        var url = (me.loginType & https) ? ssoLoginUrl.replace(/^http:/, "https:") : ssoLoginUrl;
        url = makeURL(url, request);
        excuteScript(me.scriptId, url, "gb2312")
    };
    var loginByIframe = function (username, password, savestate) {
        createIFrame(me.loginFrameName);
        var loginForm = createForm(me.loginFormId);
        var request = makeRequest(username, password, savestate);
        request.encoding = "UTF-8";
        if (me.crossDomain == false) {
            request.crossdomain = 0
        }
        request.prelt = preloginTime;
        if (me.feedBackUrl) {
            request.url = makeURL(me.feedBackUrl, {
                framelogin: 1,
                callback: "parent." + me.name + ".feedBackUrlCallBack"
            });
            request.returntype = "META"
        } else {
            request.callback = "parent." + me.name + ".loginCallBack";
            request.returntype = "IFRAME";
            request.setdomain = me.setDomain ? 1 : 0
        }
        for (var key in me.loginExtraQuery) {
            if (typeof me.loginExtraQuery[key] == "function") {
                continue
            }
            request[key] = me.loginExtraQuery[key]
        }
        for (var name in request) {
            loginForm.addInput(name, request[name])
        }
        var action = (me.loginType & https) ? ssoLoginUrl.replace(/^http:/, "https:") : ssoLoginUrl;
        action = makeURL(action, objMerge({client: me.getClientType()}, me.loginExtraFlag));
        loginForm.method = "post";
        loginForm.action = action;
        loginForm.target = me.loginFrameName;
        var result = true;
        try {
            loginForm.submit()
        } catch (e) {
            removeNode(me.loginFrameName);
            result = false
        }
        setTimeout(function () {
            removeNode(loginForm)
        }, 10);
        return result
    };
    var createIFrame = function (frameName, src) {
        if (src == null) {
            src = "javascript:false;"
        }
        removeNode(frameName);
        var frame = document.createElement("iframe");
        frame.height = 0;
        frame.width = 0;
        frame.style.display = "none";
        frame.name = frameName;
        frame.id = frameName;
        frame.src = src;
        appendChild(document.body, frame);
        window.frames[frameName].name = frameName;
        return frame
    };
    var createForm = function (formName, display) {
        if (display == null) {
            display = "none"
        }
        removeNode(formName);
        var form = document.createElement("form");
        form.height = 0;
        form.width = 0;
        form.style.display = display;
        form.name = formName;
        form.id = formName;
        appendChild(document.body, form);
        document.forms[formName].name = formName;
        form.addInput = function (name, value, type) {
            if (type == null) {
                type = "text"
            }
            var _name = this.getElementsByTagName("input")[name];
            if (_name) {
                this.removeChild(_name)
            }
            _name = document.createElement("input");
            this.appendChild(_name);
            _name.id = name;
            _name.name = name;
            _name.type = type;
            _name.value = value
        };
        return form
    };
    var removeNode = function (el) {
        try {
            if (typeof(el) === "string") {
                el = me.$(el)
            }
            el.parentNode.removeChild(el)
        } catch (e) {
        }
    };
    var getType = function (item) {
        if (typeof(item) === "undefined") {
            return "undefined"
        }
        if (item === null) {
            return "null"
        }
        return Object.prototype.toString.call(item).replace(/^\[object\s|\]$/gi, "").toLowerCase()
    };
    var isSafari = function () {
        var browserName = navigator.userAgent.toLowerCase();
        return ((/webkit/i).test(browserName) && !(/chrome/i).test(browserName))
    };
    var appendChild = function (parentObj, element) {
        parentObj.appendChild(element)
    };
    var getCookie = function (name) {
        var Res = (new RegExp(name + "=([^;]+)")).exec(document.cookie);
        return Res == null ? null : Res[1]
    };
    var makeURL = function (url, request) {
        return url + urlAndChar(url) + httpBuildQuery(request)
    };
    var urlAndChar = function (url) {
        return (/\?/.test(url) ? "&" : "?")
    };
    var urlencode = function (str) {
        return encodeURIComponent(str)
    };
    var urldecode = function (str) {
        if (str == null) {
            return ""
        } else {
            try {
                return decodeURIComponent(str)
            } catch (e) {
                return ""
            }
        }
    };
    var httpBuildQuery = function (obj) {
        if (typeof obj != "object") {
            return ""
        }
        var arr = new Array();
        for (var key in obj) {
            if (typeof obj[key] == "function") {
                continue
            }
            arr.push(key + "=" + urlencode(obj[key]))
        }
        return arr.join("&")
    };
    var parse_str = function (str) {
        var arr = str.split("&");
        var arrtmp;
        var arrResult = {};
        for (var i = 0; i < arr.length; i++) {
            arrtmp = arr[i].split("=");
            arrResult[arrtmp[0]] = urldecode(arrtmp[1])
        }
        return arrResult
    };
    var parseJSON = function (str) {
        if (typeof(str) === "object") {
            return str
        } else {
            if (window.JSON) {
                return JSON.parse(str)
            } else {
                return eval("(" + str + ")")
            }
        }
    };
    var objMerge = function (obj1, obj2) {
        for (var item in obj2) {
            obj1[item] = obj2[item]
        }
        return obj1
    };
    this.$ = function (id) {
        return document.getElementById(id)
    };
    this.generateVisitor = function () {
        var reg, domainValid = false;
        for (var i = 0; i < this.generateVisitorDomain.length; i++) {
            reg = new RegExp(this.generateVisitorDomain[i]);
            if (reg.test(document.domain)) {
                domainValid = true;
                break
            }
        }
        if (!domainValid) {
            return false
        }
        try {
            if (me.shouldGenerateVisitor() && !me.$("visitorfrm84747h4784")) {
                document.body.insertAdjacentHTML("beforeEnd", "<iframe id='visitorfrm84747h4784' style='position:absolute;left:0;top:0;border:none;width:1px;height:1px' src='" + generateVisitorUrl + "?from=iframe'/>");
                setTimeout(function () {
                    try {
                        var ifr = me.$("visitorfrm84747h4784");
                        if (ifr) {
                            ifr.parentNode.removeChild(ifr)
                        }
                    } catch (e) {
                    }
                }, 1000 * 30)
            }
        } catch (e) {
            return false
        }
        return true
    };
    this.shouldGenerateVisitor = function () {
        var is_subp_exists = false;
        var is_sup_exists = false;
        var subp = getCookie("SUBP");
        if (subp) {
            is_subp_exists = true
        }
        var sup = getCookie("SUP");
        if (sup) {
            is_sup_exists = true
        }
        if (!is_subp_exists && !is_sup_exists) {
            return true
        }
        return false
    }
}
var sinaSSOEncoder = sinaSSOEncoder || {};
(function () {
    var k = 0;
    var h = 8;
    this.hex_sha1 = function (l) {
        return i(c(g(l), l.length * h))
    };
    var c = function (B, s) {
        B[s >> 5] |= 128 << (24 - s % 32);
        B[((s + 64 >> 9) << 4) + 15] = s;
        var C = Array(80);
        var A = 1732584193;
        var z = -271733879;
        var y = -1732584194;
        var v = 271733878;
        var u = -1009589776;
        for (var p = 0; p < B.length; p += 16) {
            var r = A;
            var q = z;
            var o = y;
            var n = v;
            var l = u;
            for (var m = 0; m < 80; m++) {
                if (m < 16) {
                    C[m] = B[p + m]
                } else {
                    C[m] = e(C[m - 3] ^ C[m - 8] ^ C[m - 14] ^ C[m - 16], 1)
                }
                var D = f(f(e(A, 5), a(m, z, y, v)), f(f(u, C[m]), d(m)));
                u = v;
                v = y;
                y = e(z, 30);
                z = A;
                A = D
            }
            A = f(A, r);
            z = f(z, q);
            y = f(y, o);
            v = f(v, n);
            u = f(u, l)
        }
        return Array(A, z, y, v, u)
    };
    var a = function (m, l, o, n) {
        if (m < 20) {
            return (l & o) | ((~l) & n)
        }
        if (m < 40) {
            return l ^ o ^ n
        }
        if (m < 60) {
            return (l & o) | (l & n) | (o & n)
        }
        return l ^ o ^ n
    };
    var d = function (l) {
        return (l < 20) ? 1518500249 : (l < 40) ? 1859775393 : (l < 60) ? -1894007588 : -899497514
    };
    var f = function (l, o) {
        var n = (l & 65535) + (o & 65535);
        var m = (l >> 16) + (o >> 16) + (n >> 16);
        return (m << 16) | (n & 65535)
    };
    var e = function (l, m) {
        return (l << m) | (l >>> (32 - m))
    };
    var g = function (o) {
        var n = Array();
        var l = (1 << h) - 1;
        for (var m = 0; m < o.length * h; m += h) {
            n[m >> 5] |= (o.charCodeAt(m / h) & l) << (24 - m % 32)
        }
        return n
    };
    var i = function (n) {
        var m = k ? "0123456789ABCDEF" : "0123456789abcdef";
        var o = "";
        for (var l = 0; l < n.length * 4; l++) {
            o += m.charAt((n[l >> 2] >> ((3 - l % 4) * 8 + 4)) & 15) + m.charAt((n[l >> 2] >> ((3 - l % 4) * 8)) & 15)
        }
        return o
    };
    var j = function (l) {
        var m = "", n = 0;
        for (; n < l.length; n++) {
            m += "%" + b(l[n])
        }
        return decodeURIComponent(m)
    };
    var b = function (l) {
        var m = "0" + l.toString(16);
        return m.length <= 2 ? m : m.substr(1)
    };
    this.base64 = {
        encode: function (n) {
            n = "" + n;
            if (n == "") {
                return ""
            }
            var l = "";
            var u, s, q = "";
            var t, r, p, o = "";
            var m = 0;
            do {
                u = n.charCodeAt(m++);
                s = n.charCodeAt(m++);
                q = n.charCodeAt(m++);
                t = u >> 2;
                r = ((u & 3) << 4) | (s >> 4);
                p = ((s & 15) << 2) | (q >> 6);
                o = q & 63;
                if (isNaN(s)) {
                    p = o = 64
                } else {
                    if (isNaN(q)) {
                        o = 64
                    }
                }
                l = l + this._keys.charAt(t) + this._keys.charAt(r) + this._keys.charAt(p) + this._keys.charAt(o);
                u = s = q = "";
                t = r = p = o = ""
            } while (m < n.length);
            return l
        },
        decode: function (t, q, m) {
            var s = function (C, E) {
                for (var D = 0; D < C.length; D++) {
                    if (C[D] === E) {
                        return D
                    }
                }
                return -1
            };
            if (typeof(t) == "string") {
                t = t.split("")
            }
            var n = [];
            var B, z, w = "";
            var A, y, v, u = "";
            if (t.length % 4 != 0) {
            }
            var l = /[^A-Za-z0-9+\/=]/;
            var x = this._keys.split("");
            if (q == "urlsafe") {
                l = /[^A-Za-z0-9-_=]/;
                x = this._keys_urlsafe.split("")
            }
            if (q == "subp_v2") {
                l = /[^A-Za-z0-9_=-]/;
                x = this._subp_v2_keys.split("")
            }
            if (q == "subp_v3_3") {
                l = /[^A-Za-z0-9-_.-]/;
                x = this._subp_v3_keys_3.split("")
            }
            var p = 0;
            if (q == "binnary") {
                x = [];
                for (p = 0; p <= 64; p++) {
                    x[p] = p + 128
                }
            }
            if (q != "binnary" && l.test(t.join(""))) {
                return m == "array" ? [] : ""
            }
            p = 0;
            do {
                A = s(x, t[p++]);
                y = s(x, t[p++]);
                v = s(x, t[p++]);
                u = s(x, t[p++]);
                B = (A << 2) | (y >> 4);
                z = ((y & 15) << 4) | (v >> 2);
                w = ((v & 3) << 6) | u;
                n.push(B);
                if (v != 64 && v != -1) {
                    n.push(z)
                }
                if (u != 64 && u != -1) {
                    n.push(w)
                }
                B = z = w = "";
                A = y = v = u = ""
            } while (p < t.length);
            if (m == "array") {
                return n
            }
            var r = "", o = 0;
            for (; o < n.lenth; o++) {
                r += String.fromCharCode(n[o])
            }
            return r
        },
        _keys: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        _keys_urlsafe: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_=",
        _subp_v2_keys: "uAL715W8e3jJCcNU0lT_FSXVgxpbEDdQ4vKaIOH2GBPtfzqsmYZo-wRM9i6hynrk=",
        _subp_v3_keys_3: "5WFh28sGziZTeS1lBxCK-HgPq9IdMUwknybo.LJrQD3uj_Va7pE0XfcNR4AOYvm6t"
    };
    this.Cookie = {
        decode: function (o) {
            var n = [];
            var m = o.substr(0, 3);
            var l = o.substr(3);
            switch (m) {
                case"v01":
                    for (var p = 0; p < l.length; p += 2) {
                        n.push(parseInt(l.substr(p, 2), 16))
                    }
                    return decodeURIComponent(j(sinaSSOEncoder.base64.decode(n, "binnary", "array")));
                    break;
                case"v02":
                    l = l.replace(/\./g, "=");
                    n = sinaSSOEncoder.base64.decode(l, "urlsafe", "array");
                    return j(sinaSSOEncoder.base64.decode(n, "binnary", "array"));
                default:
                    return decodeURIComponent(o)
            }
        }
    };
    this.getSUBPCookie = {
        __parse: function (o) {
            var y, m, p, n, x, r = 0, q, t = {}, l = "", u = "";
            if (!o) {
                return t
            }
            do {
                m = o[r];
                y = ++r;
                for (q = r; q < m + y; q++, r++) {
                    l += String.fromCharCode(o[q])
                }
                n = o[r];
                y = ++r;
                if (l == "status" || l == "flag") {
                    for (q = r; q < n + y; q++, r++) {
                        u += o[q]
                    }
                } else {
                    u = o.slice(q, n + y);
                    try {
                        u = j(u)
                    } catch (w) {
                        u = ""
                    }
                    r += n
                }
                t[l] = u;
                l = "";
                u = ""
            } while (r < o.length);
            return t
        }, decode: function (o) {
            var n = [], p, m = o.substr(0, 3), l = decodeURIComponent(o.substr(3));
            switch (m) {
                case"002":
                    n = sinaSSOEncoder.base64.decode(l, "subp_v2", "array");
                    return sinaSSOEncoder.getSUBPCookie.__parse(n);
                case"003":
                    p = l.substr(0, 1);
                    l = l.substr(1);
                    n = sinaSSOEncoder.base64.decode(l, "subp_v3_" + p, "array");
                    return sinaSSOEncoder.getSUBPCookie.__parse(n);
                default:
                    return decodeURIComponent(o)
            }
        }
    }
}).call(sinaSSOEncoder);
(function () {
    var av;
    var ah = 244837814094590;
    var Y = ((ah & 16777215) == 15715070);

    function aq(z, t, az) {
        if (z != null) {
            if ("number" == typeof z) {
                this.fromNumber(z, t, az)
            } else {
                if (t == null && "string" != typeof z) {
                    this.fromString(z, 256)
                } else {
                    this.fromString(z, t)
                }
            }
        }
    }

    function h() {
        return new aq(null)
    }

    function b(aB, t, z, aA, aD, aC) {
        while (--aC >= 0) {
            var az = t * this[aB++] + z[aA] + aD;
            aD = Math.floor(az / 67108864);
            z[aA++] = az & 67108863
        }
        return aD
    }

    function ax(aB, aG, aH, aA, aE, t) {
        var aD = aG & 32767, aF = aG >> 15;
        while (--t >= 0) {
            var az = this[aB] & 32767;
            var aC = this[aB++] >> 15;
            var z = aF * az + aC * aD;
            az = aD * az + ((z & 32767) << 15) + aH[aA] + (aE & 1073741823);
            aE = (az >>> 30) + (z >>> 15) + aF * aC + (aE >>> 30);
            aH[aA++] = az & 1073741823
        }
        return aE
    }

    function aw(aB, aG, aH, aA, aE, t) {
        var aD = aG & 16383, aF = aG >> 14;
        while (--t >= 0) {
            var az = this[aB] & 16383;
            var aC = this[aB++] >> 14;
            var z = aF * az + aC * aD;
            az = aD * az + ((z & 16383) << 14) + aH[aA] + aE;
            aE = (az >> 28) + (z >> 14) + aF * aC;
            aH[aA++] = az & 268435455
        }
        return aE
    }

    if (Y && (navigator.appName == "Microsoft Internet Explorer")) {
        aq.prototype.am = ax;
        av = 30
    } else {
        if (Y && (navigator.appName != "Netscape")) {
            aq.prototype.am = b;
            av = 26
        } else {
            aq.prototype.am = aw;
            av = 28
        }
    }
    aq.prototype.DB = av;
    aq.prototype.DM = ((1 << av) - 1);
    aq.prototype.DV = (1 << av);
    var Z = 52;
    aq.prototype.FV = Math.pow(2, Z);
    aq.prototype.F1 = Z - av;
    aq.prototype.F2 = 2 * av - Z;
    var ad = "0123456789abcdefghijklmnopqrstuvwxyz";
    var af = new Array();
    var ao, v;
    ao = "0".charCodeAt(0);
    for (v = 0; v <= 9; ++v) {
        af[ao++] = v
    }
    ao = "a".charCodeAt(0);
    for (v = 10; v < 36; ++v) {
        af[ao++] = v
    }
    ao = "A".charCodeAt(0);
    for (v = 10; v < 36; ++v) {
        af[ao++] = v
    }
    function ay(t) {
        return ad.charAt(t)
    }

    function A(z, t) {
        var az = af[z.charCodeAt(t)];
        return (az == null) ? -1 : az
    }

    function X(z) {
        for (var t = this.t - 1; t >= 0; --t) {
            z[t] = this[t]
        }
        z.t = this.t;
        z.s = this.s
    }

    function n(t) {
        this.t = 1;
        this.s = (t < 0) ? -1 : 0;
        if (t > 0) {
            this[0] = t
        } else {
            if (t < -1) {
                this[0] = t + DV
            } else {
                this.t = 0
            }
        }
    }

    function c(t) {
        var z = h();
        z.fromInt(t);
        return z
    }

    function w(aD, z) {
        var aA;
        if (z == 16) {
            aA = 4
        } else {
            if (z == 8) {
                aA = 3
            } else {
                if (z == 256) {
                    aA = 8
                } else {
                    if (z == 2) {
                        aA = 1
                    } else {
                        if (z == 32) {
                            aA = 5
                        } else {
                            if (z == 4) {
                                aA = 2
                            } else {
                                this.fromRadix(aD, z);
                                return
                            }
                        }
                    }
                }
            }
        }
        this.t = 0;
        this.s = 0;
        var aC = aD.length, az = false, aB = 0;
        while (--aC >= 0) {
            var t = (aA == 8) ? aD[aC] & 255 : A(aD, aC);
            if (t < 0) {
                if (aD.charAt(aC) == "-") {
                    az = true
                }
                continue
            }
            az = false;
            if (aB == 0) {
                this[this.t++] = t
            } else {
                if (aB + aA > this.DB) {
                    this[this.t - 1] |= (t & ((1 << (this.DB - aB)) - 1)) << aB;
                    this[this.t++] = (t >> (this.DB - aB))
                } else {
                    this[this.t - 1] |= t << aB
                }
            }
            aB += aA;
            if (aB >= this.DB) {
                aB -= this.DB
            }
        }
        if (aA == 8 && (aD[0] & 128) != 0) {
            this.s = -1;
            if (aB > 0) {
                this[this.t - 1] |= ((1 << (this.DB - aB)) - 1) << aB
            }
        }
        this.clamp();
        if (az) {
            aq.ZERO.subTo(this, this)
        }
    }

    function O() {
        var t = this.s & this.DM;
        while (this.t > 0 && this[this.t - 1] == t) {
            --this.t
        }
    }

    function q(z) {
        if (this.s < 0) {
            return "-" + this.negate().toString(z)
        }
        var az;
        if (z == 16) {
            az = 4
        } else {
            if (z == 8) {
                az = 3
            } else {
                if (z == 2) {
                    az = 1
                } else {
                    if (z == 32) {
                        az = 5
                    } else {
                        if (z == 4) {
                            az = 2
                        } else {
                            return this.toRadix(z)
                        }
                    }
                }
            }
        }
        var aB = (1 << az) - 1, aE, t = false, aC = "", aA = this.t;
        var aD = this.DB - (aA * this.DB) % az;
        if (aA-- > 0) {
            if (aD < this.DB && (aE = this[aA] >> aD) > 0) {
                t = true;
                aC = ay(aE)
            }
            while (aA >= 0) {
                if (aD < az) {
                    aE = (this[aA] & ((1 << aD) - 1)) << (az - aD);
                    aE |= this[--aA] >> (aD += this.DB - az)
                } else {
                    aE = (this[aA] >> (aD -= az)) & aB;
                    if (aD <= 0) {
                        aD += this.DB;
                        --aA
                    }
                }
                if (aE > 0) {
                    t = true
                }
                if (t) {
                    aC += ay(aE)
                }
            }
        }
        return t ? aC : "0"
    }

    function R() {
        var t = h();
        aq.ZERO.subTo(this, t);
        return t
    }

    function ak() {
        return (this.s < 0) ? this.negate() : this
    }

    function G(t) {
        var az = this.s - t.s;
        if (az != 0) {
            return az
        }
        var z = this.t;
        az = z - t.t;
        if (az != 0) {
            return az
        }
        while (--z >= 0) {
            if ((az = this[z] - t[z]) != 0) {
                return az
            }
        }
        return 0
    }

    function j(z) {
        var aA = 1, az;
        if ((az = z >>> 16) != 0) {
            z = az;
            aA += 16
        }
        if ((az = z >> 8) != 0) {
            z = az;
            aA += 8
        }
        if ((az = z >> 4) != 0) {
            z = az;
            aA += 4
        }
        if ((az = z >> 2) != 0) {
            z = az;
            aA += 2
        }
        if ((az = z >> 1) != 0) {
            z = az;
            aA += 1
        }
        return aA
    }

    function u() {
        if (this.t <= 0) {
            return 0
        }
        return this.DB * (this.t - 1) + j(this[this.t - 1] ^ (this.s & this.DM))
    }

    function ap(az, z) {
        var t;
        for (t = this.t - 1; t >= 0; --t) {
            z[t + az] = this[t]
        }
        for (t = az - 1; t >= 0; --t) {
            z[t] = 0
        }
        z.t = this.t + az;
        z.s = this.s
    }

    function W(az, z) {
        for (var t = az; t < this.t; ++t) {
            z[t - az] = this[t]
        }
        z.t = Math.max(this.t - az, 0);
        z.s = this.s
    }

    function s(aE, aA) {
        var z = aE % this.DB;
        var t = this.DB - z;
        var aC = (1 << t) - 1;
        var aB = Math.floor(aE / this.DB), aD = (this.s << z) & this.DM, az;
        for (az = this.t - 1; az >= 0; --az) {
            aA[az + aB + 1] = (this[az] >> t) | aD;
            aD = (this[az] & aC) << z
        }
        for (az = aB - 1; az >= 0; --az) {
            aA[az] = 0
        }
        aA[aB] = aD;
        aA.t = this.t + aB + 1;
        aA.s = this.s;
        aA.clamp()
    }

    function l(aD, aA) {
        aA.s = this.s;
        var aB = Math.floor(aD / this.DB);
        if (aB >= this.t) {
            aA.t = 0;
            return
        }
        var z = aD % this.DB;
        var t = this.DB - z;
        var aC = (1 << z) - 1;
        aA[0] = this[aB] >> z;
        for (var az = aB + 1; az < this.t; ++az) {
            aA[az - aB - 1] |= (this[az] & aC) << t;
            aA[az - aB] = this[az] >> z
        }
        if (z > 0) {
            aA[this.t - aB - 1] |= (this.s & aC) << t
        }
        aA.t = this.t - aB;
        aA.clamp()
    }

    function aa(z, aA) {
        var az = 0, aB = 0, t = Math.min(z.t, this.t);
        while (az < t) {
            aB += this[az] - z[az];
            aA[az++] = aB & this.DM;
            aB >>= this.DB
        }
        if (z.t < this.t) {
            aB -= z.s;
            while (az < this.t) {
                aB += this[az];
                aA[az++] = aB & this.DM;
                aB >>= this.DB
            }
            aB += this.s
        } else {
            aB += this.s;
            while (az < z.t) {
                aB -= z[az];
                aA[az++] = aB & this.DM;
                aB >>= this.DB
            }
            aB -= z.s
        }
        aA.s = (aB < 0) ? -1 : 0;
        if (aB < -1) {
            aA[az++] = this.DV + aB
        } else {
            if (aB > 0) {
                aA[az++] = aB
            }
        }
        aA.t = az;
        aA.clamp()
    }

    function D(z, aA) {
        var t = this.abs(), aB = z.abs();
        var az = t.t;
        aA.t = az + aB.t;
        while (--az >= 0) {
            aA[az] = 0
        }
        for (az = 0; az < aB.t; ++az) {
            aA[az + t.t] = t.am(0, aB[az], aA, az, 0, t.t)
        }
        aA.s = 0;
        aA.clamp();
        if (this.s != z.s) {
            aq.ZERO.subTo(aA, aA)
        }
    }

    function Q(az) {
        var t = this.abs();
        var z = az.t = 2 * t.t;
        while (--z >= 0) {
            az[z] = 0
        }
        for (z = 0; z < t.t - 1; ++z) {
            var aA = t.am(z, t[z], az, 2 * z, 0, 1);
            if ((az[z + t.t] += t.am(z + 1, 2 * t[z], az, 2 * z + 1, aA, t.t - z - 1)) >= t.DV) {
                az[z + t.t] -= t.DV;
                az[z + t.t + 1] = 1
            }
        }
        if (az.t > 0) {
            az[az.t - 1] += t.am(z, t[z], az, 2 * z, 0, 1)
        }
        az.s = 0;
        az.clamp()
    }

    function E(aH, aE, aD) {
        var aN = aH.abs();
        if (aN.t <= 0) {
            return
        }
        var aF = this.abs();
        if (aF.t < aN.t) {
            if (aE != null) {
                aE.fromInt(0)
            }
            if (aD != null) {
                this.copyTo(aD)
            }
            return
        }
        if (aD == null) {
            aD = h()
        }
        var aB = h(), z = this.s, aG = aH.s;
        var aM = this.DB - j(aN[aN.t - 1]);
        if (aM > 0) {
            aN.lShiftTo(aM, aB);
            aF.lShiftTo(aM, aD)
        } else {
            aN.copyTo(aB);
            aF.copyTo(aD)
        }
        var aJ = aB.t;
        var az = aB[aJ - 1];
        if (az == 0) {
            return
        }
        var aI = az * (1 << this.F1) + ((aJ > 1) ? aB[aJ - 2] >> this.F2 : 0);
        var aQ = this.FV / aI, aP = (1 << this.F1) / aI, aO = 1 << this.F2;
        var aL = aD.t, aK = aL - aJ, aC = (aE == null) ? h() : aE;
        aB.dlShiftTo(aK, aC);
        if (aD.compareTo(aC) >= 0) {
            aD[aD.t++] = 1;
            aD.subTo(aC, aD)
        }
        aq.ONE.dlShiftTo(aJ, aC);
        aC.subTo(aB, aB);
        while (aB.t < aJ) {
            aB[aB.t++] = 0
        }
        while (--aK >= 0) {
            var aA = (aD[--aL] == az) ? this.DM : Math.floor(aD[aL] * aQ + (aD[aL - 1] + aO) * aP);
            if ((aD[aL] += aB.am(0, aA, aD, aK, 0, aJ)) < aA) {
                aB.dlShiftTo(aK, aC);
                aD.subTo(aC, aD);
                while (aD[aL] < --aA) {
                    aD.subTo(aC, aD)
                }
            }
        }
        if (aE != null) {
            aD.drShiftTo(aJ, aE);
            if (z != aG) {
                aq.ZERO.subTo(aE, aE)
            }
        }
        aD.t = aJ;
        aD.clamp();
        if (aM > 0) {
            aD.rShiftTo(aM, aD)
        }
        if (z < 0) {
            aq.ZERO.subTo(aD, aD)
        }
    }

    function N(t) {
        var z = h();
        this.abs().divRemTo(t, null, z);
        if (this.s < 0 && z.compareTo(aq.ZERO) > 0) {
            t.subTo(z, z)
        }
        return z
    }

    function K(t) {
        this.m = t
    }

    function U(t) {
        if (t.s < 0 || t.compareTo(this.m) >= 0) {
            return t.mod(this.m)
        } else {
            return t
        }
    }

    function aj(t) {
        return t
    }

    function J(t) {
        t.divRemTo(this.m, null, t)
    }

    function H(t, az, z) {
        t.multiplyTo(az, z);
        this.reduce(z)
    }

    function at(t, z) {
        t.squareTo(z);
        this.reduce(z)
    }

    K.prototype.convert = U;
    K.prototype.revert = aj;
    K.prototype.reduce = J;
    K.prototype.mulTo = H;
    K.prototype.sqrTo = at;
    function B() {
        if (this.t < 1) {
            return 0
        }
        var t = this[0];
        if ((t & 1) == 0) {
            return 0
        }
        var z = t & 3;
        z = (z * (2 - (t & 15) * z)) & 15;
        z = (z * (2 - (t & 255) * z)) & 255;
        z = (z * (2 - (((t & 65535) * z) & 65535))) & 65535;
        z = (z * (2 - t * z % this.DV)) % this.DV;
        return (z > 0) ? this.DV - z : -z
    }

    function f(t) {
        this.m = t;
        this.mp = t.invDigit();
        this.mpl = this.mp & 32767;
        this.mph = this.mp >> 15;
        this.um = (1 << (t.DB - 15)) - 1;
        this.mt2 = 2 * t.t
    }

    function ai(t) {
        var z = h();
        t.abs().dlShiftTo(this.m.t, z);
        z.divRemTo(this.m, null, z);
        if (t.s < 0 && z.compareTo(aq.ZERO) > 0) {
            this.m.subTo(z, z)
        }
        return z
    }

    function ar(t) {
        var z = h();
        t.copyTo(z);
        this.reduce(z);
        return z
    }

    function P(t) {
        while (t.t <= this.mt2) {
            t[t.t++] = 0
        }
        for (var az = 0; az < this.m.t; ++az) {
            var z = t[az] & 32767;
            var aA = (z * this.mpl + (((z * this.mph + (t[az] >> 15) * this.mpl) & this.um) << 15)) & t.DM;
            z = az + this.m.t;
            t[z] += this.m.am(0, aA, t, az, 0, this.m.t);
            while (t[z] >= t.DV) {
                t[z] -= t.DV;
                t[++z]++
            }
        }
        t.clamp();
        t.drShiftTo(this.m.t, t);
        if (t.compareTo(this.m) >= 0) {
            t.subTo(this.m, t)
        }
    }

    function al(t, z) {
        t.squareTo(z);
        this.reduce(z)
    }

    function y(t, az, z) {
        t.multiplyTo(az, z);
        this.reduce(z)
    }

    f.prototype.convert = ai;
    f.prototype.revert = ar;
    f.prototype.reduce = P;
    f.prototype.mulTo = y;
    f.prototype.sqrTo = al;
    function i() {
        return ((this.t > 0) ? (this[0] & 1) : this.s) == 0
    }

    function x(aE, aF) {
        if (aE > 4294967295 || aE < 1) {
            return aq.ONE
        }
        var aD = h(), az = h(), aC = aF.convert(this), aB = j(aE) - 1;
        aC.copyTo(aD);
        while (--aB >= 0) {
            aF.sqrTo(aD, az);
            if ((aE & (1 << aB)) > 0) {
                aF.mulTo(az, aC, aD)
            } else {
                var aA = aD;
                aD = az;
                az = aA
            }
        }
        return aF.revert(aD)
    }

    function am(az, t) {
        var aA;
        if (az < 256 || t.isEven()) {
            aA = new K(t)
        } else {
            aA = new f(t)
        }
        return this.exp(az, aA)
    }

    aq.prototype.copyTo = X;
    aq.prototype.fromInt = n;
    aq.prototype.fromString = w;
    aq.prototype.clamp = O;
    aq.prototype.dlShiftTo = ap;
    aq.prototype.drShiftTo = W;
    aq.prototype.lShiftTo = s;
    aq.prototype.rShiftTo = l;
    aq.prototype.subTo = aa;
    aq.prototype.multiplyTo = D;
    aq.prototype.squareTo = Q;
    aq.prototype.divRemTo = E;
    aq.prototype.invDigit = B;
    aq.prototype.isEven = i;
    aq.prototype.exp = x;
    aq.prototype.toString = q;
    aq.prototype.negate = R;
    aq.prototype.abs = ak;
    aq.prototype.compareTo = G;
    aq.prototype.bitLength = u;
    aq.prototype.mod = N;
    aq.prototype.modPowInt = am;
    aq.ZERO = c(0);
    aq.ONE = c(1);
    function k() {
        this.i = 0;
        this.j = 0;
        this.S = new Array()
    }

    function e(aB) {
        var aA, z, az;
        for (aA = 0; aA < 256; ++aA) {
            this.S[aA] = aA
        }
        z = 0;
        for (aA = 0; aA < 256; ++aA) {
            z = (z + this.S[aA] + aB[aA % aB.length]) & 255;
            az = this.S[aA];
            this.S[aA] = this.S[z];
            this.S[z] = az
        }
        this.i = 0;
        this.j = 0
    }

    function a() {
        var z;
        this.i = (this.i + 1) & 255;
        this.j = (this.j + this.S[this.i]) & 255;
        z = this.S[this.i];
        this.S[this.i] = this.S[this.j];
        this.S[this.j] = z;
        return this.S[(z + this.S[this.i]) & 255]
    }

    k.prototype.init = e;
    k.prototype.next = a;
    function an() {
        return new k()
    }

    var M = 256;
    var m;
    var T;
    var ab;

    function d(t) {
        T[ab++] ^= t & 255;
        T[ab++] ^= (t >> 8) & 255;
        T[ab++] ^= (t >> 16) & 255;
        T[ab++] ^= (t >> 24) & 255;
        if (ab >= M) {
            ab -= M
        }
    }

    function S() {
        d(new Date().getTime())
    }

    if (T == null) {
        T = new Array();
        ab = 0;
        var I;
        if (navigator.appName == "Netscape" && navigator.appVersion < "5" && window.crypto && typeof(window.crypto.random) === "function") {
            var F = window.crypto.random(32);
            for (I = 0; I < F.length; ++I) {
                T[ab++] = F.charCodeAt(I) & 255
            }
        }
        while (ab < M) {
            I = Math.floor(65536 * Math.random());
            T[ab++] = I >>> 8;
            T[ab++] = I & 255
        }
        ab = 0;
        S()
    }
    function C() {
        if (m == null) {
            S();
            m = an();
            m.init(T);
            for (ab = 0; ab < T.length; ++ab) {
                T[ab] = 0
            }
            ab = 0
        }
        return m.next()
    }

    function au(z) {
        var t;
        for (t = 0; t < z.length; ++t) {
            z[t] = C()
        }
    }

    function ac() {
    }

    ac.prototype.nextBytes = au;
    function g(z, t) {
        return new aq(z, t)
    }

    function ag(az, aA) {
        var t = "";
        var z = 0;
        while (z + aA < az.length) {
            t += az.substring(z, z + aA) + "\n";
            z += aA
        }
        return t + az.substring(z, az.length)
    }

    function r(t) {
        if (t < 16) {
            return "0" + t.toString(16)
        } else {
            return t.toString(16)
        }
    }

    function ae(aA, aD) {
        if (aD < aA.length + 11) {
            alert("Message too long for RSA");
            return null
        }
        var aC = new Array();
        var az = aA.length - 1;
        while (az >= 0 && aD > 0) {
            var aB = aA.charCodeAt(az--);
            if (aB < 128) {
                aC[--aD] = aB
            } else {
                if ((aB > 127) && (aB < 2048)) {
                    aC[--aD] = (aB & 63) | 128;
                    aC[--aD] = (aB >> 6) | 192
                } else {
                    aC[--aD] = (aB & 63) | 128;
                    aC[--aD] = ((aB >> 6) & 63) | 128;
                    aC[--aD] = (aB >> 12) | 224
                }
            }
        }
        aC[--aD] = 0;
        var z = new ac();
        var t = new Array();
        while (aD > 2) {
            t[0] = 0;
            while (t[0] == 0) {
                z.nextBytes(t)
            }
            aC[--aD] = t[0]
        }
        aC[--aD] = 2;
        aC[--aD] = 0;
        return new aq(aC)
    }

    function L() {
        this.n = null;
        this.e = 0;
        this.d = null;
        this.p = null;
        this.q = null;
        this.dmp1 = null;
        this.dmq1 = null;
        this.coeff = null
    }

    function o(z, t) {
        if (z != null && t != null && z.length > 0 && t.length > 0) {
            this.n = g(z, 16);
            this.e = parseInt(t, 16)
        } else {
            alert("Invalid RSA public key")
        }
    }

    function V(t) {
        return t.modPowInt(this.e, this.n)
    }

    function p(az) {
        var t = ae(az, (this.n.bitLength() + 7) >> 3);
        if (t == null) {
            return null
        }
        var aA = this.doPublic(t);
        if (aA == null) {
            return null
        }
        var z = aA.toString(16);
        if ((z.length & 1) == 0) {
            return z
        } else {
            return "0" + z
        }
    }

    L.prototype.doPublic = V;
    L.prototype.setPublic = o;
    L.prototype.encrypt = p;
    this.RSAKey = L
}).call(sinaSSOEncoder);


function get_name(name){
    return sinaSSOEncoder.base64.encode(name);
}


function get_pass(mypass,nonce,servertime,rsakey){
    var RSAKey = new sinaSSOEncoder.RSAKey();
    RSAKey.setPublic(rsakey, "10001");
    return RSAKey.encrypt([servertime, nonce].join("\t") + "\n" + mypass)
}
