var requireWebsocket = {};

requireWebsocket.connect = function () {
    // requireWebsocket.reqWs = new WebSocket(`ws://192.168.18.185:8766`);

    requireWebsocket.reqWs = new WebSocket(`ws://${window.location.hostname}:8765`);

    requireWebsocket.reqWs.onopen = function () {
        console.log("require socket connect open...");
        requireWebsocket.reqWs.send(JSON.stringify(Manual.sendValue));
    }
    
    requireWebsocket.reqWs.onmessage = function (event) {
        console.log(event);
    }
    // reqWs.send({"mode": 1,"rc": 'forward', 'ob': 3, "fl": 4, "f": 5, 'ed': 6})
    
    requireWebsocket.reqWs.onerror = function (event) {
        console.log(event);
        Main.connectModal();
    }
    
    requireWebsocket.reqWs.onclose = function (event) {
        console.log(event)
        Main.connectModal();
    }    
}


