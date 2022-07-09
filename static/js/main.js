    var canvas, ctx, flag = false,
        prevX = 0,
        currX = 0,
        prevY = 0,
        currY = 0,
        dot_flag = false;

    var x = "black",
        y = 2;

    function init() {
        canvas = document.getElementById('can');
        ctx = canvas.getContext("2d");
        w = canvas.width;
        h = canvas.height;
        console.log(w)
        console.log(h)
        console.log(username)

        canvas.addEventListener("mousemove", function (e) {
            findxy('move', e)
        }, false);
        canvas.addEventListener("mousedown", function (e) {
            findxy('down', e)
        }, false);
        canvas.addEventListener("mouseup", function (e) {
            findxy('up', e)
        }, false);
        canvas.addEventListener("mouseout", function (e) {
            findxy('out', e)
        }, false);
    }

    function color(obj) {
        switch (obj.id) {
            case "green":
                x = "green";
                break;
            case "blue":
                x = "blue";
                break;
            case "red":
                x = "red";
                break;
            case "yellow":
                x = "yellow";
                break;
            case "orange":
                x = "orange";
                break;
            case "black":
                x = "black";
                break;
            case "white":
                x = "white";
                break;
        }
        if (x == "white") y = 14;
        else y = 2;

    }

    function draw() {
        ctx.beginPath();
        ctx.moveTo(prevX, prevY);
        ctx.lineTo(currX, currY);
        ctx.strokeStyle = x;
        ctx.lineWidth = y;
        ctx.stroke();
        ctx.closePath();

         lessonSocket.send(JSON.stringify({
            'message': 'move',
            'prevx': prevX,
            'prevy': prevY,
            'curx': currX,
            'cury': currY,
            'stroke': x,
            'width': y
        }));
    }

    function erase() {
        var m = confirm("Want to clear");
        if (m) {
            ctx.clearRect(0, 0, w, h);
            lessonSocket.send(JSON.stringify({
            'message': 'clear'
        }));
        }
    }

    function findxy(res, e) {
        if (res == 'down') {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.offsetLeft;
            currY = e.clientY - canvas.offsetTop;

            flag = true;
            dot_flag = true;
            if (dot_flag) {
                ctx.beginPath();
                ctx.fillStyle = x;
                ctx.fillRect(currX, currY, 2, 2);
                ctx.closePath();
                dot_flag = false;
                lessonSocket.sendDrawingSignal('down', {'curx' : currX, 'cury': currY});
            }
        }
        if (res == 'up' || res == "out") {
            flag = false;
        }
        if (res == 'move') {
            if (flag) {
                prevX = currX;
                prevY = currY;
                currX = e.clientX - canvas.offsetLeft;
                currY = e.clientY - canvas.offsetTop;
                draw();
            }
        }
    }

    const roomName = JSON.parse(document.getElementById('room-name').textContent);

    const lessonSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/lesson/'
        + roomName
        + '/'
    );

    lessonSocket.onopen = event => {
        console.log('Connection opened!');
        sendSignal('new-peer', {});
    };

    lessonSocket.onclose = event => {
        console.error('Chat socket closed unexpectedly');
    };

    lessonSocket.onmessage = event => {
        const data = JSON.parse(event.data);
        if (data.message.username == username) {
            return;
        }

        if (data.message == 'clear') {
            ctx.clearRect(0, 0,  ctx.width,  ctx.height)
        }
        else if (data.message.message == 'down'){
            console.log(data)
            console.log(data.message.curx)
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(data.message.curx, data.message.cury, 2, 2);
            ctx.closePath();
        }
        else {
            console.log(data.message.prevx)
            ctx.beginPath();
            ctx.moveTo(data.message.prevx, data.message.prevy);
            ctx.lineTo(data.message.curx, data.message.cury);
            ctx.strokeStyle = data.message.stroke;
            ctx.lineWidth = data.message.width;
            ctx.stroke();
            ctx.closePath();
        }
    };


    var localStream = new MediaStream();
    const constrains = {
        'video': false,
        'audio': true
    }

    //const localVideo = document.querySelector('#local-video')

    var userMedia = navigator.mediaDevices.getUserMedia(constrains)
        .then(stream => {
            //localStream = stream;
            //localVideo.srcObject = localStream;
            //localVideo.muted = true;
        })
        .catch(error => {
            console.log('Error accessing media devices', error)
        });


function sendDrawingSignal(action, message) {
    var jsonString = JSON.stringify({
        'peer': username,
        'action': action,
        'message': message,
    });
};

function sendSignal(action, message) {
    var jsonString = JSON.stringify({
        'peer': username,
        'action': action,
        'message': message,
    });

    lessonSocket.send(jsonString);
};


