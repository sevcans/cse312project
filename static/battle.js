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
    console.log(content.message);
    if (content.message == "On going battle"){
        document.getElementById('Result').textContent = content.message;
    }else{
    }
}