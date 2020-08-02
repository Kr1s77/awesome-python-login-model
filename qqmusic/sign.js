function __sign_hash_20200305 (n) {
    function l(n, t) {
        var o = (65535 & n) + (65535 & t);
        return (n >> 16) + (t >> 16) + (o >> 16) << 16 | 65535 & o
    }
    function r(n, t, o, e, u, p) {
        return l((i = l(l(t, n), l(e, p))) << (r = u) | i >>> 32 - r, o);
        var i, r
    }
    function g(n, t, o, e, u, p, i) {
        return r(t & o | ~t & e, n, t, u, p, i)
    }
    function a(n, t, o, e, u, p, i) {
        return r(t & e | o & ~e, n, t, u, p, i)
    }
    function s(n, t, o, e, u, p, i) {
        return r(t ^ o ^ e, n, t, u, p, i)
    }
    function v(n, t, o, e, u, p, i) {
        return r(o ^ (t | ~e), n, t, u, p, i)
    }
    function t(n) {
        return function(n) {
            var t, o = "";
            for (t = 0; t < 32 * n.length; t += 8)
                o += String.fromCharCode(n[t >> 5] >>> t % 32 & 255);
            return o
        }(function(n, t) {
            n[t >> 5] |= 128 << t % 32,
            n[14 + (t + 64 >>> 9 << 4)] = t;
            var o, e, u, p, i, r = 1732584193, f = -271733879, h = -1732584194, c = 271733878;
            for (o = 0; o < n.length; o += 16)
                r = g(e = r, u = f, p = h, i = c, n[o], 7, -680876936),
                c = g(c, r, f, h, n[o + 1], 12, -389564586),
                h = g(h, c, r, f, n[o + 2], 17, 606105819),
                f = g(f, h, c, r, n[o + 3], 22, -1044525330),
                r = g(r, f, h, c, n[o + 4], 7, -176418897),
                c = g(c, r, f, h, n[o + 5], 12, 1200080426),
                h = g(h, c, r, f, n[o + 6], 17, -1473231341),
                f = g(f, h, c, r, n[o + 7], 22, -45705983),
                r = g(r, f, h, c, n[o + 8], 7, 1770035416),
                c = g(c, r, f, h, n[o + 9], 12, -1958414417),
                h = g(h, c, r, f, n[o + 10], 17, -42063),
                f = g(f, h, c, r, n[o + 11], 22, -1990404162),
                r = g(r, f, h, c, n[o + 12], 7, 1804603682),
                c = g(c, r, f, h, n[o + 13], 12, -40341101),
                h = g(h, c, r, f, n[o + 14], 17, -1502002290),
                r = a(r, f = g(f, h, c, r, n[o + 15], 22, 1236535329), h, c, n[o + 1], 5, -165796510),
                c = a(c, r, f, h, n[o + 6], 9, -1069501632),
                h = a(h, c, r, f, n[o + 11], 14, 643717713),
                f = a(f, h, c, r, n[o], 20, -373897302),
                r = a(r, f, h, c, n[o + 5], 5, -701558691),
                c = a(c, r, f, h, n[o + 10], 9, 38016083),
                h = a(h, c, r, f, n[o + 15], 14, -660478335),
                f = a(f, h, c, r, n[o + 4], 20, -405537848),
                r = a(r, f, h, c, n[o + 9], 5, 568446438),
                c = a(c, r, f, h, n[o + 14], 9, -1019803690),
                h = a(h, c, r, f, n[o + 3], 14, -187363961),
                f = a(f, h, c, r, n[o + 8], 20, 1163531501),
                r = a(r, f, h, c, n[o + 13], 5, -1444681467),
                c = a(c, r, f, h, n[o + 2], 9, -51403784),
                h = a(h, c, r, f, n[o + 7], 14, 1735328473),
                r = s(r, f = a(f, h, c, r, n[o + 12], 20, -1926607734), h, c, n[o + 5], 4, -378558),
                c = s(c, r, f, h, n[o + 8], 11, -2022574463),
                h = s(h, c, r, f, n[o + 11], 16, 1839030562),
                f = s(f, h, c, r, n[o + 14], 23, -35309556),
                r = s(r, f, h, c, n[o + 1], 4, -1530992060),
                c = s(c, r, f, h, n[o + 4], 11, 1272893353),
                h = s(h, c, r, f, n[o + 7], 16, -155497632),
                f = s(f, h, c, r, n[o + 10], 23, -1094730640),
                r = s(r, f, h, c, n[o + 13], 4, 681279174),
                c = s(c, r, f, h, n[o], 11, -358537222),
                h = s(h, c, r, f, n[o + 3], 16, -722521979),
                f = s(f, h, c, r, n[o + 6], 23, 76029189),
                r = s(r, f, h, c, n[o + 9], 4, -640364487),
                c = s(c, r, f, h, n[o + 12], 11, -421815835),
                h = s(h, c, r, f, n[o + 15], 16, 530742520),
                r = v(r, f = s(f, h, c, r, n[o + 2], 23, -995338651), h, c, n[o], 6, -198630844),
                c = v(c, r, f, h, n[o + 7], 10, 1126891415),
                h = v(h, c, r, f, n[o + 14], 15, -1416354905),
                f = v(f, h, c, r, n[o + 5], 21, -57434055),
                r = v(r, f, h, c, n[o + 12], 6, 1700485571),
                c = v(c, r, f, h, n[o + 3], 10, -1894986606),
                h = v(h, c, r, f, n[o + 10], 15, -1051523),
                f = v(f, h, c, r, n[o + 1], 21, -2054922799),
                r = v(r, f, h, c, n[o + 8], 6, 1873313359),
                c = v(c, r, f, h, n[o + 15], 10, -30611744),
                h = v(h, c, r, f, n[o + 6], 15, -1560198380),
                f = v(f, h, c, r, n[o + 13], 21, 1309151649),
                r = v(r, f, h, c, n[o + 4], 6, -145523070),
                c = v(c, r, f, h, n[o + 11], 10, -1120210379),
                h = v(h, c, r, f, n[o + 2], 15, 718787259),
                f = v(f, h, c, r, n[o + 9], 21, -343485551),
                r = l(r, e),
                f = l(f, u),
                h = l(h, p),
                c = l(c, i);
            return [r, f, h, c]
        }(function(n) {
            var t, o = [];
            for (o[(n.length >> 2) - 1] = void 0,
            t = 0; t < o.length; t += 1)
                o[t] = 0;
            for (t = 0; t < 8 * n.length; t += 8)
                o[t >> 5] |= (255 & n.charCodeAt(t / 8)) << t % 32;
            return o
        }(n), 8 * n.length))
    }
    function o(n) {
        return t(unescape(encodeURIComponent(n)))
    }
    return function(n) {
        var t, o, e = "0123456789abcdef", u = "";
        for (o = 0; o < n.length; o += 1)
            t = n.charCodeAt(o),
            u += e.charAt(t >>> 4 & 15) + e.charAt(15 & t);
        return u
    }(o(n))
}

function r(f, h, c, l, g) {
    g = g || [[this], [{}]];
    for (var t = [], o = null, n = [function() {
        return !0
    }
    , function() {}
    , function() {
        g.length = c[h++]
    }
    , function() {
        g.push(c[h++])
    }
    , function() {
        g.pop()
    }
    , function() {
        var n = c[h++]
          , t = g[g.length - 2 - n];
        g[g.length - 2 - n] = g.pop(),
        g.push(t)
    }
    , function() {
        g.push(g[g.length - 1])
    }
    , function() {
        g.push([g.pop(), g.pop()].reverse())
    }
    , function() {
        g.push([l, g.pop()])
    }
    , function() {
        g.push([g.pop()])
    }
    , function() {
        var n = g.pop();
        g.push(n[0][n[1]])
    }
    , function() {
        g.push(g[g.pop()[0]][0])
    }
    , function() {
        var n = g[g.length - 2];
        n[0][n[1]] = g[g.length - 1]
    }
    , function() {
        g[g[g.length - 2][0]][0] = g[g.length - 1]
    }
    , function() {
        var n = g.pop()
          , t = g.pop();
        g.push([t[0][t[1]], n])
    }
    , function() {
        var n = g.pop();
        g.push([g[g.pop()][0], n])
    }
    , function() {
        var n = g.pop();
        g.push(delete n[0][n[1]])
    }
    , function() {
        var n = [];
        for (var t in g.pop())
            n.push(t);
        g.push(n)
    }
    , function() {
        g[g.length - 1].length ? g.push(g[g.length - 1].shift(), !0) : g.push(void 0, !1)
    }
    , function() {
        var n = g[g.length - 2]
          , t = Object.getOwnPropertyDescriptor(n[0], n[1]) || {
            configurable: !0,
            enumerable: !0
        };
        t.get = g[g.length - 1],
        Object.defineProperty(n[0], n[1], t)
    }
    , function() {
        var n = g[g.length - 2]
          , t = Object.getOwnPropertyDescriptor(n[0], n[1]) || {
            configurable: !0,
            enumerable: !0
        };
        t.set = g[g.length - 1],
        Object.defineProperty(n[0], n[1], t)
    }
    , function() {
        h = c[h++]
    }
    , function() {
        var n = c[h++];
        g[g.length - 1] && (h = n)
    }
    , function() {
        throw g[g.length - 1]
    }
    , function() {
        var n = c[h++]
          , t = n ? g.slice(-n) : [];
        g.length -= n,
        g.push(g.pop().apply(l, t))
    }
    , function() {
        var n = c[h++]
          , t = n ? g.slice(-n) : [];
        g.length -= n;
        var o = g.pop();
        g.push(o[0][o[1]].apply(o[0], t))
    }
    , function() {
        var n = c[h++]
          , t = n ? g.slice(-n) : [];
        g.length -= n,
        t.unshift(null),
        g.push(new (Function.prototype.bind.apply(g.pop(), t)))
    }
    , function() {
        var n = c[h++]
          , t = n ? g.slice(-n) : [];
        g.length -= n,
        t.unshift(null);
        var o = g.pop();
        g.push(new (Function.prototype.bind.apply(o[0][o[1]], t)))
    }
    , function() {
        g.push(!g.pop())
    }
    , function() {
        g.push(~g.pop())
    }
    , function() {
        g.push(typeof g.pop())
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] == g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] === g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] > g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] >= g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] << g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] >> g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] >>> g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] + g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] - g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] * g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] / g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] % g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] | g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] & g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] ^ g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2]in g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2]instanceof g.pop()
    }
    , function() {
        g[g[g.length - 1][0]] = void 0 === g[g[g.length - 1][0]] ? [] : g[g[g.length - 1][0]]
    }
    , function() {
        for (var e = c[h++], u = [], n = c[h++], t = c[h++], p = [], o = 0; o < n; o++)
            u[c[h++]] = g[c[h++]];
        for (var i = 0; i < t; i++)
            p[i] = c[h++];
        g.push(function n() {
            var t = u.slice(0);
            t[0] = [this],
            t[1] = [arguments],
            t[2] = [n];
            for (var o = 0; o < p.length && o < arguments.length; o++)
                0 < p[o] && (t[p[o]] = [arguments[o]]);
            return r(f, e, c, l, t)
        })
    }
    , function() {
        t.push([c[h++], g.length, c[h++]])
    }
    , function() {
        t.pop()
    }
    , function() {
        return !!o
    }
    , function() {
        o = null
    }
    , function() {
        g[g.length - 1] += String.fromCharCode(c[h++])
    }
    , function() {
        g.push("")
    }
    , function() {
        g.push(void 0)
    }
    , function() {
        g.push(null)
    }
    , function() {
        g.push(!0)
    }
    , function() {
        g.push(!1)
    }
    , function() {
        g.length -= c[h++]
    }
    , function() {
        g[g.length - 1] = c[h++]
    }
    , function() {
        var n = g.pop()
          , t = g[g.length - 1];
        t[0][t[1]] = g[n[0]][0]
    }
    , function() {
        var n = g.pop()
          , t = g[g.length - 1];
        t[0][t[1]] = n[0][n[1]]
    }
    , function() {
        var n = g.pop()
          , t = g[g.length - 1];
        g[t[0]][0] = g[n[0]][0]
    }
    , function() {
        var n = g.pop()
          , t = g[g.length - 1];
        g[t[0]][0] = n[0][n[1]]
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] < g.pop()
    }
    , function() {
        g[g.length - 2] = g[g.length - 2] <= g.pop()
    }
    ]; ; )
        try {
            for (; !n[c[h++]](); )
                ;
            if (o)
                throw o;
            return g.pop()
        } catch (n) {
            var e = t.pop();
            if (void 0 === e)
                throw n;
            o = n,
            h = e[0],
            g.length = e[1],
            e[2] && (g[e[2]][0] = o)
        }
}
function getSecuritySign(data){
    let str = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let count = Math.floor(Math.random() * 7 + 10);
    let sign = 'zza';
    for(let i = 0; i < count ; i++){
        sign += str[Math.floor(Math.random() * 36)];
    }
    sign += __sign_hash_20200305('CJBPACrRuNy7'+data);
    return sign
}
