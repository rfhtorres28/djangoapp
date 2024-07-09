document.addEventListener('DOMContentLoaded', () => {


    const form = document.getElementById('myForm');
    const username = document.getElementById('username');
    const email = document.getElementById('email');
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const errorMessage = document.getElementById('errorMessage');
    var remainingError = []; 
    
    const validate_username = () => {

        const usernameValue = username.value;

        if (usernameValue === '') {
            errorMessage.innerHTML = '';
            return;
        }

        fetch(`http://172.17.0.1:80/validate-username/?username=${encodeURIComponent(usernameValue)}`).then(response => response.json())
        .then(data => {


            if (data.errors) {
                
                const len_error = data.errors.len_error;
                const username_exist = data.errors.username_exist;

                console.log(data.errors);

                if (len_error) {
                    errorMessage.innerHTML = 'Username must be less than 10 characters';
                    remainingError.push('Username must be less than 10 characters');
                
                }
                else if (username_exist) {
                    errorMessage.innerHTML = 'Username already exist. Please try another username';
                    remainingError.push('Username already exist. Please try another username');

                }
                else {
                    errorMessage.innerHTML = '';
;                }
            }



        }).catch(error => console.error('Error:', error))
    };


    const validate_email = () => {

        const emailValue = email.value;

        if (emailValue === '') {
            errorMessage.innerHTML = '';
            return;
        }

        fetch(`http://172.17.0.1:80/validate-email/?email=${encodeURIComponent(emailValue)}`).then(response => response.json())
        .then(data => {
            console.log('Data:', data);
            
            let errorMessageText = '';

            if (data.errors.email_exist) {
                errorMessageText =  'Email already exists. Please try another email';
                remainingError.push('Email already exists. Please try another email');
            } 

            if (data.errors.wrong_email_format) {
                errorMessageText = 'Email format is incorrect';
                remainingError.push('Email format is incorrect');
            }
            
            errorMessage.innerHTML = errorMessageText;
            

        }).catch(error => console.error('Error:', error))
    };



    const validate_password = () => {

        const password1Value = password1.value;


        if (password1Value === '') {
            errorMessage.innerHTML = '';
            return;
        }

        fetch(`http://172.17.0.1:80/validate-password/?password1=${encodeURIComponent(password1Value)}`).then(response => response.json())
        .then(data => {
            
            
            if (Array.isArray(data.errors.password_error)) {
                const errorList = data.errors.password_error;
                let errorMessageText = '';

                errorList.forEach(errorElement=>{

                    errorMessageText += errorElement + '\n';

                });

                errorMessage.innerHTML = errorMessageText;
                console.log(errorMessageText);
            } else if (!data.errors.password_error) {
                  errorMessage.innerHTML = ''
            }
           
            

        }).catch(error => console.error('Error:', error))
    };



    const validate_passwords = () => {

        const password1Value = password1.value;
        const password2Value = password2.value;


        if (password2Value === '') {
            errorMessage.innerHTML = '';
            return;
        }

        fetch(`http://172.17.0.1:80/validate-passwords/?password1=${encodeURIComponent(password1Value)}&password2=${encodeURIComponent(password2Value)}`).then(response => response.json())
        .then(data => {
            
            console.log(data);

            if(data.errors.match_passwords) {
                errorMessage.innerText = '';
            } 
            else {

                errorMessage.innerText = 'Passwords dont match. Please try again';
            }
            


        }).catch(error => console.error('Error:', error))
    };

     
   

// addEventListener input for username, email and password1 field

    username.addEventListener('input', validate_username);
    email.addEventListener('input', validate_email);
    password1.addEventListener('input', validate_password);
    password2.addEventListener('input', validate_passwords);
    
    


// Delete the error message if username and email field is empty
    username.addEventListener('input', () => {
        
        if (username.value === '') {
            errorMessage.innerHTML = '';
        }

    });

    email.addEventListener('input', () => {
        
        if (email.value === '') {
            errorMessage.innerHTML = '';
        }
    });


    password1.addEventListener('input', () => {    
        if (password1.value === '') {
            errorMessage.innerHTML = '';
        }
    });

    password2.addEventListener('input', () => {    
        if (password2.value === '') {
            errorMessage.innerHTML = '';
        }
    });


    form.addEventListener('submit', function(event) {
    
        event.preventDefault();

        var formData = new FormData(form);
        var csrftokenelement = document.getElementsByName('csrfmiddlewaretoken')[0];

        csrftoken = csrftokenelement ? csrftokenelement.value : null;

        fetch(form.action, {method:'POST', headers: {'X-CSRFToken':csrftoken, 'X-Requested-With':'XMLHttpRequest'}, body:formData})
        .then(response => response.json()).then(function(data){
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
           
          }).catch(error => console.error('Error:', error))
    
    

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