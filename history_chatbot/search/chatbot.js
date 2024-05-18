"use strict";
const Groq = require("groq-sdk");
const groq = new Groq({
    apiKey: "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"
});

document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", async () => {
        const userMessage = messageInput.value;
        if (userMessage.trim() === "") return;

        addMessageToChatBox("user", userMessage);

        const chatCompletion = await getGroqChatCompletion(userMessage);
        const botMessage = chatCompletion.choices[0]?.message?.content || "Error getting response from the bot.";
        
        addMessageToChatBox("bot", botMessage);
    });

    function addMessageToChatBox(role, message) {
        const messageElement = document.createElement("div");
        messageElement.className = role === "user" ? "user-message" : "bot-message";
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        messageInput.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});

async function getGroqChatCompletion(userMessage) {
    return groq.chat.completions.create({
        messages: [
            {
                role: "user",
                content: userMessage
            }
        ],
        model: "llama3-8b-8192"
    });
}
