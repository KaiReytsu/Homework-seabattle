var ws = null;
document.addEventListener(
    "DOMContentLoaded",
	function() {
        if (gameid == ''){
            ws = new WebSocket("ws://" + window.location.host + '/' + socket);
        }
        else{
            ws = new WebSocket("ws://" + window.location.host + '/' + socket+ '/' + gameid);
            console.log('test')
            document.getElementById('loader').style.display = 'none';
            document.getElementById('your_ship').style.display = 'block';
            document.getElementById('code').style.display = 'none';
        }
        console.log('it work!');
        ws.onmessage = function(event){
            var message = JSON.parse(event.data);
            if(message.type == 'id'){
               document.getElementById('private_code').innerHTML = message.data;
            }
            if(message.type == 'service'){
                if(message.data == 'new_player'){
                    document.getElementById('loader').style.display = 'none';
                    document.getElementById('your_ship').style.display = 'block';
                }
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

