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

function home_redirect() {
    window.location.replace("/home");
}

async function getProfile(){
    const response = await fetch("/profile_stats",{
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'X-Content-Type-Options': 'nosniff'
      },
    });
    const content = await response.json();
    if (content.message == 'Profile Found' && content.image != ''){
      document.getElementById('user_profile_image').src = content.image
    }
}