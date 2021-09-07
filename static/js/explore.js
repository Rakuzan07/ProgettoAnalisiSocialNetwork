$(document).ready(function () {

    $("#findArtist").click(function () {
        closeNav();
        renderSearcher();
    });

    $("#recommender2").click(function () {
            showRecommenerOptions();
    })

});


function render_top_artists(client, country){
    dict = {
        'Regno Unito' : '37i9dQZEVXbLnolsZ8PSNw',
        'USA' :'37i9dQZEVXbLRQDuF5jeBp',
        'Italia' : '37i9dQZEVXbIQnj7RRhdSX',
        'Global' : '37i9dQZEVXbMDoHDwVN2tF',
        'Spagna' : '37i9dQZEVXbNFJfN1Vw8d9',
        'Germania' : '37i9dQZEVXbJiZcmkrIHGU',
        'Australia' : '37i9dQZEVXbJPcfkRz0wJ0',
        'Francia' : '37i9dQZEVXbIPWwFssbupI',
        'Irlanda' : '37i9dQZEVXbKM896FDX8L1',
        'Belgio' : '37i9dQZEVXbJNSeeHswcKB',
        'Canada' : '37i9dQZEVXbKj23U1GF4IR',
        'Portogallo' : '37i9dQZEVXbKyJS56d1pgi',
        'Messico' : '37i9dQZEVXbO3qyFxbkOE1'
    };
    let access_token = client['access_token'];
    let id = dict[country];
    $.ajax({
        type: 'GET',
        url: 'https://api.spotify.com/v1/playlists/'+ id,
        headers: { 'Authorization' : 'Bearer ' + access_token },
        success: function (result) {
            let artists = {}

            for (var i=0; i < result['tracks']['items'].length; i++){
                var name = result['tracks']['items'][i]['track']['artists'][0]['id'];
                if(name in artists){
                    artists[name] = artists[name] + 1
                }
                else {
                    artists[name] = 1
                }
            }
            var ret_val = []
            for (i=0; i < 12; i++){
                var keys   = Object.keys(artists);
                var highest = Math.max.apply(null, keys.map(function(x) { return artists[x]} ));
                var match  = keys.filter(function(y) { return artists[y] === highest });
                match.forEach(function (artist) {
                    ret_val.push(artist);
                    delete artists[artist];
                });
            }

            artists = ret_val.slice(0,12);
            $("#artistsDiv").html("");
            console.log(country);
            $("#TopArtists").text("Top Artists "+country);
            artists.forEach(function (artist) {
                $.ajax({
                    type: 'GET',
                    url: 'https://api.spotify.com/v1/artists/' + artist,
                    headers: {'Authorization': 'Bearer ' + access_token},
                    success: function (result) {
                        var name = result['name'];
                        var url = "https://open.spotify.com/artist/" + artist;
                        var image = result['images'][0]['url'];
                        var genres = '';
                        result['genres'].forEach(function (genre) {
                            genres += genre+', ';
                        });
                        genres = genres.substring(0, genres.length - 2);
                        var followers = result['followers']['total'];
                        var popularity = result['popularity'];
                        $("#artistsDiv").append(`<div class='col-lg-3'>
                                                    <div class="flip-card card" data-aos="zoom-in-up" data-aos-duration="1800">
                                                        <div class='flip-card-inner'>
                                                            <div class="flip-card-front">
                                                                <img class='card-img-top img-fluid' src='`+image+`' alt='Card image' artistId='`+artist+`'>
                                                                <div class='card-footer'>
                                                                    <h4 class='card-title'>`+name+`</h4>
                                                                </div>
                                                            </div>
                                                            <div class="flip-card-back">
                                                                  <h3 class='card-title' style="margin-top: 6%;">`+name+`</h3>
                                                                  <p>Seguaci: `+followers+`</p>
                                                                  <p>Popolarità: `+popularity+`</p>
                                                                  <p>Generi: `+genres+`</p>
                                                                  <button style="margin: 1%;" class="btn open" onclick="change_album('` + artist +`',false)"><i class="fab fa-spotify"></i> Ascolta ultimo album</button>
                                                                  <button style="margin: 1%;" class="btn open" onclick="open_on_spotify('` + url +`')"><i class="fab fa-spotify"></i> Apri su Spotify</button>
                                                            </div>
                                                        
                                                        </div>
                                                    </div>
                                                    
                                                 </div>`);

                        $(".card-img-top").click(function () {
                            change_album($(this).attr('artistId'),false);
                        })
                    }, error: function (jqXHR) {
                        showError(jqXHR);
                    }
                });
                change_album(artists[0],true);

            });
        }, error: function (jqXHR) {
            location.reload();
        }
    });

}

function open_on_spotify(url) {
    window.open(url,"_blank");
}

function change_album(artist_id, first_time) {
        $.ajax({
            type: 'GET',
            data: {'id' : artist_id},
            url: '/get_last_album/',
            success: function (result) {
                $("#player").attr('src', result['url']);
                if(first_time === false){
                    window.scrollTo({top: document.body.scrollHeight, behavior:"smooth"});
                }
            },
            error: function (jqXHR) {
                showError(jqXHR);
            }
        });
}