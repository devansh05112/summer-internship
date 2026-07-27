// =======================================
// CEREBRA AI - Chat JS
// =======================================

const form = document.getElementById("chatForm");
const textarea = document.getElementById("question");
const chatBox = document.getElementById("chatBox");
const newChat = document.getElementById("newChat");
const prompts = document.querySelectorAll(".prompt");

// =======================================
// Auto Resize Textarea
// =======================================

textarea.addEventListener("input", () => {

    textarea.style.height = "auto";

    textarea.style.height = textarea.scrollHeight + "px";

});

// =======================================
// Enter to Send
// Shift + Enter = New Line
// =======================================

textarea.addEventListener("keydown", function(e){

    if(e.key === "Enter" && !e.shiftKey){

        e.preventDefault();

        form.requestSubmit();

    }

});

// =======================================
// Time
// =======================================

function currentTime(){

    return new Date().toLocaleTimeString([],{

        hour:"2-digit",

        minute:"2-digit"

    });

}

// =======================================
// Add User Message
// =======================================

function addUserMessage(message){

    chatBox.innerHTML += `

    <div class="user-wrapper">

        <div class="message-row user-row">

            <div class="user-message">

                ${message}

            </div>

            <div class="avatar user-avatar">

                👤

            </div>

        </div>

        <div class="time">

            ${currentTime()}

        </div>

    </div>

    `;

}

// =======================================
// Typing Indicator
// =======================================

function showTyping(){

    chatBox.innerHTML += `

    <div id="typing" class="bot-wrapper">

        <div class="bot-message">

            <div class="typing">

                <span></span>

                <span></span>

                <span></span>

            </div>

        </div>

    </div>

    `;

    chatBox.scrollTop = chatBox.scrollHeight;

}

function removeTyping(){

    const t = document.getElementById("typing");

    if(t){

        t.remove();

    }

}

// =======================================
// Copy Button
// =======================================

function copyAnswer(text){

    navigator.clipboard.writeText(text);

}

// =======================================
// Add AI Message
// =======================================

function addBotMessage(message){

    const html = marked.parse(message);

    chatBox.innerHTML += `

    <div class="bot-wrapper">

        <div class="message-row">

            <div class="avatar bot-avatar">

                🤖

            </div>

            <div class="bot-message">

                ${html}

            </div>

        </div>

        <div class="message-tools">

            <button onclick='copyAnswer(${JSON.stringify(message)})'>

                📋 Copy

            </button>

            <span class="time">

                ${currentTime()}

            </span>

        </div>

    </div>

    `;

    chatBox.scrollTop = chatBox.scrollHeight;

}

// =======================================
// Send Message
// =======================================

async function sendMessage(question){

    addUserMessage(question);

    showTyping();

    textarea.value = "";

    textarea.style.height = "58px";

    const data = new FormData();

    data.append("question", question);

    try{

        const response = await fetch("/ask",{

            method:"POST",

            body:data

        });

        const result = await response.json();

        removeTyping();

        addBotMessage(result.answer);

    }

    catch(err){

        removeTyping();

        addBotMessage("❌ Unable to contact Cerebra AI.");

    }

}

// =======================================
// Submit
// =======================================

form.addEventListener("submit", function(e){

    e.preventDefault();

    const question = textarea.value.trim();

    if(question==="") return;

    sendMessage(question);

});

// =======================================
// Prompt Buttons
// =======================================

prompts.forEach(button=>{

    button.addEventListener("click",function(){

        sendMessage(this.innerText);

    });

});

// =======================================
// New Chat
// =======================================

newChat.addEventListener("click",function(){

    chatBox.innerHTML = `

        <div class="welcome">

            <h1>Welcome 👋</h1>

            <p>

                Ask questions from your uploaded notes.

            </p>

        </div>

        <div class="suggestions">

            <button class="prompt">Explain this chapter</button>

            <button class="prompt">Give key points</button>

            <button class="prompt">Summarize the notes</button>

            <button class="prompt">Ask me MCQs</button>

        </div>

    `;

});