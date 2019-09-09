var responseWebsocket = {};

responseWebsocket.connect = function () {
    // responseWebsocket.resWs = new WebSocket(`ws://192.168.18.185:8766`);

    responseWebsocket.resWs = new WebSocket(`ws://${window.location.hostname}:8766`);

    responseWebsocket.resWs.onopen = function () {
        console.log("response socket connect open...");
    }
    
    responseWebsocket.resWs.onmessage = function (event) {
        console.log(event)
        
        Manual.mileage(JSON.parse(event["data"])['MS'])
        // 设置巡线的数值
        Manual.setSpeedScale(JSON.parse(event["data"]));
        if (Setting.grayscale.show) {
            Setting.grayscale.setColor(JSON.parse(event["data"]));
            Setting.grayscale.setValue(JSON.parse(event["data"]));
        }
        
        if (Manual.grayscaleFlag == 'on') {
            Manual.setGrayscaleColor(JSON.parse(event["data"]));
        }
        Setting.system.setValue(JSON.parse(event["data"]))
    
        // 速度
        Manual.lastSpeedValue = JSON.parse(event["data"])['MS']
        Manual.setSpeedValue(JSON.parse(event["data"]));
        if (Manual.ultrasonicFlag == 'on') {
            Manual.setUltrasonicSean(JSON.parse(event["data"])['US'])
        }
        
        if (Setting.showFlag) {
            Setting.ultrasonic.ultrasonicSetDot(JSON.parse(event["data"])['US'])
        }
    }
    return true;
}

