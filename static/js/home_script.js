async function connect(){
    var id = document.getElementById('codetext').value;
    const responce = await fetch('/checkgame' + '?codetext=' + id);
    console.log(responce)
    if (responce.status == 200){
        window.location.href = '/connect_game' + '?codetext=' + id
    }
    else{
        document.getElementById('notfound').innerHTML = 'Игра по данному коду не найдена'
    }
}