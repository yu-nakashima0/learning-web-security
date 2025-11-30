const socket = io();

// Register user with server
socket.emit("connect_user", window.currentUser);

const messageInput = document.getElementById("chat_input");
const receiverInput = document.getElementById("receiver");
const sendBtn = document.getElementById("send-btn");
const chatDisplay = document.getElementById("chat-display");

// Send message
sendBtn.onclick = () => {
    const msg = messageInput.value.trim();
    const receiver = receiverInput.value.trim();
    const sender = window.currentUser;

    if (!msg || !receiver) return;

    socket.emit("chat_message", {
        sender: sender,
        receiver: receiver,
        message: msg
    });

    messageInput.value = "";
};

// Receive message
socket.on("chat_message", (data) => {
    const p = document.createElement("p");
    p.innerHTML = `<b>${data.sender}</b> → <i>${data.receiver}</i>: ${data.message}`;
    chatDisplay.appendChild(p);
});
