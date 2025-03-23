// Open Chat Popup when the button is clicked
document.getElementById("chatButton").addEventListener("click", () => {
    openChat();
    loadChatHistory(); // Load saved messages
});

// Close Chat Popup
document.getElementById("closeChat").addEventListener("click", closeChat);

// Send Message via Text
document.getElementById("sendMessage").addEventListener("click", async () => {
    let userInput = document.getElementById("userInput").value.trim();
    if (userInput !== "") {
        await sendMessage(userInput);
    }
});

// Handle Enter Key for Sending Message
document.getElementById("userInput").addEventListener("keydown", async (e) => {
    if (e.key === "Enter") {
        let userInput = document.getElementById("userInput").value.trim();
        if (userInput !== "") {
            await sendMessage(userInput);
        }
    }
});

// Send the User Message and Get AI Response
async function sendMessage(userInput) {
    let chatContent = document.getElementById("chatContent");

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
        saveMessage("Bot", "Sorry, something went wrong.");
    }

    chatContent.scrollTop = chatContent.scrollHeight;
}

// Save Messages in Local Storage
function saveMessage(sender, text) {
    let messages = JSON.parse(localStorage.getItem("chatHistory")) || [];
    messages.push({ sender, text });
    localStorage.setItem("chatHistory", JSON.stringify(messages));
}

// Load Chat History from Local Storage
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

// Open and Close Chat Popup
function openChat() {
    document.getElementById("chatPopup").style.display = "block";
    document.getElementById("chatButton").style.display = "none"; // Hide the button when popup is open
}

function closeChat() {
    document.getElementById("chatPopup").style.display = "none";
    document.getElementById("chatButton").style.display = "block"; // Show the button again when popup is closed
}

// Handle Voice Recognition for Microphone
document.getElementById("startVoiceBtn").addEventListener("click", function () {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US'; // Set language for recognition

    recognition.onstart = function () {
        console.log("Voice recognition started.");
    };

    recognition.onresult = function (event) {
        const speechResult = event.results[0][0].transcript; // Get the result from speech
        console.log("Recognized Speech: ", speechResult);
        document.getElementById("userInput").value = speechResult; // Set result to input field
    };

    recognition.onerror = function (event) {
        console.error("Error with voice recognition: ", event.error);
    };

    recognition.start();
});

// Handle Camera Functionality
document.getElementById("startCameraBtn").addEventListener("click", function () {
    // Access the camera
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            // Attach the video stream to a video element
            const videoElement = document.createElement('video');
            videoElement.srcObject = stream;
            videoElement.play();
            document.body.appendChild(videoElement);

            // Optionally, add a stop button to stop the video stream
            const stopButton = document.createElement('button');
            stopButton.innerHTML = "Stop Camera";
            stopButton.addEventListener('click', function () {
                stream.getTracks().forEach(track => track.stop()); // Stop the camera stream
                videoElement.remove(); // Remove the video element
                stopButton.remove(); // Remove the stop button
            });
            document.body.appendChild(stopButton);
        })
        .catch(function (error) {
            console.error("Error accessing camera: ", error);
        });
});
