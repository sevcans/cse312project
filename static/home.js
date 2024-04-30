const { json } = require("express");

const randomCrusaderStuff = [
    "Crusader armor evolved over time, starting with chainmail shirts and helmets in the early Crusades, and later incorporating plate armor during the later Crusades.",
    "Chainmail, consisting of interlocking metal rings, was a common form of protection for Crusaders, providing flexibility and coverage against slashing attacks.",
    "Crusader helmets varied in design but often included nasal helmets, which featured a nose guard for facial protection, or the iconic 'Great Helm,' a fully enclosed helmet with eye slits and a flat top.",
    "Plate armor became more prevalent among Crusaders in the 12th and 13th centuries, offering superior protection against thrusting attacks and ranged weapons like arrows.",
    "Crusader armor was often adorned with religious symbols such as crosses, indicating the wearer's devotion to Christianity and their participation in holy wars.",
    "Shields were essential pieces of Crusader armor, providing additional protection in battle. They were typically made of wood, reinforced with metal rims and bosses for added durability.",
    "Crusader knights sometimes wore surcoats over their armor, which displayed their heraldic symbols and helped identify them on the battlefield.",
    "Crusader armor was expensive and typically only affordable for nobles and wealthier knights, limiting its availability to the upper echelons of Crusader society.",
    "The weight of Crusader armor varied depending on its composition and design, with full suits of plate armor weighing anywhere from 40 to 60 pounds.",
    "Despite advancements in armor technology, Crusaders still faced significant risks on the battlefield, including injury from blunt force trauma, exhaustion, and the limitations of their protective gear against certain weapons."
  ];

var socket = null;



function randomText() {
    document.getElementById("randomText").innerHTML = "<br/>"+randomCrusaderStuff[Math.floor(Math.random()*9)]
}

function updateOnlineList(data) {
    html = ""
    data = JSON.parse(data)
    for(const username of data){
        html += "<span id='userName' style='height:2vh'>" + username + "</span>";
    }
    const list = document.getElementById("onlineList");
    list.innerHTML = html
}

async function updateUserList() {

    const response = await fetch("/userList",{
        method: "GET",
        headers:{
            "Content-Type": "application/json",
            'X-Content-Type-Options': 'nosniff'
          }});
        
        const content = await response.json();
        for(const user of content){
            addUserToList(user);
        }    
}

function createSocket(){
    socket = io();
        socket.on('connect',function(){
            socket.emit("create-connection")
        });
        socket.on("chat-event", (data) => {
            addMessageToChat(JSON.parse(data))
        });
        socket.on("onlineList", (data) => {
            updateOnlineList(data)
        });
}

function welcome() {
    document.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            sendChat();
        }
    });
    document.getElementById("chat-text-box").focus();
    updateUserList();
    updateChat();
    // setInterval(updateChat, 5000);
    createSocket();
}

// let messageHTML = "<br><button class ='requestBattle' onclick='requestBattle(\"" + username + "\")'>Battle</button> ";
// let messageHTML = "<br><button class ='requestBattle' onclick='requestBattle(\"" + username + "\")'>Battle</button> ";
//     messageHTML += "<span id='chat-messages'>"+username+ " | " + message + "</span>";

function chatMessageHTML(messageJSON) {
    var username = messageJSON.username;
    var message = messageJSON.message;    
    var upvote = messageJSON.upvote.length;
    if(upvote == 0){upvote = ""}
    var downvote = messageJSON.downvote.length;
    if(downvote == 0){downvote = ""}
    var uid = messageJSON.id;
    var profile = messageJSON.profile;
    let messageHTML = "<br><br><button class='chat-username'>" +username+"</button>";
    messageHTML +="<span class='chat-messages'>"+message+"<button onclick='upvote("+uid+",\""+username+"\")' class='chat-upvote'>"+upvote+" ^</button> <button onclick='downvote("+uid+",\""+username+"\")' class='chat-downvote'>"+downvote+" v</button> <img src='"+profile+"' alt='image' class='profile_img'></span>";
    return messageHTML;   
}
function addMessageToChat(messageJSON) {
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML += chatMessageHTML(messageJSON);
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

async function sendChat(){
    // get text from chat box
    var chatTextBox = document.getElementById("chat-text-box").value
      
    // create response based on what is expected at server chat messages
    if(socket){
        socket.emit("chat",{message:chatTextBox})
    }else{
        const response = await fetch("/chat-messages",{
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    'X-Content-Type-Options': 'nosniff'},
                body: JSON.stringify({'message': chatTextBox})
        }).then((response)=>{return response.json()}).then((content)=>{
            if(content.message == "posted"){
            document.getElementById("chat-text-box").value = "";}    
        });   
    }
}

async function updateChat() {
       const response = await fetch("/chat-messages",{
        method: "GET",
        headers:{
            "Content-Type": "application/json",
            'X-Content-Type-Options': 'nosniff'}        
        });
        clearChat();
        const content = await response.json();
        for(const message of content){
            addMessageToChat(message);
        }
}

function clearChat() {
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.innerHTML = "";
}

async function logout(){
    const response = await fetch("/logout",{
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'X-Content-Type-Options': 'nosniff'
      },
    });
    const content = await response.json();
    console.log(response.json.message)
    if (content.message == 'Logged Out Successful'){
      window.location.replace("/");
      document.getElementById('LogOutMessage').textContent = content.message;
    }
  }

  
async function upvote(uid, username){
    const response = await fetch("/upvote",{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'X-Content-Type-Options': 'nosniff'
        },
        body: JSON.stringify({"id": uid, "username": username})
      });
  }
  
async function downvote(uid, username){
    const response = await fetch("/downvote",{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'X-Content-Type-Options': 'nosniff'
        },
        body: JSON.stringify({"id": uid, "username": username})
      });
    }

function battle_redirect() {
    window.location.replace("/battle");
}
function profile_redirect() {
    window.location.replace("/profile");
}
