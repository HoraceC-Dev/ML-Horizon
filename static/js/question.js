import { createProjectRequirement } from "../js/chat.js";

// Get references to important elements
const questionBody = document.getElementById("questionBody");
questionBody.innerHTML = '<link rel="stylesheet" href="../static/css/question.css"><div class="quiz-container" id="quiz-container"><form id="quiz-form"></form><button type="button" id="back-btn" style="display: none;">Back</button></div>';

const quizForm = document.getElementById("quiz-form");
const backBtn = document.getElementById("back-btn");
const result = document.getElementById("result");
let questions = [];
const questionsText = {
                        "What is your experience level": ["Beginner", "Intermediate", "Advanced", "Expert"],
                        "What application are you interested in": ["Image Recognition", "Applicaiton 2", "Aon 3", "Applicaiton 4", "Applon 5", "Apon 6",
                            "Application 1", "Applicaiton 2", "Application 3", "Applicaiton 4", "Ation 5"],
                        "What algorithm do you want to use": ["Linear regression", "Alg","Algori 3","Algohm 4","Algo 5",]};
const answer = ["","",""];
let index = 0;
let isApl = false;
let experience = {"Beginner" : "Low to no experience", "Intermediate" : "Done a bit of coding", "Advanced" : "Pretty good at coding", "Expert" : "Very good at coding"};
let [algorithm, application] = await loadQuestions();

backBtn.addEventListener("click", () => back());


async function loadQuestions() {
    let algorithm = await fetch('../../static/algorithms.json')
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch(error => console.error('Error:', error));
    let application = await fetch('../../static/applications.json')
    .then(response => response.json())
    .then(data => {
        return data
    })
    .catch(error => console.error('Error:', error));
    return [algorithm, application];
}

export function generateQuestion() {
    questionBody.style.display = "flex";
    expOptions();

}

function expOptions() {
    let question = "What is your Experience";
    let [q, answerOptions] = makeTitleBox(question);
    for(let option in experience) {
        let answerBox = createAnswerBox(option, experience[option]);
        answerOptions.appendChild(answerBox);
    }
    quizForm.appendChild(q);
}

function appOptions() {
    let question = "What is the application";
    let [q, answerOptions] = makeTitleBox(question);
    for(let option in application) {
        let answerBox = createAnswerBox(option, application[option]);
        answerOptions.appendChild(answerBox);
    }
    let answerBox = createAnswerBox("Any", "Any Algorithm");
    answerOptions.appendChild(answerBox);
    quizForm.appendChild(q);
    q.style.display = "none";
}

function algOptions(app) {

    let question = "What is the Algorithm";
    let [q, answerOptions] = makeTitleBox(question);
    if(app != "Any") {
        let algo = algorithm[app];
        for(let option in algo) {
            let answerBox = createAnswerBox(option, algo[option]);
            answerOptions.appendChild(answerBox);
        }
    }
    let answerBox = createAnswerBox("Any", "Any Algorithm");
    answerOptions.appendChild(answerBox);

    quizForm.appendChild(q);
}

function makeTitleBox(question) {
    const q = document.createElement("div");
    const answerOptions = document.createElement("div");
    const title = document.createElement("p");
    title.innerHTML = question;
    q.className = "question";
    answerOptions.className = "answer-options";
    questions.push(q);
    q.appendChild(title);
    q.appendChild(answerOptions);
    if(index != 0) {
        const other = createOtherButton();
        q.appendChild(other);
    }
    return [q, answerOptions];
}

function createAnswerBox(option, description) {
    const answerBox = document.createElement('div');
    answerBox.className = "answer-box";

    const answerButton = createAnswerButton(option);
    const answerDescription = createAnswerDescription(description);
    addHoveringFunctionality(answerButton, answerDescription);

    answerBox.appendChild(answerButton);
    answerBox.appendChild(answerDescription);
    return answerBox;
}

function createAnswerButton(option) {
    const opt = document.createElement("button");
    opt.className = "answer-message";
    opt.type = "button";
    opt.innerHTML = option;
    opt.onclick = function () {
        answer[index] = opt.innerHTML;
        const currentQuestion = questions[index];
        currentQuestion.style.display = "none";
        if (index == 0) {
            index += 1;
            appOptions();
            questions[index].style.display = "block";
            backBtn.style.display = "block";
        }
        else if (index == 1) {
            index += 1;
            algOptions(option);
            questions[index].style.display = "block";
            backBtn.style.display = "block";
        }
        else if(index == 2) {
            submit();
        }
        setTimeout(() => {
            let question = questions[index];
            question.classList.remove('hidden');
            question.style.animation = 'slideIn 0.5s forwards';
        }, 500); 
    }
    
    return opt;
}

function createAnswerDescription(description) {
    const popupBoxContainer = document.createElement('div');
    popupBoxContainer.className = "popup-box-container";
    popupBoxContainer.textContent = description;
    popupBoxContainer.style.display = "none";
    return popupBoxContainer;
}

function addHoveringFunctionality(answerContainer, popupBox) {
    answerContainer.addEventListener("mousemove", (e) => {
        //const x = document.documentElement.clientWidth / 2;
        //const y = document.documentElement.clientHeight / 2;
        const rect = answerContainer.getBoundingClientRect();
        const x = rect.left;
        const y = rect.top;
        const pop = popupBox.getBoundingClientRect();
        const popx = pop.width / 2;
        const popy = pop.height / 2;
        popupBox.style.left = `${e.clientX - x + popx }px`;
        popupBox.style.top = `${e.clientY - y + popy + 80}px`;
        popupBox.style.display = "block";
    });
    answerContainer.addEventListener("mouseleave", () => {
        popupBox.style.display = "none";
        //setTimeout(() => {popupBox.style.display = "none";}, 10);
    });

}

function createOtherButton() { 
    const otherContainer = document.createElement("div");
    const otherButton = document.createElement("button");
    const inputContainer = document.createElement("div");
    const otherInput = document.createElement("input");
    const submitButton = document.createElement("button");

    otherContainer.className = "other-container";

    otherButton.className = "answer-box";
    otherButton.type = "button";
    otherButton.innerHTML = "Others";
    otherButton.onclick = function() {
        inputContainer.style.display = "flex";
        otherButton.style.display = "none";
    };

    inputContainer.className = "input-container";
    inputContainer.style.display = "none";

    otherInput.type = "text";
    otherInput.className = "textInput";
    otherInput.placeholder = "Type Here";

    submitButton.className = "submit-btn";
    //submitButton.classList = "submit-btn answer-box";
    submitButton.type = "button";
    submitButton.innerHTML = "Submit";
    submitButton.onclick = function() {
        answer[index] = otherInput.value.trim();
        const currentQuestion = questions[index];
        currentQuestion.style.display = "none";
        if(index == 2) {
            submit();
        }else{
            index += 1;
            algOptions();
            questions[index].style.display = "block";
            backBtn.style.display = "block";
        }
    };


    inputContainer.appendChild(otherInput);
    inputContainer.appendChild(submitButton);
    otherContainer.appendChild(otherButton);
    otherContainer.appendChild(inputContainer);
    return otherContainer;
}


function submit() {
    backBtn.style.display = "none";
    questionBody.style.display = "none";
    console.log(answer);
    questionBody.remove();
    createProjectRequirement(answer);
}

function back() {
    if(index == 1) backBtn.style.display = "none";
    answer[index] = "";
    const currentQuestion = questions[index];
    currentQuestion.style.display = "none";
    questions[index-1].style.display = "block";
    index -= 1;
    questions.splice(index + 1, 1);
    quizForm.removeChild(quizForm.lastElementChild);
}

//generateQuestion();
