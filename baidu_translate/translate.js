var i = "320305.131321201"


function n(r, o) {
    for (var t = 0; t < o.length - 2; t += 3) {
        var e = o.charAt(t + 2);
        e = e >= "a" ? e.charCodeAt(0) - 87 : Number(e),
            e = "+" === o.charAt(t + 1) ? r >>> e : r << e,
            r = "+" === o.charAt(t) ? r + e & 4294967295 : r ^ e
    }
    return r
}

function a(r) {
    var t = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
    if (null === t) {
        var a = r.length;
        a > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(a / 2) - 5, 10) + r.substr(-10, 10))
    } else {
        for (var C = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), h = 0, f = C.length, u = []; f > h; h++)
            "" !== C[h] && u.push.apply(u, e(C[h].split(""))),
            h !== f - 1 && u.push(t[h]);
        var g = u.length;
        g > 30 && (r = u.slice(0, 10).join("") + u.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + u.slice(-10).join(""))
    }
    var l = void 0
        , d = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
    l = null !== i ? i : (i = o.common[d] || "") || "";
    for (var m = l.split("."), S = Number(m[0]) || 0, s = Number(m[1]) || 0, c = [], v = 0, F = 0; F < r.length; F++) {
        var p = r.charCodeAt(F);
        128 > p ? c[v++] = p : (2048 > p ? c[v++] = p >> 6 | 192 : (55296 === (64512 & p) && F + 1 < r.length && 56320 === (64512 & r.charCodeAt(F + 1)) ? (p = 65536 + ((1023 & p) << 10) + (1023 & r.charCodeAt(++F)),
            c[v++] = p >> 18 | 240,
            c[v++] = p >> 12 & 63 | 128) : c[v++] = p >> 12 | 224,
            c[v++] = p >> 6 & 63 | 128),
            c[v++] = 63 & p | 128)
    }
    for (var w = S, A = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), b = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), D = 0; D < c.length; D++)
        w += c[D],
            w = n(w, A);
    return w = n(w, b),
        w ^= s,
    0 > w && (w = (2147483647 & w) + 2147483648),
        w %= 1e6,
    w.toString() + "." + (w ^ S)
}
