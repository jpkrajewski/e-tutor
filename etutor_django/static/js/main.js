let canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;

let x = "black",
    y = 2;

const userFirstName = JSON.parse(document.getElementById('userFirstName').textContent)
const username = userFirstName == 'student' ? userFirstName + Math.ceil(Math.random() * 10000) : userFirstName

const messageList = document.getElementById('message-list');
const sendMessageButton = document.getElementById('btn-send-msg');
const messageInputBox = document.getElementById('msg');


sendMessageButton.addEventListener('click', () => {
    let message = messageInputBox.value;

    if(message == '') {
        return;
    }

    if(isValidURL(message)) {
        showChatMessageLink('Me', message);
    } else {
        showChatMessage('Me: ' + message);
    }

    messageInputBox.value = '';
    sendSignal('send', {'message': message, 'user': username}, 'chat');

});

messageInputBox.onkeypress = (event) => {
  const keyCode = event.keyCode
  if (keyCode === 13) {
    sendMessageButton.click()
  }
}


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
    if (x == "white") y = 30;
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

    sendSignal('move', {
        'prevx': prevX,
        'prevy': prevY,
        'curx': currX,
        'cury': currY,
        'stroke': x,
        'width': y
    }, 'draw')
}

function erase() {
    if (confirm("Clear?")) {
        ctx.clearRect(0, 0, w, h);
        sendSignal('clear', {}, 'draw');
    }
}

function findxy(res, e) {
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        currX = e.clientX - canvas.getBoundingClientRect().left;
        currY = e.clientY - canvas.getBoundingClientRect().top;

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (res == 'up' || res == "out") {
        flag = false;
    }
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.getBoundingClientRect().left;
            currY = e.clientY - canvas.getBoundingClientRect().top;
            draw();
        }
    }
}

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const lessonSocket = new WebSocket(
    ws_scheme
    + '://'
    + window.location.host
    + '/ws/lesson/'
    + roomName
    + '/'
);

lessonSocket.onopen = event => {
    console.log('Connection opened!');
    sendSignal('new-peer', {}, 'connected');
};

lessonSocket.onclose = event => {
    console.error('Chat socket closed unexpectedly');
    showChatMessage('Chat socket closed unexpectedly, refresh page.');
};

lessonSocket.onerror = event => {
    console.error('Error occurred');
}

lessonSocket.onmessage = event => {
    const data = JSON.parse(event.data).message;

    if (data.username == username) {
        return;
    }

    switch(data.type) {

        case 'draw':
            drawAction(data);
            break;

        case 'chat':
            chatAction(data);
            break;

        case 'connected':
            chatAction(data);
            break;

        default:
            console.log('default');

    }

    console.log(data);
    console.log(username);
};

function showChatMessage(chatMessage) {
    let li = document.createElement('li');
    li.appendChild(document.createTextNode(chatMessage));
    li.classList.add("list-group-item");
    messageList.appendChild(li);
}

function showChatMessageLink(user, link) {

    let a = document.createElement('a');
    let linkText = document.createTextNode(link);
    a.appendChild(linkText);
    a.href = link;
    a.target = "_blank"

    let li = document.createElement('li');
    li.appendChild(document.createTextNode(user + ': '));
    li.appendChild(a);
    li.classList.add("list-group-item");
    messageList.appendChild(li);
}

function chatAction(data){
    switch(data.action) {
        case 'send':
            if(isValidURL(data.message.message)) {
                console.log('works');
                showChatMessageLink(data.message.user, data.message.message);
            } else {
                showChatMessage(data.message.user + ': ' + data.message.message);
            }
            break;

        case 'new-peer':
            showChatMessage(data.username + ' joined the room!');
            break;

        default:
            console.log('bad chat action');
    }
}

function drawAction(data){
    switch(data.action) {
        case 'clear':
            ctx.clearRect(0, 0, w, h);
            break;

        case 'down':
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(data.message.curx, data.message.cury, 2, 2);
            ctx.closePath();
            break;

        case 'move':
            ctx.beginPath();
            ctx.moveTo(data.message.prevx, data.message.prevy);
            ctx.lineTo(data.message.curx, data.message.cury);
            ctx.strokeStyle = data.message.stroke;
            ctx.lineWidth = data.message.width;
            ctx.stroke();
            ctx.closePath();
            break;

        default:
            console.log('gowno');
    }
}

function sendSignal(action, message, type) {
    let jsonString = JSON.stringify({
        'username': username,
        'action': action,
        'message': message,
        'type': type,
    });
    console.log(jsonString);
    lessonSocket.send(jsonString);
};

let localStream = new MediaStream();
const constrains = {
    'video': true,
    'audio': true,
}

const localVideo = document.querySelector('#local-video');

let userMedia = navigator.mediaDevices.getUserMedia(constrains)
    .then(stream => {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;
    })
    .catch(error => {
        console.log('Error accessing media devices', error)
    });

function createOffer(peerUsername, receiverChannelName) {
    let peer = new RTCPeerConnection(null);
    addLocalTracks(peer);
    let dc = peer.createDataChannel('channel');
    dc.addEventListener('open', () => {
        console.log()
    });
}

function addLocalTracks(peer) {
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream)
    });

    return;
}

function isValidURL(str) {
  var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
    '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
    '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
    '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
    '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
    '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!pattern.test(str);
}

function saveCanvas() {
    console.log('start')
    const link = document.createElement('a');
    let name = new Date().toLocaleTimeString();
    link.download = 'mathematics' + name + '.png';
    link.href = canvas.toDataURL();
    link.click();
    link.delete;
}


init();