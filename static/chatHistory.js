let login = document.getElementById("loginButton");
login.addEventListener('click',function (event) {
        event.preventDefault(); // Prevent the form from submitting normally
        getChatHistory();
    });

function getChatHistory(){

         fetch('/pythonlogin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded' // Use appropriate content type
            },
            body: `username=${encodeURIComponent('Naveen')}&password=${encodeURIComponent('naveen')}`
        })
        .then(response => response.json())
        .then(data => {
              let responseData = data.ques;
              responseData.forEach(item => {
                window.location.href = 'home/home.html';;
//        if(item.hasOwnProperty('page')){
//             window.location.href = 'home/home.html';;
//        }else{
//            window.alert(item);
//        }
        if(item.hasOwnProperty('questionsList')){
            let quesRow = document.createElement("tr");
            let quesCol = document.createElement("td");
            let queRes = document.createElement("pre");
            queRes.textContent = item.questionsList;
            quesCol.innerHTML = '';
            quesCol.appendChild(queRes);
            quesRow.appendChild(quesCol);
        }
    });
})

        .catch(error => {
//            console.error('Error:', error);
            console.log(error)
//            column3.textContent = "Error fetching response"; // Display error message
        });

}