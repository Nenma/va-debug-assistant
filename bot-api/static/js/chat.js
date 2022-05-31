const content = document.querySelector('.conversation-wrapper');
const message = document.querySelector('#message-text');

const addChatBubble = (message, sender, type) => {
    let messageSent = document.createElement('div');
    let messageSentBubble = document.createElement('div');
    let messageSentTime = document.createElement('div');
    let messageSentAvatar = document.createElement('div');
    let messageSentTimestamp = document.createElement('div');
    let messageSentStatus = document.createElement('div');

    messageSent.className = type;
    messageSentBubble.className = 'bubble';
    messageSentTime.className = 'time';
    messageSentTimestamp.className = 'timestamp';
    messageSentAvatar.className = 'avatar';
    messageSentStatus.className = 'status';


    messageSentBubble.innerHTML = message;
    messageSentAvatar.innerHTML = sender;
    messageSentTime.innerHTML = new Date().getHours() + ':' + new Date().getMinutes();


    messageSentTime.appendChild(messageSentStatus);
    messageSentTimestamp.appendChild(messageSentTime);
    messageSentTimestamp.appendChild(messageSentAvatar);


    messageSent.appendChild(messageSentBubble);
    messageSent.appendChild(messageSentTimestamp);

    content.appendChild(messageSent);
}

document.querySelector('.send').addEventListener('click', async (event) => {
    event.preventDefault();

    // ================ USER MESSAGE ================
    addChatBubble(message.value, 'ME', 'message-sent');

    // ================ BOT MESSAGE ================
    let res = await fetch('http://localhost:5000/send', {
        method: 'POST',
        body: JSON.stringify({ 'message': message.value }),
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow'
    });
    res = await res.json();

    if (res.original_question) {
        addChatBubble(`This was the original question: ${res.original_question}`, 'DA', 'message-received');
    }
    addChatBubble(res.answer, 'DA', 'message-received');
    if (res.question_link) {
        addChatBubble(`You can find more here ${res.question_link}`, 'DA', 'message-received');
    }
    
    message.value = '';
});

document.querySelector('.location').addEventListener('click', (event) => {

    event.preventDefault();

    let messageLocation = document.createElement('div');
    let messageLocationText = document.createElement('div');

    messageLocation.className = 'message-location';
    messageLocationText.className = 'location';

    messageLocationText.innerHTML = "<p>You can have leisurely dialogue with me! Try telling me something!</p><p>If you are struggling with a dev problem, try asking 'I have a question ...' followed by your topic!<p></p>If you want to know more about a certain fact, try saying 'Tell me more about ...' followed by your topic!</p>";
    messageLocation.appendChild(messageLocationText);

    content.appendChild(messageLocation);
});