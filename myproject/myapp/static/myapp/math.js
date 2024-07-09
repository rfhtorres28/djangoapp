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

function validateForm() {
    const formData = new FormData(form);

    var csrftokenelement = document.getElementsByName('csrfmiddlewaretoken')[0];
        csrftoken = csrftokenelement ? csrftokenelement.value : null;

        fetch(form.action, {method:'POST', headers: {'X-CSRFToken':csrftoken, 'X-Requested-With':'XMLHttpRequest', 'accept': 'application/json'}, body:formData})
        .then(response => response.json())
        .then(data => {
            console.log("Data", data);
            if (data) {
                
                if (data.error) {

                    alert(data.error);
                    
                }
                else {
                    form.submit();
                }
            }

        }).catch(error => console.error(error));


}