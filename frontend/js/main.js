let socket;

// Функция для подключения к серверу
function connectToServer(host, port, username) {
  const uri = `ws://${host}:${port}`;
  socket = new WebSocket(uri);

  socket.onopen = () => {
    console.log("Подключено к серверу");
    socket.send(JSON.stringify({ user: username }));
    showChat(username);
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    displayMessage(data);
  };

  socket.onclose = () => {
    console.log("Соединение закрыто");
    showConnectionForm();
  };

  socket.onerror = (error) => {
    console.error("Ошибка соединения:", error);
    alert("Ошибка подключения к серверу. Проверьте адрес и порт.");
    showConnectionForm();
  };
}

// Функция для отображения сообщений
function displayMessage(data) {
  const messagesDiv = document.getElementById("messages");
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");

  if (data.type === "system") {
    messageDiv.classList.add("message-system");
    messageDiv.innerHTML = `<strong>Система:</strong> ${data.message}`;
  } else if (data.type === "chat") {
    messageDiv.classList.add("message-user");
    messageDiv.innerHTML = `<strong>${data.user}:</strong> ${data.message}`;
  }

  messagesDiv.appendChild(messageDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Функция для отправки сообщения
function sendMessage() {
  const messageInput = document.getElementById("message-input");
  const message = messageInput.value.trim();

  if (message && socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: "chat", message: message }));
    messageInput.value = "";
  }
}

// Функция для отключения от сервера
function disconnect() {
  if (socket) {
    socket.close();
  }
}

// Функция для отображения формы подключения
function showConnectionForm() {
  document.getElementById("connection-form").style.display = "block";
  document.getElementById("chat-container").style.display = "none";
}

// Функция для отображения чата
function showChat(username) {
  document.getElementById("connection-form").style.display = "none";
  document.getElementById("chat-container").style.display = "block";
  document.getElementById("chat-title").textContent = `Чат (${username})`;
  document.getElementById("message-input").focus();
}

// Обработчики событий
document.addEventListener("DOMContentLoaded", () => {
  const connectForm = document.getElementById("connect-form");
  const sendBtn = document.getElementById("send-btn");
  const messageInput = document.getElementById("message-input");
  const disconnectBtn = document.getElementById("disconnect-btn");

  connectForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const host = document.getElementById("host").value;
    const port = document.getElementById("port").value;
    const username = document.getElementById("username").value;
    connectToServer(host, port, username);
  });

  sendBtn.addEventListener("click", sendMessage);

  messageInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  disconnectBtn.addEventListener("click", disconnect);
});
