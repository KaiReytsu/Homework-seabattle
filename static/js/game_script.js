var ws = null;
document.addEventListener(
    "DOMContentLoaded",
	function() {
        if (gameid == ''){
            ws = new WebSocket("ws://" + window.location.host + '/' + socket);
        }
        else{
            ws = new WebSocket("ws://" + window.location.host + '/' + socket+ '/' + gameid);
        }
        console.log('it work!');
        ws.onmessage = function(event){
            var shipid = document.getElementById('ship').innerHTML = event.data
        }
        }
    );

    function clicktest(){
        console.log('begin!!')
        console.log(ws)
        ws.send('hi')
}

