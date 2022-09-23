var Setting = {};

Setting.id = "setting";

// 超声波设置
Setting.ultrasonic = {};

Setting.showFlag = false;


Setting.ultrasonic.show = true;
// 车轮速度设置
Setting.wheel = {};

// 巡线设置
Setting.grayscale = {};

Setting.grayscale.show = false;

Setting.system = {};

Setting.system.showFlag = false;

Setting.wheel.motor = 2;

Setting.wheel.speedValueText = 0;


Setting.show = function () {
    Setting.showFlag = true;
    document.querySelector('#settingContent').style.display = 'block';
    document.querySelector('#header').style.display = 'block';
    document.querySelector('.header_title').style.display = 'block'
    Setting.tabClick();
    if (Setting.ultrasonic.show) {
        Manual.sendValue['US'] = ['on', 0];
    }
   
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
}

Setting.hide = function () {
    Setting.showFlag = false;
    document.querySelector('#settingContent').style.display = 'none';
    document.querySelector('#header').style.display = 'none';
    document.querySelector('.header_title').style.display = 'none';
    Manual.sendValue['US'] = ['off', 0];
    Manual.sendValue['MS'] = ['off', 2, 0];
    Manual.sendValue['ST'] = 'off';
    Manual.sendValue['TL'] = ['off', Setting.grayscale.lineReference];
    Manual.sendValue['CD'] = ['off', Setting.grayscale.cliffReference];
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
}

Setting.init = function() {
    Setting.wheel.chooseWheel();
    Setting.tabInit();
    Setting.grayscale.changeReference();
    Setting.ultrasonic.rangeSet();
    Setting.wheel.setRange();
    Setting.wheel.upArrowEvent();
    Setting.wheel.downArrowEvent();
}

Setting.resize = function () {
    var settingContentHeight = $(window).height() - $('#header').height()
    $('#settingContent').height(settingContentHeight);
}

Setting.tabInit = function () {
    $(".tab_item").eq(0).css({background: "#2d4188"})
    $('.setting_block').eq(0).show();
}

Setting.tabClick = function () {
    $('.tab_item').click(function () {
        $('.tab_item').css({background: "none"})
        $(this).css({background: "#2d4188"})
        $('.setting_block').hide();
        $('.setting_block').eq($(this).index()).show();
        if ($(this).index() === 0) {
            Manual.sendValue['US'] = ['on', 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        } else{
            Setting.ultrasonic.show = false;
            Manual.sendValue['US'] = ['off', 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
        if ($(this).index() === 1) {
            Manual.sendValue['MS'] = ['on', 2, 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }else {
            Manual.sendValue['MS'] = ['off', 2, 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
        if ($(this).index() === 2) {
            Setting.grayscale.show = true;
            Manual.sendValue['GS'] = 'on';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }else {
            Setting.grayscale.show = false;
            Manual.sendValue['GS'] = 'off';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
        if ($(this).index() === 3) {
            Setting.system.showFlag = true;
            Manual.sendValue['ST'] = 'on';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }else {
            Setting.system.showFlag = false;
            Manual.sendValue['ST'] = 'off';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
    })
}

Setting.ultrasonic.rangeSet = function () {
    var change = function (e) {
        Manual.sendValue['US'][0] = 'on';
        Manual.sendValue['US'][1] = e.value;
        requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
    }
    $('input#setting_ultrasonic_slider_range').RangeSlider({min: -90, max: 90, step: 1, callback:change})
}

Setting.ultrasonic.ultrasonicSetDot = function (data) {
    var angle = -parseInt(data[0]);
    var distance = parseInt(data[1]);
    rad = angle * Math.PI / 180;
    distance = distance * 480 / 110;
    $('style').html(`.setting_ultrasonic_img_block:after{transform: rotate(${angle}deg)}`)
    if (distance < 0 || distance > 480) {
        $(`.setting_ultrasonic_dot`).remove();
        return false;
    }
    if (document.documentElement.clientWidth > 800) {
        var x = Math.round(Math.sin(rad) * distance) + ($('.setting_ultrasonic_dot_block').width() - 560) / 2;
    }else {
        var x = Math.round(Math.sin(rad) * distance) + $('.setting_ultrasonic_dot_block').width() / 2;
    }
    var y = Math.round(Math.cos(rad) * distance);
    x = (x + parseInt($('.setting_ultrasonic_dot_block').css('width')) / 2) / 100 + "rem";
    y = y / 100 + "rem";
    // console.log(angle, distance)
    // console.log(x ,y)
    // if ($(`.setting_ultrasonic_dot_${angle}`).length === 0) {
    $('.setting_ultrasonic_dot_block').html(`<div class='setting_ultrasonic_dot setting_ultrasonic_dot_${angle}'></div>`)
    // }
    $(`.setting_ultrasonic_dot_${angle}`).css({'left': x, 'bottom': y})
}

Setting.grayscale.cliffReference = 110;

Setting.grayscale.lineReference = 400;

Setting.grayscale.setValue = function (data) {
    for (var i = 0; i < data['GS'].length; i++) {
        $('.grayscale_setting_item_text_item').eq(i).html(`Grayscale value:${data['GS'][i]}`);
    }
}

Setting.grayscale.setColor = function (data) {
    Setting.grayscale.cliffReference = $('.cliffreference input').val();
    Setting.grayscale.lineReference = $('.linereference input').val();
    for (var i = 0; i < data['GS'].length; i++) {
        if (data['GS'][i] < Setting.grayscale.cliffReference) {
            $('.grayscale_setting_item_danger').eq(i).show().css({'background': "red"}).find('img').show();
        }else if (data['GS'][i] < Setting.grayscale.lineReference){
            $('.grayscale_setting_item_danger').eq(i).show().css({'background': "black"}).find('img').hide();
        }else {
            $('.grayscale_setting_item_danger').eq(i).show().css({'background': "none"}).find('img').hide();
        }
    }
}

Setting.grayscale.changeReference = function () {
    $('.cliffreference input').change(function () {
        // console.log($(this).val());
        Setting.grayscale.cliffReference = $(this).val();
        Manual.sendValue['CD'] = [Manual.cliffFlag, Setting.grayscale.cliffReference]
    })

    $('.linereference input').change(function () {
        Setting.grayscale.lineReference = $(this).val();
        Manual.sendValue['TL'] = [Manual.lineFlag, Setting.grayscale.lineReference]
    })
}

Setting.wheel.chooseWheel = function () {
    $('.wheel').click(function () {
        $('.wheel').css({"opacity": 0});
        $(this).css({"opacity": 1});
        $('.wheel_name span').html($(this).attr('data-name'))
        Setting.wheel.motor = $(this).attr('motor');
    })
}


Setting.wheel.setRange = function () {
    var change = function (e) {
        console.log(e.value);
        Setting.wheel.speedValueText = e.value;
        $('.wheel_speed_power_value').html(`${e.value}%`);
    }
    $('input#wheel_speed_power_slider_input').RangeSlider({min: 0, max: 100, step: 1, callback:change})
}

Setting.wheel.setSpeedValueText = function (data) {
    $('.wheel_speed_value .wheel_speed_value_text').html(data);
}

Setting.wheel.upArrowEvent = function () {
    var timeout = '';
    $('.wheel_arrow_key_up_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['MS'] = ['on', Setting.wheel.motor, Setting.wheel.speedValueText]
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['MS'] = ['on', Setting.wheel.motor, 0]
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Setting.wheel.downArrowEvent = function () {
    var timeout = '';
    $('.wheel_arrow_key_down_div').on({
        "touchstart": function (e) {
            e.preventDefault();
            Manual.sendValue['MS'] = ['on', Setting.wheel.motor, -Setting.wheel.speedValueText]
            timeout = setInterval(function(){
                requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
            }, 30)
        },
        "touchend": function () {
            clearInterval(timeout);
            Manual.sendValue['MS'] = ['on', Setting.wheel.motor, 0]
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
        }
    })
}

Setting.system.setValue = function (data) {
    if (Setting.system.showFlag ) {
        var systemObj = data['ST'];
        // console.log(systemObj);
        $('.cpu_temperature').find('.system_value').html(`${systemObj['cpu_temperature']}℃`);
        $('.gpu_temperature').find('.system_value').html(`${systemObj['gpu_temperature']}℃`);
        $('.cpu_usage_text').html(`CPU Usage: ${systemObj['cpu_usage']}%`);
        $('.cpu_usage').find('.system_value').find('.fill').width(`${systemObj['cpu_usage']}%`)
        var diskAll = systemObj['disk'][0];
        var diskOcc = systemObj['disk'][1]
        var diskValue = parseInt(systemObj['disk'][3]);
        $('.disk_text').html(`disk: ${diskOcc}/${diskAll}`);
        $('.disk').find('.system_value').find('.fill').width(`${diskValue}%`)
        var ramAll = parseInt(systemObj['ram'][0])
        var ramOcc = parseInt(systemObj['ram'][1])
        var ramValue = Math.round(ramOcc / ramAll * 100)
        $('.ram_text').html(`ram: ${ramOcc}MB/${ramAll}MB`);
        $('.ram').find('.system_value').find('.fill').width(`${ramValue}%`)
        var batteryAll = 8.4;
        var batteryOcc = parseInt(systemObj['battery']);
        var batteryValue = Math.round(batteryOcc / batteryAll * 100)
        $('.battery_text').html(`battery: ${batteryOcc}v/${batteryAll}v`);
        $('.battery').find('.system_value').find('.fill').width(`${batteryValue}%`)
    }
    
    // css({"background": "black",'backgroundSize': `${systemObj['cpu_usage']}%`});
}