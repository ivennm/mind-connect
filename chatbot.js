document.getElementById("chatButton").addEventListener("click", () => {
    document.getElementById("chatPopup").style.display = "block";
    document.getElementById("chatPopup").classList.add("open");
    document.getElementById("chatButton").style.display = "none"; // Hide button
    document.getElementById("userInput").focus();
    loadChatHistory(); // Load saved messages
});

document.getElementById("closeChat").addEventListener("click", () => {
    document.getElementById("chatPopup").style.display = "none";
    document.getElementById("chatPopup").classList.remove("open");
    document.getElementById("chatButton").style.display = "block"; // Show button again
});

document.getElementById("sendMessage").addEventListener("click", async () => {
    let userInput = document.getElementById("userInput").value.trim();
    if (userInput !== "") {
        await sendMessage(userInput);
    }
});

document.getElementById("userInput").addEventListener("keydown", async (e) => {
    if (e.key === "Enter") {
        let userInput = document.getElementById("userInput").value.trim();
        if (userInput !== "") {
            await sendMessage(userInput);
        }
    }
});

async function sendMessage(userInput) {
    let chatContent = document.getElementById("chatContent");
    if (!chatContent) {
        console.error("chatContent element not found.");
        return;
    }

    // Display User Message
    let userMessage = document.createElement("p");
    userMessage.innerHTML = `<strong>You:</strong> ${userInput}`;
    chatContent.appendChild(userMessage);

    saveMessage("You", userInput); // Save message in localStorage

    document.getElementById("userInput").value = "";

    // Fetch AI Response
    try {
        let response = await fetch("/get-response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        });

        let data = await response.json();

        // Display AI Response
        let botMessage = document.createElement("p");
        botMessage.innerHTML = `<strong>Bot:</strong> ${data.response}`;
        chatContent.appendChild(botMessage);

        saveMessage("Bot", data.response); // Save bot response

    } catch (error) {
        let errorMessage = document.createElement("p");
        errorMessage.innerHTML = `<strong>Bot:</strong> Sorry, something went wrong.`;
        chatContent.appendChild(errorMessage);
        saveMessage("Bot", "Sorry, something went wrong."); // Save error message
    }

    chatContent.scrollTop = chatContent.scrollHeight;
}

// Save chat messages in local storage
function saveMessage(sender, text) {
    let messages = JSON.parse(localStorage.getItem("chatHistory")) || [];
    messages.push({ sender, text });
    localStorage.setItem("chatHistory", JSON.stringify(messages));
}

// Load chat history
function loadChatHistory() {
    let chatContent = document.getElementById("chatContent");
    let messages = JSON.parse(localStorage.getItem("chatHistory")) || [];

    chatContent.innerHTML = ""; // Clear old messages before loading

    messages.forEach(({ sender, text }) => {
        let messageElement = document.createElement("p");
        messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatContent.appendChild(messageElement);
    });

    chatContent.scrollTop = chatContent.scrollHeight;
}
