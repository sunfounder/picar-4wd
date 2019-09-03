// (function(doc, win) {
//     var docEl = doc.documentElement,
//         isIOS = navigator.userAgent.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/),
//         dpr = isIOS ? Math.min(win.devicePixelRatio, 3) : 1,
//         dpr = window.top === window.self ? dpr : 1, //被iframe引用时，禁止缩放
//         dpr = 1,
//         scale = 1 / dpr,
//         resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize';
//     docEl.dataset.dpr = dpr;
//     var metaEl = doc.createElement('meta');
//     metaEl.name = 'viewport';
//     metaEl.content = 'initial-scale=' + scale + ',maximum-scale=' + scale + ', minimum-scale=' + scale;
//     docEl.firstElementChild.appendChild(metaEl);
//     var recalc = function() {
//         var width = docEl.clientWidth;
//         if (width / dpr > 750) {
//             width = 750 * dpr;
//         }
//         // 乘以100，px : rem = 100 : 1
//         docEl.style.fontSize = 100 * (width / 1340) + 'px';
//     };
//     recalc()
//     if (!doc.addEventListener) return;
//     win.addEventListener(resizeEvt, recalc, false);
// })(document, window);

;(function (designWidth, maxWidth) {
    var doc = document,
        win = window;
    var docEl = doc.documentElement;
    var tid;
    var rootItem, rootStyle;

    function refreshRem() {
        var width = docEl.getBoundingClientRect().width;
        if (!maxWidth) {
            maxWidth = 540;
        }
        ;
        if (width > maxWidth) {
            width = maxWidth;
        }
        //与淘宝做法不同，直接采用简单的rem换算方法1rem=100px
        var rem = width * 100 / designWidth;
        //兼容UC开始
        rootStyle = "html{font-size:" + rem + 'px !important}';
        rootItem = document.getElementById('rootsize') || document.createElement("style");
        if (!document.getElementById('rootsize')) {
            document.getElementsByTagName("head")[0].appendChild(rootItem);
            rootItem.id = 'rootsize';
        }
        if (rootItem.styleSheet) {
            rootItem.styleSheet.disabled || (rootItem.styleSheet.cssText = rootStyle)
        } else {
            try {
                rootItem.innerHTML = rootStyle
            } catch (f) {
                rootItem.innerText = rootStyle
            }
        }
        //兼容UC结束
        docEl.style.fontSize = rem + "px";
    };
    refreshRem();

    win.addEventListener("resize", function () {
        clearTimeout(tid); //防止执行两次
        tid = setTimeout(refreshRem, 300);
    }, false);

    win.addEventListener("pageshow", function (e) {
        if (e.persisted) { // 浏览器后退的时候重新计算
            clearTimeout(tid);
            tid = setTimeout(refreshRem, 300);
        }
    }, false);

    if (doc.readyState === "complete") {
        doc.body.style.fontSize = "16px";
    } else {
        doc.addEventListener("DOMContentLoaded", function (e) {
            doc.body.style.fontSize = "16px";
        }, false);
    }
})(1334, 2048);