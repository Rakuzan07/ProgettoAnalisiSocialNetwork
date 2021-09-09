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
    window.location = 'http://localhost:8000/home/';
}