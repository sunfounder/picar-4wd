var Manual = {};

Manual.id = "manual";

Manual.SpeedValue = '';

Manual.setSpeedValuetext = '';

Manual.cliffFlag = '';

Manual.lineFlag = '';

Manual.aviodFlag = '';

Manual.followFlag = '';

Manual.ultrasonicFlag = '';

Manual.sendValue = {
    "mode": 'off',
    "rc": 'rest',
    'csb': ['off', 'off', 'on'],
    'csbs': ['off', 0], 
    "fl": ['off', 0],
    "ed": ['off', 0], 
    "f": 'off', 
    "sp": 0,
    'sps': ['off',1, 0, 'forward'],
    'sr': 'off',
}

Manual.show = function () {
    document.querySelector('#manualContent').style.display = 'block';
    document.querySelector('#header').style.display = 'block';
    document.querySelector('.menu').style.display = 'block';
    Manual.powerCircle();
    Manual.sendValue['csb'] = ['off', 'off', 'on'];
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
    Manual.setUltrasonic();
}

Manual.hide = function () {
    document.querySelector('#manualContent').style.display = 'none';
    document.querySelector('#header').style.display = 'none';
    document.querySelector('.menu').style.display = 'none';
    Manual.menuItemClick("reset");
    Manual.sendValue = {
        "mode": 'off',
        "rc": 'rest',
        'csb': ['off', 'off', 'off'],
        'csbs': ['off', 0], 
        "fl": ['off', 0],
        "ed": ['off', 110], 
        "f": 'off', 
        "sp": 0,
        'sps': ['off',1, 0, 'forward'],
        'sr': 'off'
    }
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
    $('.ultrasonic_dot_block').html('');
}

Manual.init = function () {
    Manual.menuItemClick();
    Manual.setRange();
    Manual.upArrowEvent();
    Manual.downArrowEvent();
    Manual.leftArrowEvent();
    Manual.rightArrowEvent();
}
 
Manual.resize = function () {
    var manualContentHeight = $(window).height() - $('#header').height()
    $('#manualContent').height(manualContentHeight);
}

Manual.setRange = function () {
    var change = function (e) {
        console.log(e.value);
        Manual.sendValue['sp'] = e.value;
        requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
    }
    $('input#power_slider_input').RangeSlider({min: 0, max: 100, step: 1, callback:change})
}

Manual.setSpeedValue = function (data) {
    var value = parseInt((Manual.SpeedValue * 0.2) +  (data['sp'] * 0.9))
    $('.speedValue .text').html(value);
}

Manual.setUltrasonic = function (data) {
    Manual.sendValue['csb'] = ['off', 'off', 'on'];
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
}

Manual.setUltrasonicSean = function (data) {
    var angle = -parseInt(data[0]);
    var distance = parseInt(data[1]);
    rad = angle * Math.PI / 180;
    distance = distance * 270 / 70;
    $('style').html(`.ultrasonic_img_block:after{transform: rotate(${angle}deg)}`)
    if (distance < 0 || distance > 270) {
        $(`.ultrasonic_dot_${angle}`).hide();
        return false;
    }
    var x = Math.round(Math.sin(rad) * distance) + $('.ultrasonic_dot_block').width() / 2;
    var y = Math.round(Math.cos(rad) * distance);
    x = (x + parseInt($('.ultrasonic_dot_block').css('width')) / 2) / 100 + "rem";
    y = y / 100 + "rem";
    // console.log(angle, distance)
    // console.log(x ,y)
    if ($(`.ultrasonic_dot_${angle}`).length === 0) {
        $('.ultrasonic_dot_block').append(`<div class='ultrasonic_dot ultrasonic_dot_${angle}'></div>`)
    }
    $(`.ultrasonic_dot_${angle}`).show().css({'left': x, 'bottom': y})
}

// Manual.closeUltrasonic = function () {
//     Manual.sendValue['ob'] = 'off';
//     requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
// }

Manual.upArrowEvent = function () {
    var timeout = '';
    $('.up_arrowKey_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['rc'] = 'forward'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['rc'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Manual.downArrowEvent = function () {
    var timeout = '';
    $('.down_arrowKey_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['rc'] = 'backward'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['rc'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Manual.leftArrowEvent = function () {
    var timeout = '';
    $('.left_arrowKey_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['rc'] = 'turn_left'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['rc'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Manual.rightArrowEvent = function () {
    var timeout = '';
    $('.right_arrowKey_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['rc'] = 'turn_right'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['rc'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Manual.powerCircle = function () {
    var percent = parseInt($('.mask :first-child').text());
    var baseColor = $('.circle-bar').css('background-color');

    if( percent<=50 ){
        $('.circle-bar-right').css('transform','rotate('+(percent*3.6)+'deg)');
    }else {
        $('.circle-bar-right').css({
            'transform':'rotate(0deg)',
            'background-color':baseColor
        });
        $('.circle-bar-left').css('transform','rotate('+((percent-50)*3.6)+'deg)');
    }
}

Manual.menuItemClick = function (reset) {
    if (arguments.length > 0) {
        $('.menu_item').off('click')
        flag_aviod = true;
        flag_follow = true;
        flag_cliff = true;
        flag_path = true;
        flag_auto = true;
        $('.menu_item').find('p').css({'color': 'white'});
    }
    var flag_aviod = true,flag_follow = true,flag_cliff = true,flag_path = true,flag_auto = true;
    $('.menu_item_aviod').click(function() {
        if (flag_aviod) {
            Manual.aviodFlag = 'on';
            Manual.followFlag = 'off'
            Manual.ultrasonicFlag = 'on'
            Manual.sendValue['csb'] = [Manual.aviodFlag, Manual.followFlag, Manual.ultrasonicFlag]
            $(this).find('p').css({'color': 'blue'})
            $('.menu_item_follow').find('p').css({'color': 'white'})
            flag_aviod = false;
            flag_follow = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.aviodFlag = 'off'
            Manual.followFlag = 'off'
            Manual.sendValue['csb'] = [Manual.aviodFlag, Manual.followFlag, 'on']
            $(this).find('p').css({'color': 'white'})
            flag_aviod = true;
            flag_follow = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
        
    })
    $('.menu_item_follow').click(function() {
        if (flag_follow) {
            Manual.aviodFlag = 'off';
            Manual.followFlag = 'on'
            Manual.ultrasonicFlag = 'on'
            Manual.sendValue['csb'] = [Manual.aviodFlag, Manual.followFlag, Manual.ultrasonicFlag]
            $('.menu_item_aviod').find('p').css({'color': 'white'})
            $(this).find('p').css({'color': 'blue'})
            flag_follow = false;
            flag_aviod = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.aviodFlag = 'off'
            Manual.followFlag = 'off'
            Manual.sendValue['csb'] = [Manual.aviodFlag, Manual.followFlag, 'on']
            $(this).find('p').css({'color': 'white'})
            flag_follow = true;
            flag_follow = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
    $('.menu_item_cliff').click(function() {
        if (flag_cliff) {
            Manual.cliffFlag = 'on';
            Manual.sendValue['ed'] = [Manual.cliffFlag, Setting.grayscale.cliffReference]
            $(this).find('p').css({'color': 'blue'})
            flag_cliff = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.cliffFlag = 'off';
            Manual.sendValue['ed'] = [Manual.cliffFlag, Setting.grayscale.cliffReference]
            $(this).find('p').css({'color': 'white'})
            flag_cliff = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
    $('.menu_item_path').click(function() {
        if (flag_path) {
            Manual.lineFlag = 'on';
            Manual.sendValue['fl'] = [Manual.lineFlag, Setting.grayscale.lineReference]
            $(this).find('p').css({'color': 'blue'})
            flag_path = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.lineFlag = 'off';
            Manual.sendValue['fl'] = [Manual.lineFlag, Setting.grayscale.lineReference]
            $(this).find('p').css({'color': 'white'})
            flag_path = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
    $('.menu_item_auto').click(function() {
        if (flag_auto) {
            $(this).find('p').css({'color': 'blue'})
            flag_auto = false;
        }else {
            $(this).find('p').css({'color': 'white'})
            flag_auto = true;
        }
    })
    $('.menu_item_setting').click(function() {
        Manual.sendValue['csb'] = ['off', 'off', 'off'];
        Main.renderPage('setting');
        console.log('dfsd')
    })
}