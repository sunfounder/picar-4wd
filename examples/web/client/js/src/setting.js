var Setting = {};

Setting.id = "setting";

// ultrasonic setting
Setting.ultrasonic = {};
Setting.showFlag = false;
Setting.ultrasonic.show = true;

// wheel speed setting
Setting.wheel = {};
Setting.wheel.motor = 2;
Setting.wheel.speedValueText = 0;

var wheel_button_timeout = '';

// grayscale setting
Setting.grayscale = {};
Setting.grayscale.show = false;
Setting.grayscale.cliffReference = 110;
Setting.grayscale.lineReference = 400;

// system info
Setting.system = {};
Setting.system.showFlag = false;


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

Setting.init = function () {
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
    $(".tab_item").eq(0).css({ background: "#2d4188" })
    // $('.setting_block').eq(0).show();
    $('.setting_block').eq(0).css('display', 'flex');
}

Setting.tabClick = function () {
    $('.tab_item').click(function () {
        $('.tab_item').css({ background: "none" })
        $(this).css({ background: "#2d4188" })
        $('.setting_block').hide();
        // $('.setting_block').eq($(this).index()).show();
        $('.setting_block').eq($(this).index()).css('display', 'flex');
        if ($(this).index() === 0) {
            Manual.sendValue['US'] = ['on', 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        } else {
            Setting.ultrasonic.show = false;
            Manual.sendValue['US'] = ['off', 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
        if ($(this).index() === 1) {
            Manual.sendValue['MS'] = ['on', 2, 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        } else {
            Manual.sendValue['MS'] = ['off', 2, 0];
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
        if ($(this).index() === 2) {
            Setting.grayscale.show = true;
            Manual.sendValue['GS'] = 'on';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        } else {
            Setting.grayscale.show = false;
            Manual.sendValue['GS'] = 'off';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
        if ($(this).index() === 3) {
            Setting.system.showFlag = true;
            Manual.sendValue['ST'] = 'on';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        } else {
            Setting.system.showFlag = false;
            Manual.sendValue['ST'] = 'off';
            requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
        }
    })
}

// ultrasonic
// =================================================================================================
Setting.ultrasonic.rangeSet = function () {
    var change = function (e) {
        Manual.sendValue['US'][0] = 'on';
        Manual.sendValue['US'][1] = e.value;
        requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
    }
    $('input#setting_ultrasonic_slider_range').RangeSlider({ min: -90, max: 90, step: 1, callback: change })
}

Setting.ultrasonic.ultrasonicSetDot = function (data) {
    var MAX_DISTANCE = 110; // cm
    var angle = parseInt(data[0]);
    var distance = parseInt(data[1]);

    // console.log(`angle: ${angle}, distance: ${distance}`);

    rad = angle * Math.PI / 180;

    // radar dial hand 
    // $('.setting_ultrasonic_dial_hand').css('transform', `rotate(${angle}deg)`)
    $('.setting_ultrasonic_dial_hand').css({
        transform: `rotate(${angle}deg)`
    })

    // current dot
    if (distance < 0 || distance > MAX_DISTANCE) {
        $('.setting_ultrasonic_dot_current').css('display', 'none');
    } else {
        percent = distance / MAX_DISTANCE * 100;
        $('.setting_ultrasonic_dot_current').css({
            display: 'block',
            bottom: `${percent}%`
        })
    }
}

// grayscale
// =================================================================================================
Setting.grayscale.setValue = function (data) {
    for (var i = 0; i < data['GS'].length; i++) {
        $('.grayscale_setting_item_text_item').eq(i).html(`Grayscale value:${data['GS'][i]}`);
    }
}

Setting.grayscale.setColor = function (data) {
    Setting.grayscale.cliffReference = $('.cliffreference input').val();
    Setting.grayscale.lineReference = $('.linereference input').val();
    console.log(`xx: ${data['GS']}`);
    for (var i = 0; i < data['GS'].length; i++) {
        if (data['GS'][i] < Setting.grayscale.cliffReference) {
            $('.grayscale_setting_item_danger').eq(i).show().css({ 'background': "red" }).find('img').show();
        } else if (data['GS'][i] < Setting.grayscale.lineReference) {
            $('.grayscale_setting_item_danger').eq(i).show().css({ 'background': "black" }).find('img').hide();
        } else {
            $('.grayscale_setting_item_danger').eq(i).show().css({ 'background': "none" }).find('img').hide();
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


// wheel
// =================================================================================================
Setting.wheel.chooseWheel = function () {
    $('.wheel').click(function () {
        $('.wheel').css({ "opacity": 0 });
        $(this).css({ "opacity": 1 });
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
    $('input#wheel_speed_power_slider_input').RangeSlider({ min: 0, max: 100, step: 1, callback: change })
}

Setting.wheel.setSpeedValueText = function (data) {
    $('.wheel_speed_value .wheel_speed_value_text').html(data);
}

wheel_button_pressed_handler = function (dir = 1) {
    Manual.sendValue['MS'] = ['on', Setting.wheel.motor, dir * Setting.wheel.speedValueText]
    wheel_button_timeout = setInterval(function () {
        requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
    }, 30)
    console.log(`pressed_handler: ${Manual.sendValue['MS']}`)
};

wheel_button_released_handler = function () {
    clearInterval(wheel_button_timeout);
    Manual.sendValue['MS'] = ['on', Setting.wheel.motor, 0]
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
    console.log(`released_handler: ${Manual.sendValue['MS']}`)
};

Setting.wheel.upArrowEvent = function (e) {
    $('.wheel_arrow_key_up_div').on({
        // mobile
        "touchstart": function (e) {
            console.log('touchstart');
            e.preventDefault();
            wheel_button_pressed_handler(1);
        },
        "touchend": function () {
            console.log('touchend');
            wheel_button_released_handler();
        },
        // pc
        'mousedown': function () {
            console.log('mousedown');
            wheel_button_pressed_handler(1);
        },
        'mouseup': function () {
            console.log('mouseup');
            wheel_button_released_handler();
        },
    })
}

Setting.wheel.downArrowEvent = function () {
    $('.wheel_arrow_key_down_div').on({
        // mobile
        "touchstart": function (e) {
            console.log('touchstart');
            e.preventDefault();
            wheel_button_pressed_handler(-1);
        },
        "touchend": function () {
            console.log('touchend');
            wheel_button_released_handler();
        },
        // pc
        'mousedown': function () {
            console.log('mousedown');
            wheel_button_pressed_handler(-1);
        },
        'mouseup': function () {
            console.log('mouseup');
            wheel_button_released_handler();
        },
    })
}

// system
// =================================================================================================
Setting.system.setValue = function (data) {
    if (Setting.system.showFlag) {
        var systemObj = data['ST'];
        // console.log(systemObj);
        $('.cpu_temperature').find('.system_value').html(`${systemObj['cpu_temperature']}℃`);

        $('.cpu_usage_text').html(`CPU Usage: ${systemObj['cpu_usage']}%`);
        $('.cpu_usage').find('.system_value').find('.fill').width(`${systemObj['cpu_usage']}%`)

        var diskAll = systemObj['disk'][0];
        var diskOcc = systemObj['disk'][1]
        var diskPercent = parseInt(systemObj['disk'][3]);
        $('.disk_text').html(`disk: ${diskOcc}GB / ${diskAll}GB`);
        $('.disk').find('.system_value').find('.fill').width(`${diskPercent}%`)

        var ramAll = parseInt(systemObj['ram'][0])
        var ramOcc = parseInt(systemObj['ram'][1])
        // var ramPercent = Math.round(ramOcc / ramAll * 100)
        var ramPercent = Math.round(systemObj['ram'][2])
        $('.ram_text').html(`ram: ${ramOcc}MB / ${ramAll}MB`);
        $('.ram').find('.system_value').find('.fill').width(`${ramPercent}%`)

        var batteryAll = 8.4;
        var batteryOcc = parseFloat(systemObj['battery']);
        var batteryPercent = Math.round(batteryOcc / batteryAll * 100)
        if (batteryPercent > 100) batteryPercent = 100;
        batteryOcc = batteryOcc.toFixed(2);
        $('.battery_text').html(`battery: ${batteryOcc}v / ${batteryAll}v`);
        $('.battery').find('.system_value').find('.fill').width(`${batteryPercent}%`)
    }
}