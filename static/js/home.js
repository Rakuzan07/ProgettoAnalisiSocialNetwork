
function setCookie(refresh){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const code = urlParams.get('code');
    if (code !== null) {
        document.cookie = "code=" + code + "; path=/";
    }

    if (refresh !== null) {
        document.cookie = "refresh_token=" + refresh + "; path=/";
    }

}

function getArtist(){
    cookie = getCookie('code');
    window.location='http://127.0.0.1:8000/artist/?token='+cookie;
    console.log("test");
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