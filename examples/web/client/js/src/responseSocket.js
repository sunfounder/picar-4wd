var responseWebsocket = {};

responseWebsocket.connect = function () {
    responseWebsocket.resWs = new WebSocket('ws://192.168.18.223:8766');

    responseWebsocket.resWs.onopen = function () {
        console.log("response socket connect open...");
    }
    
    responseWebsocket.resWs.onmessage = function (event) {
        // console.log(event)
        // 设置巡线的数值
        Setting.grayscale.setValue(JSON.parse(event["data"]));
        Setting.grayscale.setColor(JSON.parse(event["data"]));
    
        // 速度
        Manual.lastSpeedValue = JSON.parse(event["data"])['sp']
        Manual.setSpeedValue(JSON.parse(event["data"]));
        Manual.setUltrasonicSean(JSON.parse(event["data"])['csb'])
    }
    return true;
}

