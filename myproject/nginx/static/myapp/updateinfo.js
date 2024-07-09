document.addEventListener('DOMContentLoaded', (event)=>{

    const usernameElement = document.getElementById('username');
    const emailElement = document.getElementById('email');
    let validationErrorElement = document.getElementById('validationError');


    const validate_latest_username= () => {

        const usernameValue = usernameElement.value;


        if (usernameValue === '') {
            errorMessage.innerHTML = '';
            return;
        }

        fetch(`http://13.229.128.220:80/validate-latest-username/?username=${encodeURIComponent(usernameElement.value)}`).then(response=> response.json())
        .then(data => {

         
             let errorMessageText = ''
            

            if (data.errors.is_username_exist) {
            
                errorMessageText = 'Username already exist, Please try different username';
     
            }
            if (!data.errors.username_len_validation) {
    
                errorMessageText = 'Username must be less than 10 characters';
                
            }

                validationErrorElement.innerHTML = errorMessageText;
                
      
  

        }).catch(error => console.error(error));   

    };


    const validate_latest_email = () => {

        const emailValue = emailElement.value;


        if (emailValue === '') {
            errorMessage.innerHTML = '';
            return;
        }

        fetch(`http://13.229.128.220:80/validate-latest-email/?email=${encodeURIComponent(emailElement.value)}`).then(response=> response.json())
        .then(data => {
               console.log('Data:', data.errors)
               let errorMessageText = ''
              if (data.errors.is_email_exist) {
                errorMessageText = 'Email already exist';
              }

              if (!data.errors.is_email_valid) {
                errorMessageText = 'Email is invalid';
              }

              validationErrorElement.innerHTML = errorMessageText;
              
             

        }).catch(error => console.error(error));   

    };







    usernameElement.addEventListener('input', validate_latest_username);
    emailElement.addEventListener('input', validate_latest_email);
    

    usernameElement.addEventListener('input', () => {
        
        if (usernameElement.value === '') {
            validationErrorElement.innerHTML = '';
        }

    });



    emailElement.addEventListener('input', () => {
        
        if (emailElement.value === '') {
            validationErrorElement.innerHTML = '';
        }

    });


});