/* jshint esversion: 11*/
const chatBotModal = document.getElementById("chatbotModal");

chatBotModal.addEventListener("shown.bs.modal", function () {
  // Remove aria-hidden when modal is shown to fix accessibility issue
  this.removeAttribute("aria-hidden");
  sessionStorage.setItem("chat-log", JSON.stringify([])); // Initialize empty array
  document.getElementById("chatbotToggle").style.visibility = "hidden";
  document.getElementById("chatInput").focus();
  document.getElementById("sendButton").addEventListener("click", sendMessage);
  document
    .getElementById("chatInput")
    .addEventListener("keydown", check_keystroke);
});

chatBotModal.addEventListener("hidden.bs.modal", function () {
  // Add aria-hidden when modal is hidden
  this.setAttribute("aria-hidden", "true");
  sessionStorage.removeItem("chat-log"); // Clear conversation history
  document.getElementById("chatbotToggle").style.visibility = "visible";
  document
    .getElementById("sendButton")
    .removeEventListener("click", sendMessage);
  document
    .getElementById("chatInput")
    .removeEventListener("keydown", check_keystroke);
});

function check_keystroke(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

function sendMessage() {
  const input = document.getElementById("chatInput");
  const chat = document.getElementById("chatMessages");
  const userId = document.getElementById("sendButton").dataset.user;

  if (input.value.trim() !== "") {
    const date = new Date();
    const time = date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    let conversation = JSON.parse(sessionStorage.getItem("chat-log")) || [];
    conversation.push({
      role: "user",
      content: input.value, 
    });
    sessionStorage.setItem("chat-log", JSON.stringify(conversation)); // Save back to storage

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
    messageDiv.scrollIntoView({ behavior: "smooth" });

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
    messageDiv.scrollIntoView({ behavior: "smooth" });

    sendMessageToDjango(conversation, userId); // Send full conversation history
    input.value = "";
  }
}

function displayReply(reply) {
  const chat = document.getElementById("chatMessages");
  chat.removeChild(chat.lastChild);
  const now = new Date();
  const time = now.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });

  let conversation = JSON.parse(sessionStorage.getItem("chat-log")) || [];
  conversation.push({
    role: "assistant",
    content: reply.response || reply.value || reply,
  });
  sessionStorage.setItem("chat-log", JSON.stringify(conversation)); // Save back to storage

  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chat-message", "bot-message");
  const message = document.createElement("span");
  message.classList.add("message-content");
  message.innerHTML = `<i class="fas fa-robot me-2"></i>${reply.response || reply.value || reply}`;
  const timeStamp = document.createElement("span");
  timeStamp.classList.add("time-stamp");
  timeStamp.textContent = time;
  messageDiv.appendChild(message);
  messageDiv.appendChild(timeStamp);
  chat.appendChild(messageDiv);
  messageDiv.scrollIntoView({ behavior: "smooth" });
}

function sendMessageToDjango(conversation, user_id) {
  let url = "/chat-bot/";  // Use absolute URL with leading slash
  const csrftoken = getCookie("csrftoken");
  try {
    fetch(url, {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken, "Content-Type": "application/json" },
      body: JSON.stringify({ user: user_id, conversation: conversation }), // Send conversation instead of message
    })
      .then((response) => response.json())
      .then((data) => {
        // get the actual message from the response data
        displayReply(data);
      })
      .catch((error) =>
        displayReply("Something has gone wrong: " + String(error))
      );
  } catch (error) {
    displayReply("Something has gone wrong: " + String(error));
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
