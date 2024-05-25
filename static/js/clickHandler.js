
function winClick(index) {
    const res = document.getElementById('gameResult');
    res.innerHTML = "Верно!";
    showRightAnswer(index);
}

function loseClick(index) {
    const res = document.getElementById('gameResult');
    res.innerHTML = "Не правильно("
    showRightAnswer(index);
}

function showRightAnswer(index){
    const elements = document.getElementsByClassName('smth-content');
    for (let i = 0; i < 4; i++) {
        if(i == index){
            elements[i].style.color = '#07FFD7';
        }
        else{
            elements[i].style.color = 'red';
        }
    }
    showButtonNext();
}

function showButtonNext(){
    let button = document.getElementById("next");
    button.style.display = "block";
}

function hideButtonNext(){
    let button = document.getElementById("next");
    button.style.display = "none";
}

