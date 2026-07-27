const questions = document.querySelectorAll(".question");

const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
const submitBtn = document.getElementById("submitBtn");

const progressBar = document.getElementById("progressBar");
const currentQuestion = document.getElementById("currentQuestion");

let current = 0;

// ================================
// Show Question
// ================================

function showQuestion(index) {

    questions.forEach(question => {
        question.classList.add("hidden");
    });

    questions[index].classList.remove("hidden");

    currentQuestion.innerText = index + 1;

    let progress = ((index + 1) / questions.length) * 100;

    progressBar.style.width = progress + "%";

    prevBtn.style.display =
        index === 0 ? "none" : "inline-block";

    if (index === questions.length - 1) {

        nextBtn.style.display = "none";

        submitBtn.style.display = "inline-block";

    } else {

        nextBtn.style.display = "inline-block";

        submitBtn.style.display = "none";

    }

}

// ================================
// Next
// ================================

nextBtn.addEventListener("click", function () {

    if (current < questions.length - 1) {

        current++;

        showQuestion(current);

    }

});

// ================================
// Previous
// ================================

prevBtn.addEventListener("click", function () {

    if (current > 0) {

        current--;

        showQuestion(current);

    }

});

// ================================
// Submit Quiz
// ================================

submitBtn.addEventListener("click", function () {

    let answersArray = [];

    for (let i = 0; i < questions.length; i++) {

        const selected = document.querySelector(
            `input[name="q${i}"]:checked`
        );

        if (selected) {

            answersArray.push(
                parseInt(selected.value)
            );

        } else {

            answersArray.push(-1);

        }

    }

    document.getElementById("answersInput").value =
        JSON.stringify(answersArray);

    document.getElementById("quizForm").submit();

});

// ================================
// Keyboard Navigation
// ================================

document.addEventListener("keydown", function (e) {

    if (e.key === "ArrowRight") {

        if (current < questions.length - 1) {

            current++;

            showQuestion(current);

        }

    }

    if (e.key === "ArrowLeft") {

        if (current > 0) {

            current--;

            showQuestion(current);

        }

    }

});

// ================================
// Initialize
// ================================

showQuestion(0);