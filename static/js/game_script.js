var ws = null;
var movemode = false;
document.addEventListener(
    "DOMContentLoaded",
	function() {
        var type = 0;
        if (gameid == ''){
            ws = new WebSocket("ws://" + window.location.host + '/' + socket);
        }
        else{
            type = 1
            ws = new WebSocket("ws://" + window.location.host + '/' + socket+ '/' + gameid);
            console.log('test')
            document.getElementById('loader').style.display = 'none';
            document.getElementById('your_ship').style.display = 'block';
            document.getElementById('code').style.display = 'none';
        }
        console.log('it work!');
        ws.onmessage = function(event){
            var message = JSON.parse(event.data);
            switch (message.type) {
                case 'id':
                    document.getElementById('private_code').innerHTML = message.data;
                    break;
                case 'service':
                    if(message.data == 'new_player'){
                        document.getElementById('loader').style.display = 'none';
                        document.getElementById('your_ship').style.display = 'block';
                    }
                    break;
                case 'offline':
                    if(type){
                        alert('Создатель игры отключился')     //переделать на модальное окно
                        document.location.href = '/'
                    }else{
                        document.getElementById('loader').style.display = 'block';
                        document.getElementById('your_ship').style.display = 'none';
                        alert('Второй игрок отключился')    //добавить вывод сообщения об оключении второго игрока
                    }
                    
                default:
                    break;
            }
            console.log(message)
        }
        }
    );

    function clicktest(){
        console.log('begin!!')
        console.log(ws)
        ws.send('hi')
}
function moveship(){
    movemode = true;
}
function placeship(num){
    if(movemode){
        movemode = false;    //нужно ещё отнимать количество кораблей
    }
}
