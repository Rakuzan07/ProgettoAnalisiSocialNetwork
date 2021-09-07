$(document).ready(function () {

    $(".boxes-img").click(function () {
        if($(this).attr("active") !== "true"){
            $(".img-active").removeClass('img-active').attr("active", "false");
            $(this).attr("active", "true");
            $(this).addClass("img-active")
        }
    });

    $("#artists").click(function () {
        $("#p1").css("font-weight", "normal");
        $("#p2").css("font-weight", "bold");
        $("#p3").css("font-weight", "normal");
        artists_rec()

    });

    $("#played").click(function () {
        $("#p1").css("font-weight", "bold");
        $("#p2").css("font-weight", "normal");
        $("#p3").css("font-weight", "normal");
        played_rec()
    });

    $("#tags").click(function () {
        $("#p1").css("font-weight", "normal");
        $("#p2").css("font-weight", "normal");
        $("#p3").css("font-weight", "bold");
        tags_rec()
    });

    $("#loginBtn").click(function () {
        login();
    });


});

function recommend_by_artists() {
    let artists = $("#art").val();
    let type = $("input[name='optradio']:checked").val();


    $("#pane").html( `<div class='spinner-grow'  style='color: #1DB954; margin-top: 5%;' role='status'>  <span class='sr-only'>Sto cercando...</span></div>
                                 <p>Sto cercando...</p>`);

    $.ajax({
        type: 'GET',
        url: "../art_recommender/",
        data: ({'artists' : artists,
                'accuracy' : type}),
        success : function (result) {
            display_recommendations(result, result['searched']);

        }, error: function (jqXHR) {
            showError(jqXHR);
        }
    })
}

function recommend_by_recently_played (token) {
    $.ajax({
        type: 'GET',
        url: '../track_recommender/',
        data: {'token' : token},
        success: function (result) {
            display_recommendations(result, "last played");
        }, error: function (jqXhr) {
            showError(jqXHR);
        }
    })

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

function artists_rec() {
    // e non sei loggato metti il bottone login
    // altrimenti metti il bottone cerca raccomandazioni

    if (getCookie('code') == null) {
         $("#pane").html(`<h1 className="display-4">Effettua  il login</h1>
        <button class='btn' id='loginBtn'><i class="fab fa-spotify"></i> Login with spotify</button>`);
    }
    else {
        $("#pane").html(`<h1 class="display-4">Inserisci una lista di artisti separati da virgole</h1>
                                
                                <input type="text" id="art" class="form-control">
                                <small id="Help" class="form-text" style="color: white; text-align: left;">Es: Ed Sheeran, Rihanna, Shakira</small>
                                <div class="row" style="margin: 1%;">
                                    <div class="form-check col-lg-4">
                                      <label class="form-check-label" for="radio1">
                                        <input type="radio" class="form-check-input" id="radio1" name="optradio" value="0.1">Somiglianza scarsa
                                      </label>
                                    </div>
                                    <div class="form-check col-lg-4">
                                      <label class="form-check-label" for="radio2">
                                        <input type="radio" class="form-check-input" id="radio2" name="optradio" value="0.2" checked>Somiglianza media
                                      </label>
                                    </div>
                                    <div class="form-check col-lg-4">
                                      <label class="form-check-label" for="radio3">
                                        <input type="radio" class="form-check-input" id="radio3" name="optradio" value="0.5">Somiglianza forte
                                      </label>
                                    </div>
                                </div>
                                <button id="search" class="btn btn-lg" ><i id="searchIcon" class="fas fa-2x fa-search"></i></button>`);

        $("#search").hover(function () {
            $("#searchIcon").css("color", "#1DB954");
        }, function () {
            $("#searchIcon").css("color", "white");
        }).click(function () {
            recommend_by_artists();
        });
    }
}



function played_rec() {
    let token = getToken();
    if(token == null){
        $("#pane").html(`<h1 class='display-4'>Effettua il login con il tuo account Spotify!</h1>                       
                                <button class='btn' id='loginBtn'><i class="fab fa-spotify"></i> Login with spotify</button>`);
    }
    else {
        $("#pane").html( `<div class='spinner-grow'  style='color: #1DB954; margin-top: 2%;' role='status'>  <span class='sr-only'>Sto cercando...</span></div>
                                 <p>Sto cercando...</p>`);
        recommend_by_recently_played(token);
    }


    $("#loginBtn").click(function () {
        login();
    });
}


function display_recommendations(result, searched) {

    let artists = "";
    if (searched === "last played"){
        artists = "ultimi ascolti";
    }
    else {
        searched.forEach(function (artist) {
            artists += artist + ", "
        });
        artists = artists.substr(0, artists.length - 2);
    }


    if(result['recommendations'][0]['similarity'] !== -1){
                $("#pane").html("").append(`<hr><h4 class="display-4" style="color: white; font-size: 3rem">Suggerimenti basati su `
                +artists +`</h4><div id='resultsDiv' class='row'></div>`);

                result['recommendations'].forEach(function (artist) {
                    if(artist['similarity'] !== -1){
                        $("#resultsDiv").append(`<div class='col-lg-2'>
                                                    <div class="flip-card card">
                                                        <div class='flip-card-inner'>
                                                            <div class="flip-card-front">
                                                                <img class='card-img-top img-fluid' src='`+artist['image']+`' alt='Image not found!' 
                                                                    artistId='`+artist['_id']+`'>
                                                                <div class='card-footer'>
                                                                    <h5 class='card-title'>`+artist['name']+`</h5>
                                                                </div>
                                                            </div>
                                                            <div class="flip-card-back">
                                                                  <h3 class='card-title' style="margin-top: 6%;">`+artist['name']+`</h3>
                                                                  <!--<button style="margin: 3%; " class="btn open" onclick="see_graph('`+artist['name'] +`')"><i class="fab fa-spotify"></i> Genera il suo grafo</button>-->
                                                                  <button style="margin: 3% 1% 1%;" class="btn open" onclick="open_on_spotify('` + artist['url'] +`')"><i class="fab fa-spotify"></i> Apri su Spotify</button>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>`);
                    }
                });
            }
            else{
                $("#pane").html("").append(`<hr><div id='resultsDiv' class='row' style="margin: 2% 0 0;">
                                                            <h4 class="display-4" style="font-size: 2rem;">Non ho trovato nulla che fa al caso tuo, prova a dimunure il grado di 
                                                            somiglianza o a cambiare lista di artisti</h4>`);
            }
}

function open_on_spotify(url) {
    window.open(url,"_blank");
}

function see_graph(artist) {
    window.open("/graph/?artist=" + artist);
}