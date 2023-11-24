window.addEventListener('load', function () {
//    let questionForm = document.getElementById("questionForm");
    let subBut = document.getElementById("sub");
    let newChat = document.getElementById("newChat");
    let username1 = document.querySelector("p");
    var usernameText = username1.textContent;
    var usernameinput = usernameText.split('Hello User, ')[1].slice(0, -1);
    var questionsBody = document.getElementById("questionsBody");
    getQuestionsFromServer();
    function getQuestionsFromServer() {
    fetch('/get_all_questions')
    .then(response => response.json())
    .then(data => {
        let allQuestions = data.allQuestions;

        allQuestions.forEach(item => {
             if (item.hasOwnProperty('questionsList')) {
                   let questions = item.questionsList;
                  questions.forEach(questionItem => {
                          let question = questionItem.question;
                          let shortenedQuestion = question.substring(0, 40);
                          console.log('Question:', question);
                          let quesRow = document.createElement("tr");
                          let quesCol = document.createElement("td");
                          let atag = document.createElement("a");
                          let queRes = document.createElement("pre");
                           atag.href = '#'; // Set the href attribute to '#' or your desired link
        atag.textContent = shortenedQuestion; // Display shortenedQuestion as the hyperlink text

        // Append the anchor tag to the table cell
        quesCol.innerHTML = '';
        atag.appendChild(queRes);
        quesCol.appendChild(atag);
        quesRow.appendChild(quesCol);
        questionsBody.appendChild(quesRow);
//                          queRes.textContent = shortenedQuestion;
//                          quesCol.innerHTML = '';
//                          atag.appendChild(queRes)
//                          quesCol.appendChild(atag);
//                          quesRow.appendChild(quesCol);
//                          questionsBody.appendChild(quesRow)
            // Perform actions with 'question' (here, it logs each question to the console)
        });
    }
//            console.log(item.questionsList);
//            let quesRow = document.createElement("tr");
//            let quesCol = document.createElement("td");
//            let queRes = document.createElement("pre");
//            queRes.textContent = item.questionsList.question;
//            quesCol.innerHTML = '';
//            quesCol.appendChild(queRes);
//            quesRow.appendChild(quesCol);
//            questionsBody.appendChild(quesRow)
        })
        // Use allQuestions data as needed
//        console.log(allQuestions);
        // Perform actions with allQuestions data
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error
    });
}

    newChat.addEventListener('click',function(event){
        event.preventDefault();
        clearTableData();
    });


    subBut.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the form from submitting normally
        getQuestion();
    });


    function clearTableData(){
        var tbody = document.getElementById("reqres");
         while (tbody.firstChild) {
             tbody.removeChild(tbody.firstChild);
       }
    }

    function getQuestion() {
        let questionInput = document.getElementById("question");
        let question = questionInput.value;

        // Create table row elements and append the question
        let tbody = document.getElementById("reqres");

          let row1 = document.createElement("tr");
        let row2 = document.createElement("tr");

        let column1 = document.createElement("td");
        let column2 = document.createElement("td");
        let column3 = document.createElement("td");
        let column4 = document.createElement("td");

        column2.textContent = question;
        column3.textContent = "Fetching response..."; // Placeholder for the response

        row1.appendChild(column1);
        row1.appendChild(column2);
        tbody.appendChild(row1);


        // Make an asynchronous request to the server
        fetch('/pythonresult/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded' // Use appropriate content type
            },
            body: `question=${encodeURIComponent(question)}&username=${encodeURIComponent(usernameinput)}`
        })
        .then(response => response.json())
        .then(data => {
              let responseData = data.resp;
              responseData.forEach(item => {
        if ('response' in item) {
            // Display response in a pre element
            let preResponse = document.createElement("pre");
            preResponse.textContent = item.response;
//            responseColumn.appendChild(preResponse);
             column3.innerHTML = '';
            column3.appendChild(preResponse);
        }
    });
})

        .catch(error => {
            console.error('Error:', error);
            column3.textContent = "Error fetching response"; // Display error message
        });
         row2.appendChild(column3);
        row2.appendChild(column4);
        tbody.appendChild(row2);

    }
});


















//window.addEventListener('load', function () {
//window.alert("Hi there");
//let submit = document.getElementById("sub");
//let ques = document.getElementById("question");
//let tbody = document.getElementById("reqres");
//submit.onclick = getQuestion;
//
//function getQuestion(){
//    let question = ques.value;
//    let row = document.createElement("tr");
//    let column1 = document.createElement("td");
//    let column2 = document.createElement("td");
//    column2.textContent = question;
//    row.appendChild(column1);
//    row.appendChild(column2);
//    tbody.appendChild(tbody);
//}
//})