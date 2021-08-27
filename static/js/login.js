function spotifyLogin() {

    const authEndpoint = 'https://accounts.spotify.com/authorize';
    const clientId = '7dfcff2789584927a64d6685f9f0d614';
    const redirectUri = encodeURIComponent('http://localhost:8000/home');
    const scopes = ['user-follow-modify'];

    window.location = `${authEndpoint}?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}&scope=${scopes.join('%20')}&show_dialog=true`;

}

function checkLogin() {
    const loginCookie = getCookie("code");
    if (loginCookie !== null) {
        window.location = 'http://localhost:8000/home'
    }
}

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return null;
}