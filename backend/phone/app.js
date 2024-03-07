// @ts-nocheck

const userSelectorBtn = document.querySelector('#user-selector')
const botSelectorBtn = document.querySelector('#bot-selector')
const chatHeader = document.querySelector('.chat-header')
const chatMessages = document.querySelector('.chat-messages')
const chatInputForm = document.querySelector('.chat-input-form')
const chatInput = document.querySelector('.chat-input')
const clearChatBtn = document.querySelector('.clear-chat-button')

const messages = JSON.parse(localStorage.getItem('messages')) || []
const topic = config.MQTT_TOPIC;
const topic_door = config.MQTT_DOOR_TOPIC;
const broker = config.MQTT_IP;
let client;
let payload;

const createChatMessageElement = (message) => `
  <div class="message ${message.sender === 'User' ? 'blue-bg' : 'gray-bg'}">
    <div class="message-sender">${message.sender}</div>
    <div class="message-text">${message.text}</div>
    <div class="message-timestamp">${message.timestamp}</div>
  </div>
`

window.onload = () => {
  messages.forEach((message) => {
    chatMessages.innerHTML += createChatMessageElement(message)
  })
}

let messageSender = 'User'

const updateMessageSender = (name) => {
  messageSender = name
  //chatHeader.innerText = `${messageSender} chatting...`
  //chatInput.placeholder = `Type here, ${messageSender}...`

  if (name === 'User') {
    userSelectorBtn.classList.add('active-person')
    botSelectorBtn.classList.remove('active-person')
  }
  if (name === 'Bot') {
    botSelectorBtn.classList.add('active-person')
    userSelectorBtn.classList.remove('active-person')
  }

  /* auto-focus the input field */
  chatInput.focus()
}

userSelectorBtn.onclick = () => updateMessageSender('User')
botSelectorBtn.onclick = () => updateMessageSender('Bot')

const sendMessage = (e) => {
  //e.preventDefault()

  const timestamp = new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
  const message = {
    sender: messageSender,
    text: chatInput.value,
    timestamp,
  }

  /* Save message to local storage */
  messages.push(message)
  localStorage.setItem('messages', JSON.stringify(messages))

  /* Add message to DOM */
  chatMessages.innerHTML += createChatMessageElement(message)

  /* Clear input field */
  chatInputForm.reset()

  /*  Scroll to bottom of chat messages */
  chatMessages.scrollTop = chatMessages.scrollHeight
}

chatInputForm.addEventListener('submit', sendMessage)

clearChatBtn.addEventListener('click', () => {
  localStorage.clear()
  chatMessages.innerHTML = ''
})


window.addEventListener("load", (event) => {
  let chat_header = document.getElementById("chat-header");
  //let msg = document.getElementById("msg");

  const options = {
      clean: true,
      connectTimeout: 4000,
      port: config.MQTT_PORT,
      username: config.MQTT_USER,
      password: config.MQTT_PASSWORD,
  };
  const client = mqtt.connect("wss://" + broker, options);

  client.on("connect", function () {
      chat_header.textContent = "OwlDoor (Connected)."
      client.subscribe(topic);
      client.subscribe(topic_door);
      client.subscribe("connection/#")
  });

  client.on("message", (topic, message) => {
      const decoder = new TextDecoder('utf-8'); // Specify the encoding, utf-8 is commonly used
      let payload = decoder.decode(message);
      console.log(topic, payload)
      if (topic == "phone/image") {
        chatInput.value = `OwlDoor erspäht:<br>
        <img id="image" src="${payload}" width="160" height="120" />`

        updateMessageSender('Bot')
        sendMessage(null);
        updateMessageSender('User')
      }
      else if (topic == "face"){
        chatInput.value = `OwlDoor erspäht ${payload} vor deiner Haustür!`

        updateMessageSender('Bot')
        sendMessage(null);
        updateMessageSender('User')
      }
      else {
        chatInput.value = payload

        updateMessageSender('Bot')
        sendMessage(null);
        updateMessageSender('User')
      }
  });
});
