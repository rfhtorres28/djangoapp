document.addEventListener('DOMContentLoaded', function(){

    const form = document.getElementById('myForm');

    form.addEventListener('submit', function(event) {
    
    event.preventDefault();

    var formData = new FormData(form);
    var csrftokenelement = document.getElementsByName('csrfmiddlewaretoken')[0]
        if (csrftokenelement) {
            csrftoken = csrftokenelement.value;
        }
        else {
            csrftoken = null;
        }

    fetch(form.action, {method:'POST', headers: {'X-CSRFToken':csrftoken, 'X-Requested-With':'XMLHttpRequest'}, body:formData})
    .then(function(response){
        if (response){
            return response.json();
           }
    })
    .then(function(data){
        console.log(data); 
        resetFormStyles();

        if (data.errors) {

          // checking if there is an error in the username field
          if (data.errors && data.errors.username && Array.isArray(data.errors.username)) {
              var usernameError = data.errors.username[0];
              console.log(usernameError);
          }
          else{
              var usernameError = '';
          }

          // checking if there is an error in the email field
          if (data.errors && data.errors.email &&Array.isArray(data.errors.email)) {
              var emailError = data.errors.email[0]
              console.log(emailError);
          }
          else {
              var emailError = '';
          }

          //checking if there is an error in the password field
          if (data.errors && data.errors.password2 && Array.isArray(data.errors.password2)) {
              var passwordErrorArray = data.errors.password2;
              console.log(passwordErrorArray);
          }
          else {
              var passwordErrorArray = '';
          }

         
          var passwordError = ''
      
          for (let i=0; i<passwordErrorArray.length; i++){
              passwordError += `${passwordErrorArray[i]}\n`;
          }


          if (usernameError) {
              const usernameElement = document.getElementById('username');
              usernameElement.style.setProperty('border-color', '#e74c3c', 'important');
          } 

          if (emailError){
              const emailElement = document.getElementById('email');
              emailElement.style.borderColor = '#e74c3c';
          }

          if (passwordError){
              const password1Element = document.getElementById('password1');
              const password2Element = document.getElementById('password2');
              password1Element.style.borderColor = '#e74c3c';
              password2Element.style.borderColor = '#e74c3c';
          }

          var errorMessage = usernameError + '\n' + emailError + '\n' + passwordError;
          console.error('hehe', errorMessage);
        
          // displays the alert message after 1sec to ensure that the setPropery of the fields with errors will be applied first before displaying the error message
          if (errorMessage) {
              setTimeout(function(){
                alert(errorMessage);
              }, 1000);   
          }
    
      } else {
          form.submit();
      }
       
      })
      .catch(
          function(error){
          console.error(error);
      })


function resetFormStyles() {
    const elements = ['username', 'email', 'password1', 'password2'];
    elements.forEach(function(id) {
    const element = document.getElementById(id);
        if (element) {
            element.style.removeProperty('border-color');
            element.style.removeProperty('background-color');
        }
    });
}




});
});