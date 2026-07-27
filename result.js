// ===============================
// Animated Score
// ===============================

const scoreElement = document.getElementById("scoreValue");

const finalScore = parseInt(scoreElement.innerText);

let current = 0;

const counter = setInterval(() => {

    current++;

    scoreElement.innerText = current;

    if (current >= finalScore) {

        clearInterval(counter);

    }

}, 20);


// ===============================
// Doughnut Chart
// ===============================

const ctx = document.getElementById("quizChart");

new Chart(ctx, {

    type: "doughnut",

    data: {

        labels: [

            "Correct",

            "Wrong",

            "Not Attempted"

        ],

        datasets: [{

            data: [

                correct,

                wrong,

                skipped

            ],

            backgroundColor: [

                "#22C55E",

                "#EF4444",

                "#F59E0B"

            ],

            borderWidth: 0,

            hoverOffset: 18

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        cutout: "70%",

        animation: {

            animateRotate: true,

            animateScale: true,

            duration: 1800

        },

        plugins: {

            legend: {

                position: "bottom",

                labels: {

                    color: "#ffffff",

                    padding: 20,

                    font: {

                        size: 15,

                        weight: "bold"

                    }

                }

            },

            tooltip: {

                backgroundColor: "#111827",

                titleColor: "#fff",

                bodyColor: "#fff",

                padding: 15,

                cornerRadius: 12

            }

        }

    }

});


// ===============================
// Card Animation
// ===============================

const cards = document.querySelectorAll(".review-card");

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if(entry.isIntersecting){

            entry.target.style.opacity = 1;

            entry.target.style.transform = "translateY(0px)";

        }

    });

});

cards.forEach(card=>{

    card.style.opacity=0;

    card.style.transform="translateY(40px)";

    card.style.transition=".6s";

    observer.observe(card);

});


// ===============================
// Confetti 🎉
// ===============================

if(finalScore>=90){

for(let i=0;i<120;i++){

const confetti=document.createElement("div");

confetti.className="confetti";

confetti.style.left=Math.random()*100+"vw";

confetti.style.animationDelay=Math.random()*3+"s";

confetti.style.background=

["#2563EB","#22C55E","#F59E0B","#EF4444"][Math.floor(Math.random()*4)];

document.body.appendChild(confetti);

}

}