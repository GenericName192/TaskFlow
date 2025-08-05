var chatBotModal = document.getElementById("chatbotModal")

chatBotModal.addEventListener("shown.bs.modal", function(){
    // Remove aria-hidden when modal is shown to fix accessibility issue
    this.removeAttribute("aria-hidden");
    document.getElementById("chatbotToggle").style.visibility = "hidden";
    document.getElementById("chatInput").focus();
    document.getElementById("sendButton").addEventListener("click", sendMessage);
    document.getElementById("chatInput").addEventListener("keydown", check_keystroke)})

chatBotModal.addEventListener("hidden.bs.modal", function(){
    // Add aria-hidden when modal is hidden
    this.setAttribute("aria-hidden", "true");
    document.getElementById("chatbotToggle").style.visibility = "visible";
    document.getElementById("sendButton").removeEventListener("click", sendMessage);
    document.getElementById("chatInput").removeEventListener("keydown", check_keystroke)})

function check_keystroke(event){
    if (event.key === "Enter"){
            sendMessage();
    }
}

function sendMessage(){
    const input = document.getElementById("chatInput");
    const chat = document.getElementById("chatMessages");
    const userID = document.getElementById("user_id").value;

    if (input.value.trim() !== ""){
        const date = new Date()
        const time = date.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        });
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", "user-message");
        const message = document.createElement("span");
        message.classList.add("message-content");
        message.innerText = input.value;
        const timeStamp = document.createElement("span");
        timeStamp.classList.add("time-stamp");
        timeStamp.textContent = time;
        messageDiv.appendChild(message);
        messageDiv.appendChild(timeStamp);
        chat.appendChild(messageDiv);
        messageDiv.scrollIntoView({behavior: "smooth"})

        const loadingIcon = document.createElement("div");
        loadingIcon.setAttribute("id", "loading");
        loadingIcon.innerHTML = `<div class="spinner-grow spinner-grow-sm" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <div class="spinner-grow spinner-grow-sm" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>`;
        chat.appendChild(loadingIcon);
        messageDiv.scrollIntoView({behavior: "smooth"})

        // sendMessageToDjango(input.value, userID);
        input.value = ""
    }
}

function displayReply(reply){
    const chat = document.getElementById("chatMessages");
    chat.removeChild(chat.lastChild);
    const now = new Date();
    const time = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message", "bot-message");
    const message = document.createElement("span");
    message.classList.add("message-content");
    message.innerHTML = `<i class="fas fa-robot me-2"></i>${reply.value}`;
    const timeStamp = document.createElement("span");
    timeStamp.classList.add("time-stamp");
    timeStamp.textContent = time;
    messageDiv.appendChild(message);
    messageDiv.appendChild(timeStamp);
    chat.appendChild(messageDiv);
    messageDiv.scrollIntoView({behavior: "smooth"})
}

function sendMessageToDjango(user_message, user_id){

}