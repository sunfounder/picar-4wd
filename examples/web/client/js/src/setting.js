var Setting = {};

Setting.id = "setting";

// 超声波设置
Setting.ultrasonic = {};

// 车轮速度设置
Setting.wheel = {};

// 巡线设置
Setting.grayscale = {};


Setting.show = function () {
    document.querySelector('#settingContent').style.display = 'block';
    document.querySelector('#header').style.display = 'block';
    document.querySelector('.header_title').style.display = 'block'
    Setting.tabClick();
    Manual.sendValue['csb'] = ['off', 'off', 'off'];
    requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
}

Setting.hide = function () {
    document.querySelector('#settingContent').style.display = 'none';
    document.querySelector('#header').style.display = 'none';
    document.querySelector('.header_title').style.display = 'none';
}

Setting.init = function() {
    Setting.wheel.chooseWheel();
    Setting.tabInit();
    Setting.grayscale.changeReference();
    Setting.ultrasonic.rangeSet();
    Setting.wheel.setRange();
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
            Manual.sendValue['csb'] = ['off', 'off', 'off'];
            requireWebsocket.reqWs.send(Manual.sendValue);
        }
    })
}

Setting.ultrasonic.rangeSet = function () {
    var change = function (e) {
        console.log(e.value);
        Manual.sendValue['csbs'][0] = 'on';
        Manual.sendValue['csbs'][1] = e.value;
        requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue))
    }
    $('input#setting_ultrasonic_slider_range').RangeSlider({min: -90, max: 90, step: 1, callback:change})
}

Setting.grayscale.setValue = function (data) {
    for (var i = 0; i < data['fl'].length; i++) {
        $('.grayscale_setting_item_text_item').eq(i).html(`Grayscale value:${data['fl'][i]}`);
    }
}

Setting.grayscale.setColor = function (data) {
    Setting.grayscale.cliffReference = $('.cliffreference input').val();
    Setting.grayscale.lineReference = $('.linereference input').val();
    for (var i = 0; i < data['fl'].length; i++) {
        if (data['fl'][i] < Setting.grayscale.cliffReference) {
            $('.grayscale_setting_item_danger').eq(i).show().css({'background': "red"});
        }else if (data['fl'][i] < Setting.grayscale.lineReference){
            $('.grayscale_setting_item_danger').eq(i).show().css({'background': "black"});
        }else {
            $('.grayscale_setting_item_danger').eq(i).show().css({'background': "none"});
        }
    }
}

Setting.grayscale.changeReference = function () {
    $('.cliffreference input').change(function () {
        // console.log($(this).val());
        Setting.grayscale.cliffReference = $(this).val();
        Manual.sendValue['ed'] = [Manual.cliffFlag, Setting.grayscale.cliffReference]
    })

    $('.linereference input').change(function () {
        Setting.grayscale.lineReference = $(this).val();
        Manual.sendValue['fl'] = [Manual.lineFlag, Setting.grayscale.lineReference]
    })
}

Setting.wheel.chooseWheel = function () {
    $('.wheel').click(function () {
        $('.wheel').css({"opacity": 0});
        $(this).css({"opacity": 1});
        $('.wheel_name span').html($(this).attr('data-name'))
    })
}

Setting.wheel.setRange = function () {
    var change = function (e) {
        console.log(e.value);
        $('.wheel_speed_power_value').html(`${e.value}%`);
    }
    $('input#wheel_speed_power_slider_input').RangeSlider({min: 0, max: 100, step: 1, callback:change})
}