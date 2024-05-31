
function validateClick(index) {
    if(index == rightIndex){
        const res = document.getElementById('gameResult');
        res.innerHTML = "Верно!";
        wins += 1;
    }
    else{
        const res = document.getElementById('gameResult');
        res.innerHTML = "Не правильно(";
    }
    showRightAnswer();
}

function showRightAnswer(){
    const elements = Array.from(document.getElementsByClassName('smth-content'));

    for (let i = 0; i < 4; i++) {
        if(i == rightIndex){
            elements[i].style.color = '#07FFD7';
        }
        else{
            elements[i].style.color = 'red';
        }
    }
    showButtonNext();
}

function shuffleArray(songsArray) {
    array = Array.from(songsArray);
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function hideRightAnswer(){
    const elements = Array.from(document.getElementsByClassName('smth-content'));

    for (let i = 0; i < 4; i++) {
        elements[i].style.color = 'black';
    }
}

function showButtonNext(){
    let button = document.getElementById("next");
    button.style.display = "block";
}

function hideButtonNext(){
    let button = document.getElementById("next");
    button.style.display = "none";
}

function restartAnimation() {
    var el = document.getElementById('progress');
    el.style.animation = 'none';
    el.offsetHeight;
    el.style.animation = null;
}

function getAllSongs(){
    fetch('/songs/' + genreId)
    .then(response => response.json())
    .then(data => {
        allSongs = data;
    })
    .then(prom => {
        initializeAudio();
    })
    .then(prom => playNext())
    .catch(error => console.error('Ошибка:', error));
}

function initializeAudio(){
    for (let i = 0; i < 10; i++) {
        const newAudio = new Audio(startPath + allSongs[i]['path']);
        audio.push(newAudio);
        newAudio.addEventListener('canplaythrough', function() {
            newAudio.addEventListener('timeupdate', function() {
                if (newAudio.currentTime >= 30) {
                    newAudio.pause();
                }
            });
        });
    }
}

function randomNumber(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function refreshTiles(){
    const elements = Array.from(document.getElementsByClassName('smth-content'));
    console.log("Current song " + currSong + " " + allSongs[currSong]['name']);
    tiles = shuffleArray(allSongs);
    let isInTiles = false;
    for (let i = 0; i < 4; i++) {
        elements[i].style.color = 'black';
        elements[i].innerHTML = "<p>" + tiles[i]['author'] + "</p><p>" + tiles[i]['name'] + "</p>"
        if (tiles[i]['name'] == allSongs[currSong]['name']){
            isInTiles = true;
            rightIndex = i;
        }
    }
    if (isInTiles == false){
        let ind = randomNumber(0,3);
        elements[ind].innerHTML = "<p>" + allSongs[currSong]['author'] + "</p><p>" + allSongs[currSong]['name'] + "</p>";
        console.log("changed "+ ind);
        rightIndex = ind;
    }
}

function playNext(){

    currSong += 1;
    if (currSong >= 10){
        var next = document.getElementById('next');
        next.href = '/end/' + wins;
    }
    else if(currSong != 0){
        audio[currSong-1].pause();
        audio[currSong].play();
    }
    else{
        audio[currSong].play();
    }
    refreshTiles();
    hideButtonNext();
    restartAnimation();

    const res = document.getElementById('gameResult');
    res.innerHTML = "Выбери вариант";
}

