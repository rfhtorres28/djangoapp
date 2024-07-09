let countdownTime = 180;
const timeDisplay = document.getElementById('time');
const form = document.getElementById('myForm');


// 
window.addEventListener('load', startTimer);


function startTimer() {

   const timerInterval = setInterval(() => {
     countdownTime = countdownTime - 1;
     timeDisplay.innerHTML = formatTime(countdownTime);

    if (countdownTime <= 0) {
        clearInterval(timerInterval);
        form.submit();
    }


   }, 1000)

}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60; // Rename to avoid conflict
    return `${pad(minutes)}:${pad(remainingSeconds)}`;
}

function pad(num) {
    if (num < 10) {
        return '0' + num;
    }
    else {
        return num;
    }

}

