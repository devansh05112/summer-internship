// ==========================================
// CEREBRA AI FLASHCARDS
// ==========================================
let mastered = [];

let favorites = [];

const finishScreen =
document.getElementById("finishScreen");

const masterBtn =
document.getElementById("masterBtn");

const favoriteBtn =
document.getElementById("favoriteBtn");

const studyAgain =
document.getElementById("studyAgain");


let currentCard = 0;

// Elements
const flashcard = document.getElementById("flashcard");

const question = document.getElementById("question");
const hint = document.getElementById("hint");
const answer = document.getElementById("answer");

const progressFill = document.getElementById("progressFill");
const cardCounter = document.getElementById("cardCounter");
const progressPercent = document.getElementById("progressPercent");

const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const shuffleBtn = document.getElementById("shuffleBtn");
const restartBtn = document.getElementById("restartBtn");

// ==========================================
// Update Card
// ==========================================

function loadCard(index){

    if(flashcards.length===0) return;

    flashcard.classList.remove("flipped");

    question.textContent = flashcards[index].question;
    hint.textContent = flashcards[index].hint;
    answer.textContent = flashcards[index].answer;

    cardCounter.textContent =
        `Card ${index+1} / ${flashcards.length}`;

    const percent =
        ((index+1)/flashcards.length)*100;

    progressFill.style.width = percent+"%";

    progressPercent.textContent =
        Math.round(percent)+"%";

    prevBtn.disabled = currentCard===0;

    nextBtn.disabled =
    currentCard===flashcards.length-1;

}

// ==========================================
// Flip Card
// ==========================================

flashcard.addEventListener("click",()=>{

    flashcard.classList.toggle("flipped");

});

// ==========================================
// Next
// ==========================================

nextBtn.addEventListener("click", () => {

    if (currentCard < flashcards.length - 1) {

        currentCard++;

        loadCard(currentCard);

    } else {

        finishScreen.style.display = "block";

    }

});

// ==========================================
// Previous
// ==========================================

prevBtn.addEventListener("click",()=>{

    if(currentCard>0){

        currentCard--;

        loadCard(currentCard);

    }

});

// ==========================================
// Restart
// ==========================================

restartBtn.addEventListener("click",()=>{

    currentCard=0;

    loadCard(currentCard);

});

// ==========================================
// Shuffle
// ==========================================

shuffleBtn.addEventListener("click",()=>{

    flashcards.sort(()=>Math.random()-0.5);

    currentCard=0;

    loadCard(currentCard);

});

// ==========================================
// Keyboard
// ==========================================

document.addEventListener("keydown",(e)=>{

    if(e.code==="Space"){

        e.preventDefault();

        flashcard.classList.toggle("flipped");

    }

    if(e.key==="ArrowRight"){

        nextBtn.click();

    }

    if(e.key==="ArrowLeft"){

        prevBtn.click();

    }

});

masterBtn.addEventListener("click",()=>{

    if(!mastered.includes(currentCard)){

        mastered.push(currentCard);

        masterBtn.innerHTML="✅ Mastered";

    }

});

favoriteBtn.addEventListener("click",()=>{

    if(favorites.includes(currentCard)){

        favorites=
        favorites.filter(x=>x!==currentCard);

        favoriteBtn.innerHTML="❤️ Favorite";

    }

    else{

        favorites.push(currentCard);

        favoriteBtn.innerHTML="💙 Saved";

    }

});

// ==========================================
// Initialize
// ==========================================

loadCard(currentCard);

// ==========================================
// Study Again
// ==========================================

studyAgain.addEventListener("click",()=>{

    finishScreen.style.display="none";

    currentCard=0;

    loadCard(currentCard);

});

let startX=0;

flashcard.addEventListener("touchstart",e=>{

    startX=e.touches[0].clientX;

});

flashcard.addEventListener("touchend",e=>{

    let endX=e.changedTouches[0].clientX;

    if(endX-startX>70){

        prevBtn.click();

    }

    if(startX-endX>70){

        nextBtn.click();

    }

});