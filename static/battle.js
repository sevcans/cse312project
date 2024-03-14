async function find_battle(){
    const response = await fetch("/find_battle",{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'X-Content-Type-Options': 'nosniff'
        },
    });
    const content = await response.json();
    console.log(content.message);
    if (content.message == "Battle Found"){
        phealth = "Health: "+ content.player_health
        pDamage = "Damage: "+ content.player_damage
        bhealth = "Health: "+ content.bot_health
        bDamage = "Damage: "+ content.bot_damage
        document.getElementById('UserName').textContent = content.player_name;
        document.getElementById('Player_Image_ID').src = content.player_image;
        document.getElementById('player_hp_info').textContent = phealth;
        document.getElementById('player_dmg_info').textContent = pDamage;

        document.getElementById('BotName').textContent = content.bot_name;
        document.getElementById('Bot_Image_ID').src = content.bot_image;        
        document.getElementById('bot_hp_info').textContent = bhealth;
        document.getElementById('bot_dmg_info').textContent = bDamage;

        document.getElementById("attack_button").style.display = "block";
        document.getElementById("defense_button").style.display = "block";
        document.getElementById('Result').textContent = content.message;
        setTimeout(function() {
            document.getElementById('Result').textContent = "";
        }, 3500);
    }
}

async function generate_battle(){
    const response = await fetch("/gen_battle",{
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'X-Content-Type-Options': 'nosniff'
        },
    });
    const content = await response.json();
    if (content.message == "Ongoing Battle"){
        document.getElementById('Result').textContent = content.message;
        setTimeout(function() {
            document.getElementById('Result').textContent = "";
        }, 3500);
    }else{
        phealth = "Health: "+ content.player_health
        pDamage = "Damage: "+ content.player_damage
        bhealth = "Health: "+ content.bot_health
        bDamage = "Damage: "+ content.bot_damage
        document.getElementById('UserName').textContent = content.player_name;
        document.getElementById('Player_Image_ID').src = content.player_image;
        document.getElementById('player_hp_info').textContent = phealth;
        document.getElementById('player_dmg_info').textContent = pDamage;

        document.getElementById('BotName').textContent = content.bot_name;
        document.getElementById('Bot_Image_ID').src = content.bot_image;        
        document.getElementById('bot_hp_info').textContent = bhealth;
        document.getElementById('bot_dmg_info').textContent = bDamage;

        document.getElementById("attack_button").style.display = "block";
        document.getElementById("defense_button").style.display = "block";
        document.getElementById('Result').textContent = content.message;
        setTimeout(function() {
            document.getElementById('Result').textContent = "";
        }, 3500);
    }
}