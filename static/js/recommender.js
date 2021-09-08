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
        followship_rec()
    });

});

function recommend_by_artists() {

    $("#pane").html( `<div class='spinner-grow'  style='color: #1DB954; margin-top: 5%;' role='status'>  <span class='sr-only'>Sto cercando...</span></div>
                                 <p>Sto cercando...</p>`);

    $.ajax({
        type: 'GET',
        url: "../art_recommender/",
        success : function (result) {
            console.log("entrato");
            display_recommendations(result, "artist");
        }, error: function (jqXHR) {
            showError(jqXHR);
        }
    })
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

function do_login() {
    window.location = "http://localhost:8000/login";
}

function artists_rec() {
    // e non sei loggato metti il bottone login
    // altrimenti metti il bottone cerca raccomandazioni

    if (getCookie('code') == null) {
         $("#pane").html(`<h1 className="display-4">Effettua  il login</h1>
        <button class='btn' id='loginBtn' onclick=do_login()><i class="fab fa-spotify"></i> Login with spotify</button>`);
    }
    else {
        $("#pane").html(`<h1 class="display-4">Inizia la ricerca</h1>
                               <button class='btn' id='recommend' onclick=recommend_by_artists()><i id="searchIcon" class="fas fa-2x fa-search">Cerca</button>`);
        $("#search").hover(function () {
            $("#searchIcon").css("color", "#1DB954");
        }, function () {
            $("#searchIcon").css("color", "white");
        }).click(function () {
            recommend_by_artists();
        });
    }
}



function followship_rec() {
    if (getCookie('code') == null) {
         $("#pane").html(`<h1 className="display-4">Effettua  il login</h1>
        <button class='btn' id='loginBtn' onclick=do_login()><i class="fab fa-spotify"></i> Login with spotify</button>`);
    }
    else {
        $("#pane").html(`<h1 class="display-4">Inizia la ricerca</h1>
                               <button class='btn' id='recommend' onclick=recommend_by_followship()><i id="searchIcon" class="fas fa-2x fa-search">Cerca</button>`);
        $("#search").hover(function () {
            $("#searchIcon").css("color", "#1DB954");
        }, function () {
            $("#searchIcon").css("color", "white");
        }).click(function () {
            recommend_by_artists();
        });
    }
}

function recommend_by_followship() {
    $("#pane").html( `<div class='spinner-grow'  style='color: #1DB954; margin-top: 5%;' role='status'>  <span class='sr-only'>Sto cercando...</span></div>
                                 <p>Sto cercando...</p>`);

    $.ajax({
        type: 'GET',
        url: "../foll_rec/",
        success : function (result) {
            display_recommendations(result, "followship");
        }, error: function (jqXHR) {
            showError(jqXHR);
        }
    })
}


function display_recommendations(result, type) {


            if (type === 'followship'){
                $("#pane").html("").append(`<hr><h4 class="display-4" style="color: white; font-size: 3rem">Suggerimenti basati sugli utenti seguiti</h4><div id='resultsDiv' class='row'></div>`);
            }
            else {
                $("#pane").html("").append(`<hr><h4 class="display-4" style="color: white; font-size: 3rem">Suggerimenti basati sugli artisti seguiti</h4><div id='resultsDiv' class='row'></div>`);
            }

            if (result.length > 0){
                result.forEach(function (artist) {
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
                                                               <button style="margin: 3% 1% 1%;" class="btn open" onclick="open_on_spotify('` + artist['url'] +`')"><i class="fab fa-spotify"></i> Apri su Spotify</button>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>`);

                });
            }
            else{
                $("#pane").html("").append(`<hr><div id='resultsDiv' class='row' style="margin: 2% 0 0;">
                                                            <h4 class="display-4" style="font-size: 2rem;">Non ho trovato nulla che fa al caso tuo</h4>`);
            }
}

function open_on_spotify(url) {
    window.open(url,"_blank");
}