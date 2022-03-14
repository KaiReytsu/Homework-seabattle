var ws = null;
var movemode = false;
var shiptype = 0;
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
        ws.onmessage = function(event){
            var message = JSON.parse(event.data);
            console.log(message)
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
                case 'ready':
                    console.log('ready')
                    var enemy = document.getElementsByClassName('enemy')
                    for (var i = 0; i < enemy.length; i++){
                        enemy[i].addEventListener('click', function(){
                            console.log(enemy.id)
                        })
                    }
                    
                default:
                    break;
            }
            console.log(message)
        }
        }
    );

function moveship(ship){
    
    if (ship.parentNode.className == 'gameplay'){
        var div = document.getElementById('single_deck');
        div.appendChild(ship);
    }else{
        movemode = true;
        shiptype = ship;
    }
    
}
function placeship(cell){
    if(movemode){
        movemode = false;    //нужно ещё отнимать количество кораблей
        if(cell.innerHTML == ''){
            cell.appendChild(shiptype);
        }}
    var div = document.getElementById('single_deck');
    if (div.children.length != 0){
        document.getElementById('ready_btn').setAttribute('disabled', true)
    }else{
        document.getElementById('ready_btn').removeAttribute('disabled')
    }
}

function ready(){
    var cell_matrix = [];
    var ready_message = {'type': 'ready',
                            'data': null};
    var tr_num = 0;
    while(tr_num < 10){
        cell_matrix.push([]);
        var td_num = 0;
        while(td_num < 10){ 
            var cage_num = tr_num * 10 + td_num;
            var td = document.getElementById('cage' + cage_num)
            var img = td.firstChild
            if (img == null){
                cell_matrix[tr_num].push(0);
            }else if(img.className == 'single_deck'){
                img.removeAttribute('onclick');
                cell_matrix[tr_num].push(1);
            }
            td_num += 1;
        }
        tr_num += 1;
    }
    console.log(cell_matrix);
    ready_message.data = cell_matrix;
    ws.send(JSON.stringify(ready_message));

}

