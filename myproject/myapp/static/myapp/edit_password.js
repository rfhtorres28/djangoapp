document.addEventListener('DOMContentLoaded', function (){

    const form = document.getElementById('myForm')

    form.addEventListener('submit', function(event){
        event.preventDefault(); //prevent the form from submitting
 

        var formData = new FormData(form);

        var csrftokenelement = document.getElementsByName('csrfmiddlewaretoken')[0]
        if (csrftokenelement) {
            csrftoken = csrftokenelement.value;
        }
        else {
            csrftoken = null;
        }

        var xml = new XMLHttpRequest();
        xml.open("POST", form.action, true); 
        xml.setRequestHeader('X-CSRFToken', csrftoken);
        xml.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xml.onload = function (){

            var errorResponse = JSON.parse(xml.responseText);
            if (errorResponse.errors) {
                
                // Check if errorResponse.errors.old_password is an array or list
                if (Array.isArray(errorResponse.errors.old_password)){
                    var oldErrorMessage = errorResponse.errors.old_password[0];
                }
                else {
                    var oldErrorMessage = '';
                }
              
                if (Array.isArray(errorResponse.errors.new_password2)){
                    var newErrorMessages = errorResponse.errors.new_password2;
                    var newErrorMessage = '';
                    for (let i=0; i<newErrorMessages.length; i++) {
                     newErrorMessage += `${newErrorMessages[i]}\n`
                    }
                }
                else {
                    var newErrorMessages = '';
                }
                

                let errorMessage = oldErrorMessage + '\n' + newErrorMessage;
                alert(errorMessage);
                window.location.reload();
                }
        
                
            else {
             
                    alert(errorResponse.message);
                    window.location.href = `/account/${errorResponse.username}`;
                   
                }
                
            }
       

        xml.onerror = function() {
            console.log('An error occurred during the transaction');
        };

        xml.send(formData); //send the formData via AJAX request

}); 

});

