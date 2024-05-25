var audio = document.getElementById("myAudio");
    audio.addEventListener('timeupdate', function() {
        if (audio.currentTime >= 30) {
            audio.pause();
        }
    });