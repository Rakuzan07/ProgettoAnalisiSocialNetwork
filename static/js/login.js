function spotifyLogin() {
    const authEndpoint = 'https://accounts.spotify.com/authorize';
    const clientId = '7dfcff2789584927a64d6685f9f0d614';
    const redirectUri = encodeURIComponent('http://localhost:8000/home');
    const scopes = ['user-read-recently-played'];

    window.location = `${authEndpoint}?client_id=${clientId}&response_type=code&redirect_uri=${redirectUri}&scope=${scopes.join('%20')}&show_dialog=true`;

}