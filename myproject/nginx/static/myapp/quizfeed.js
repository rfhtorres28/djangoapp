document.addEventListener('DOMContentLoaded', (event)=>{
    let url = `ws://13.229.128.220:80/ws/socket-server`; 

    const socketServer = new WebSocket(url);
    

    //attach onmessage event to handle incomming websocket messages
    socketServer.onmessage = function (jsonData) {
          let json_data = JSON.parse(jsonData.data)
          console.log("Data:", json_data);
       
    
    
        if (json_data.type === 'quiz_result') {
            let messageDiv = document.getElementById('scrollable')
            let quizResultDiv = document.createElement('div');
            quizResultDiv.className = 'quiz-post';

     

            quizResultDiv.innerHTML = `
                <div class="post-header">
                    <img src="${json_data.user_pic}" alt="Example Image" class="user_profile_image" width="70px" height="70px">
                    <span style="margin-left: 5%;">
                        <a href="/account/${json_data.username}" style="text-decoration: none;">@${json_data.username}</a> got
                        <span style="color: red; margin-left: 2px;">${json_data.score_percentage}%</span> in ${json_data.subject} Quiz
                    </span>
                    <br>
                </div>
                <span style="font-size: 15px; margin-top: 4%;">Answered 0s ago</span>
            `;

            messageDiv.prepend(quizResultDiv); 


             }

             


            
   };
 


});



// Creating an server instance of  Websocket


