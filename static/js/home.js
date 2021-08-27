
function setCookie(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const code = urlParams.get('code');
    if (code !== null) {
        document.cookie = "code=" + code;
    }
}