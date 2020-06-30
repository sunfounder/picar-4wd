var Manual = {};

Manual.id = "manual";

Manual.SpeedValue = '';

Manual.setSpeedValuetext = '';

Manual.grayscaleFlag = ''

Manual.aviodFlag = '';

Manual.followFlag = '';

Manual.ultrasonicFlag = '';

Manual.mileageObj = {};

Manual.mileageValue = 0;

Manual.sendValue = {
    'RC':'off',  // remote control  rest
    'GS': "off", // 巡线模块  'off'
    'RD':'off',  // 雷达  'off'
    'OA':'off',  // 避障  'off'
    'OF':'off',  // 跟随  'off'
    'TL':['off',400], // 巡线value  ['off', 400]
    'CD':['off',110], // 悬崖  ['off',110]
    'PW':50,  // 调速功率  50
    'SR':0,  // 复位  off
    'ST':'off', // 系统信息  'off'
    'US':['off',0],  // 超声波设置  ['off', 0]
    'MS':['off',4,0] // 测速设置  ['off', 1, 0]
}

/*
    send_dict = {
        'GS':[0,0,0],  // 巡线value
        'US':[angle, distance], // 超声波value
        'MS':[0,min], // 测速值
        'ST':{'a':1} // 系统信息value
    } 
*/

Manual.show = function () {
    document.querySelector('#manualContent').style.display = 'block';
    document.querySelector('#header').style.display = 'block';
    document.querySelector('.menu').style.display = 'block';
    // Manual.setUltrasonic();
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
}

Manual.hide = function () {
    document.querySelector('#manualContent').style.display = 'none';
    document.querySelector('#header').style.display = 'none';
    document.querySelector('.menu').style.display = 'none';
    Manual.menuItemClick("reset");
    Manual.sendValue = {
        'RC':'off',  // remote control
        'GS': "off", // 巡线模块
        'RD':'off',  // 雷达
        'OA':'off',  // 避障
        'OF':'off',  // 跟随
        'TL':['off',400], // 巡线value
        'CD':['off',110], // 悬崖
        'PW':50,  // 调速功率
        'SR': 'off',  // 复位
        'ST':'off', // 系统信息
        'US':['off',0],  // 超声波设置
        'MS':['off',1,0] // 测速设置
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
        $('.power>span').html(`${e.value}%`)
        Manual.sendValue['PW'] = e.value;
        requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
    }
    $('input#power_slider_input').RangeSlider({min: 0, max: 100, step: 1, callback:change})
}

Manual.setSpeedValue = function (data) {
    var value = parseInt((Manual.SpeedValue * 0.2) +  (data['MS'][0] * 0.9))
    $('.speedValue .text').html(value);
}

Manual.setSpeedScale = function (data) {
    var speedValue = data['MS'][0]
    var scale = Math.round(speedValue *(21 / 30))
    $('.scale_item').css({'background': "white"})
    for (var i = 0; i < scale; i++) {
        $('.scale_item').eq(i).css({'background': "black"})
    }
}

Manual.setUltrasonic = function (data) {
    Manual.sendValue['US'] = 'on';
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
}

Manual.setUltrasonicSean = function (data) {
    var angle = -parseInt(data[0]);
    var distance = parseInt(data[1]);
    rad = angle * Math.PI / 180;
    distance = distance * 270 / 70;
    $('style#ultrasonic').html(`.ultrasonic_img_block:after{transform: rotate(${angle}deg)}`)
    if (distance < 0 || distance > 270) {
        $(`.ultrasonic_dot_${angle}`).hide();
        return false;
    }
    if (document.documentElement.clientWidth > 800) {
        var x = Math.round(Math.sin(rad) * distance) + ($('.ultrasonic_dot_block').width() - 250)/ 2;
    }else {
        var x = Math.round(Math.sin(rad) * distance) + $('.setting_ultrasonic_dot_block').width() / 2;
    }
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
            Manual.sendValue['RC'] = 'forward'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['RC'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Manual.downArrowEvent = function () {
    var timeout = '';
    $('.down_arrowKey_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['RC'] = 'backward'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['RC'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Manual.leftArrowEvent = function () {
    var timeout = '';
    $('.left_arrowKey_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['RC'] = 'turn_left'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['RC'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Manual.rightArrowEvent = function () {
    var timeout = '';
    $('.right_arrowKey_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['RC'] = 'turn_right'
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['RC'] = 'rest'
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}



Manual.menuItemClick = function (reset) {
    if (arguments.length > 0) {
        $('.menu_item').off('click')
        flag_aviod = true;
        flag_follow = true;
        flag_cliff = true;
        flag_path = true;
        flag_auto = true;
        flag_ultrasonic = true;
        flag_grayScale = true;
        $('.menu_item').css({'opacity': 0.5});
        $('.menu_item_setting').css({'opacity': 1});
    }
    var flag_aviod = true,flag_follow = true,flag_cliff = true,flag_path = true,flag_auto = true, flag_ultrasonic = true, flag_grayScale = true;
    $('.menu_item_ultrasonic').click(function() {
        if (flag_ultrasonic) {
            Manual.ultrasonicFlag = 'on';
            Manual.sendValue['RD'] = Manual.ultrasonicFlag;
            $(this).css({'opacity': 1})
            $('.menu_item_follow').css({'opacity': 0.5})
            flag_ultrasonic = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.ultrasonicFlag = 'off';
            Manual.sendValue['RD'] = Manual.ultrasonicFlag;
            $(this).css({'opacity': 0.5})
            flag_ultrasonic = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
        
    })

    $('.menu_item_grayScale').click(function() {
        if (flag_grayScale) {
            Manual.grayscaleFlag = 'on';
            Manual.sendValue['GS'] = Manual.grayscaleFlag;
            $(this).css({'opacity': 1})
            $('.menu_item_follow').css({'opacity': 0.5})
            flag_grayScale = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.grayscaleFlag = 'off';
            Manual.sendValue['GS'] = Manual.grayscaleFlag;
            $(this).css({'opacity': 0.5})
            flag_grayScale = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
        
    })
    $('.menu_item_aviod').click(function() {
        if (flag_aviod) {
            Manual.aviodFlag = 'on';
            Manual.followFlag = 'off'
            Manual.sendValue['OA'] = Manual.aviodFlag;
            Manual.sendValue['RD'] = 'on'
            $(this).css({'opacity': 1})
            $('.menu_item_follow').css({'opacity': 0.5})
            flag_aviod = false;
            flag_follow = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.aviodFlag = 'off'
            Manual.followFlag = 'off'
            Manual.sendValue['OA'] = Manual.aviodFlag;
            Manual.sendValue['RD'] = Manual.ultrasonicFlag;
            $(this).css({'opacity': 0.5})
            flag_aviod = true;
            flag_follow = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
        
    })
    
    $('.menu_item_follow').click(function() {
        if (flag_follow) {
            Manual.aviodFlag = 'off';
            Manual.followFlag = 'on'
            Manual.sendValue['OF'] = Manual.followFlag;
            Manual.sendValue['RD'] = 'on'
            $('.menu_item_aviod').css({'opacity': 0.5})
            $(this).css({'opacity': 1})
            flag_follow = false;
            flag_aviod = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.aviodFlag = 'off'
            Manual.followFlag = 'off'
            Manual.sendValue['OF'] = Manual.followFlag;
            Manual.sendValue['RD'] = Manual.ultrasonicFlag;
            $(this).css({'opacity': 0.5})
            flag_follow = true;
            flag_aviod = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
    $('.menu_item_cliff').click(function() {
        if (flag_cliff) {
            Manual.cliffFlag = 'on';
            Manual.sendValue['CD'] = ['on', Setting.grayscale.cliffReference]
            Manual.sendValue['GS'] = 'on';
            $(this).css({'opacity': 1})
            flag_cliff = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.cliffFlag = 'off';
            Manual.sendValue['CD'] = ['off', Setting.grayscale.cliffReference]
            Manual.sendValue['GS'] = Manual.grayscaleFlag;
            $(this).css({'opacity': 0.5})
            flag_cliff = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
    $('.menu_item_path').click(function() {
        if (flag_path) {
            Manual.sendValue['TL'] = ['on', Setting.grayscale.lineReference]
            Manual.sendValue['GS'] = 'on';
            $(this).css({'opacity': 1})
            flag_path = false;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }else {
            Manual.sendValue['TL'] = ['off', Setting.grayscale.lineReference]
            Manual.sendValue['GS'] = Manual.grayscaleFlag;
            $(this).css({'opacity': 0.5})
            flag_path = true;
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
    $('.menu_item_setting').click(function() {
        Main.renderPage('setting');
        console.log('dfsd')
    })
}

Manual.setGrayscaleColor = function (data) {
    for (var i = 0; i < data['GS'].length; i++) {
        if (data['GS'][i] < Setting.grayscale.cliffReference) {
            $('.line_of_inspection_item_danger').eq(i).show().css({'background': "red"}).find('img').show();
        }else if (data['GS'][i] < Setting.grayscale.lineReference){
            $('.line_of_inspection_item_danger').eq(i).show().css({'background': "black"}).find('img').hide();
        }else {
            $('.line_of_inspection_item_danger').eq(i).show().css({'background': "none"}).find('img').hide();
        }
    }
}

Manual.mileage = function (data) {
    if (Manual.mileageObj['last'] != undefined) {
        Manual.mileageObj['first'] = Manual.mileageObj['last'];
    }
    Manual.mileageObj['last'] = data;
    var timeFirst = parseFloat(Manual.mileageObj['first'][1]);
    var timeLast = parseFloat(Manual.mileageObj['last'][1]);
    var speedFirst = parseFloat(Manual.mileageObj['first'][0]);
    var speedLast = parseFloat(Manual.mileageObj['last'][0]);
    if (Manual.mileageObj['first'] != undefined) {
        Manual.mileageValue += ((speedFirst + speedLast) / 2) * (timeLast - timeFirst)
        $('.mileage>span').html(`${Math.round(Manual.mileageValue)}cm`)
    }
}

Manual.mileageReset = function () {
    Manual.mileageValue = 0;
    $('.mileage>span').html(`0cm`)
}

Manual.ultrasonicReset = function () {
    $('style').html('');
    $('ultrasonic_dot_block').html('');
}

Manual.grayScaleReset = function () {
    $('.line_of_inspection_item_danger').hide();
}