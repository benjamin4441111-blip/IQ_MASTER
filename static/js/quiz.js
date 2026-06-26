const questions = [

{
question: "What comes next? 2, 4, 8, 16, ?",
options: ["18", "24", "32", "30"],
answer: 2
},

{
question: "Which number is odd one out? 3, 5, 7, 10, 11",
options: ["3", "5", "10", "11"],
answer: 2
},

{
question: "If CAT = 24, then DOG = ?",
options: ["26", "30", "32", "34"],
answer: 0
},

{
question: "Which shape has the most sides?",
options: [
"Triangle",
"Square",
"Pentagon",
"Hexagon"
],
answer: 3
},

{
question:
"1, 1, 2, 3, 5, 8, ?",
options: ["11", "12", "13", "15"],
answer: 2
},

{
question:
"C-3, E-5, G-7, I-9, ?,? ",
options:["k-11,M-13", "M-18,K-14", "X-24,M-21", "O-15,X-24"],
answer:1
},

{
question:
"if A+D = 5, C+E=8, X+Y=?",
options:["34","49","45","52"],
answer:2
}














];

let current = 0;
let correct = 0;
let incorrect = 0;
let skipped = 0;

let totalTime = 0;
let startTime = Date.now();

const questionElement =
document.getElementById("question");

const optionsElement =
document.getElementById("options");

function loadQuestion() {

if(current >= questions.length){
finishQuiz();
return;
}

let q = questions[current];

questionElement.innerHTML =
q.question;

optionsElement.innerHTML = "";

q.options.forEach((option, index)=>{

let btn =
document.createElement("button");

btn.className = "btn";
btn.style.margin = "10px";

btn.innerHTML = option;

btn.onclick = () =>
checkAnswer(index);

optionsElement.appendChild(btn);

});

startTime = Date.now();
}

function checkAnswer(index){

let q = questions[current];

let spent =
(Date.now() - startTime)/1000;

totalTime += spent;

if(index === q.answer){
correct++;
}else{
incorrect++;
}

current++;

loadQuestion();
}

function skipQuestion(){

let spent =
(Date.now() - startTime)/1000;

totalTime += spent;

skipped++;
current++;

loadQuestion();
}

function finishQuiz(){

let avg =
(totalTime/questions.length)
.toFixed(1);

let iq =
80 + correct*10;

let form =
document.createElement("form");

form.method = "POST";
form.action = "/save_score";

form.innerHTML = `
<input name="correct"
value="${correct}">

<input name="incorrect"
value="${incorrect}">

<input name="skipped"
value="${skipped}">

<input name="avg_time"
value="${avg}">

<input name="iq_score"
value="${iq}">
`;

document.body.appendChild(form);
form.submit();
}

loadQuestion();