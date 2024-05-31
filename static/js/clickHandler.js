
function winClick(index) {
    const res = document.getElementById('gameResult');
    res.innerHTML = "Верно!";
    showRightAnswer(index);
    //fetch('/game_result/win')
    //.catch(error => console.error('Ошибка:', error));
}

function loseClick(index) {
    const res = document.getElementById('gameResult');
    res.innerHTML = "Не правильно(";
    showRightAnswer(index);
//    fetch('/game_result/lose')
//    .catch(error => console.error('Ошибка:', error));
}

function showRightAnswer(index){
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

function hideRightAnswer(){
    for (let i = 0; i < 4; i++) {
        elements[i].style.color = 'black';
    }
}

function showButtonNext(){
    let button = document.getElementById("next");
    button.style.display = "block";
}

function getAllSongs(){
    fetch('/songs/' + genreId)
    .then(response => response.json())
    .then(data => {
        allSongs = data;
    })
    .then(prom => playNext())
    .catch(error => console.error('Ошибка:', error));
}

function randomNumber(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function refreshTiles(){
    fetch('/songs/' + genreId)
    .then(response => response.json())
    .then(data => {
        tiles = data;
        console.log(tiles);
    })
    .then(prom => {
        let isInTiles = false;
        for (let i = 0; i < 4; i++) {
            elements[i].style.color = 'black';
            elements[i].innerHTML = "<p>" + tiles[i]['author'] + "</p><p>" + tiles[i]['name'] + "</p>"
            if (tiles[i]['name'] == allSongs[currSong]['name']){
                isInTiles = true;
            }
        }
        if (isInTiles == false){
            let ind = randomNumber(0,4);
            elements[ind].innerHTML = "<p>" + allSongs[currSong]['author'] + "</p><p>" + allSongs[currSong]['name'] + "</p>";
            console.log("changed "+ ind);

        }
    })
    .catch(error => console.error('Ошибка:', error));
}

let currSong = -1;
var audio = new Audio();
function playNext(){
    currSong += 1;
    refreshTiles();
    stopPlaying();
    audio = new Audio(startPath + allSongs[currSong]['path']);
    console.log("current song: " + allSongs[currSong]['name'])
    audio.currentTime = 0;
    audio.addEventListener('timeupdate', function() {
            if (audio.currentTime >= 30) {
                audio.pause();
            }
        }
    )
    audio.play();
}

function stopPlaying(){
    audio.pause();
    audio.currentTime = 30;
}
const elements = document.getElementsByClassName('smth-content');
let tiles = [];
let allSongs = [];
getAllSongs();
