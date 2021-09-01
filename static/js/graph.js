function render_graph() {
    $("#graphDiv").html(`<div class='spinner-grow'  style='color: #1DB954; margin-top: 40%;' role='status'>  <span class='sr-only'>Retrieving data...</span></div>
                                 <p>Sto caricando...</p>`);
    // let diameter = 3;
    $.ajax({
            type: 'GET',
            url: '/get_graph/',
            data: {
            },
            dataType: 'json',
            success: function (result) {
            console.log(result);
                $("#graphDiv").html("");
                $("#sidebar").css("background-color", "#29323c").css("border", "1px solid black").css("border-radius", "10px")
                    .css("padding-top", "1%").css("height", "100vh");
                if(!$("#artistCard").length){
                    $("#sidebar").append('<div class="card" id="artistCard"></div>')
                        .append('<iframe id="player" src="https://open.spotify.com/embed/playlist/37i9dQZEVXbMDoHDwVN2tF" style="margin-top: 5%;" width="280" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>');
                    $("#artistCard").css("height", "60%");
                }
                drawArtistsGraph(result["links"], result["nodes"]);
                window.scrollTo(0, document.body.scrollHeight);
            },
            error: function (jqXHR) {
                showError(jqXHR);
            }
        });

}

function drawArtistsGraph(links, Nodes){
    first_info(Object.keys(Nodes)[0]);
    let nodes = {};

    links.forEach(function (link) {
            link.source = nodes[link.source] || (nodes[link.source] = {name: link.source});
            link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});
    });

    var width = $("#graphDiv").width();
    var height = $("#pane").height();

    var force = d3.layout.force()
        .nodes(d3.values(nodes))
        .links(links)
        .size([width, height])
        .linkDistance(150)
        .charge(-1000)
        .on("tick", tick)
        .start();

    var svg = d3.select("#graphDiv").append("svg")
        .attr("id", "artistsGraph")
        .attr("width", width)
        .attr("height", height);

    svg.append("text").attr("x", 10).attr("y", 10).text("Genres:")
        .style("font-size", "15px").style("fill", "white").attr("alignment-baseline","middle");
    svg.append("circle").attr("cx",20).attr("cy",30).attr("r", 6).style("fill", "#FF0000");
    svg.append("circle").attr("cx",20).attr("cy",60).attr("r", 6).style("fill", '#ff9900');
    svg.append("circle").attr("cx",20).attr("cy",90).attr("r", 6).style("fill", '#0066ff');
    svg.append("circle").attr("cx",20).attr("cy",120).attr("r", 6).style("fill", '#cc00cc');
    svg.append("circle").attr("cx",20).attr("cy",150).attr("r", 6).style("fill", '#00cc00');
    svg.append("circle").attr("cx",20).attr("cy",180).attr("r", 6).style("fill", '#ffff00');
    svg.append("circle").attr("cx",20).attr("cy",210).attr("r", 6).style("fill", '#66ffff');
    svg.append("circle").attr("cx",20).attr("cy",240).attr("r", 6).style("fill", '#ff99ff');
    svg.append("circle").attr("cx",20).attr("cy",270).attr("r", 6).style("fill", '#e6e6e6');
    svg.append("text").attr("x", 30).attr("y", 35).text("Rock/Metal").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 65).text("Latina").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 95).text("Pop/Hip-Hop").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 125).text("Dance/Electronic").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 155).text("Indie").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 185).text("Funk").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 215).text("Blues").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 245).text("Jazz").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 275).text("Other").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");

    var link = svg.selectAll(".link")
        .data(force.links())
        .enter().append("line")
        .attr("class", "link")
        .style("stroke", "white");

    var node = svg.selectAll(".node")
        .data(force.nodes())
        .enter().append("g")
        .attr("class", "node")
        .on("mouseover.tooltip", mouseover)
        .on("mouseover.fade", fade(0.1))
        .on("mouseout", mouseout)
        .on("mouseout.fade", fade(1))
        .on("click", show_info)
        .style("fill", get_color)
        .call(force.drag);

    node.append("circle")
        .attr("r", 5);



    function tick() {
        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
            });

        node
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
    }

    const linkedByIndex = {};
    links.forEach(d => {
        linkedByIndex[`${d.source.index},${d.target.index}`] = 1;
    });

    function isConnected(a, b) {
        return linkedByIndex[`${a.index},${b.index}`] || linkedByIndex[`${b.index},${a.index}`] || a.index === b.index;
    }


    function mouseover(d) {
        d3.select(this).select("circle").transition()
            .duration(100)
            .attr("r", 10);
        d3.select(this).style("show", "true");
    }


    function mouseout(d) {
        d3.select(this).select("circle").transition()
            .duration(100)
            .attr("r", 5);
        link.style('stroke', 'white');
    }

    function fade(opacity) {
        return d => {
            node.style('stroke-opacity', function (o) {
                const thisOpacity = isConnected(d, o) ? 1 : opacity;
                this.setAttribute('fill-opacity', thisOpacity);
                return thisOpacity;
            });

            link.style('stroke-opacity', o => (o.source === d || o.target === d ? 1 : opacity));
        };
    }

    function get_color(d) {
        var genres = Nodes[d.name].genres;
        let color= '#e6e6e6';
        for ( let i =0; i< genres.length ; i++){
            if (genres[i].toLowerCase().includes("rock")|| genres[i].toLowerCase().includes("metal")) return '#ff0000';
            if (genres[i].toLowerCase().includes("latina") || genres[i].toLowerCase().includes("reggaeton")) return '#ff9900';
            if (genres[i].toLowerCase().includes("pop") || genres[i].toLowerCase().includes("hip") || genres[i].toLowerCase().includes('R&B')) return '#0066ff';
            if (genres[i].toLowerCase().includes("dance") || genres[i].toLowerCase().includes("house") ||  genres[i].toLowerCase().includes("elettronica")) return '#cc00cc';
            if (genres[i].toLowerCase().includes("indie")) return '#00cc00';
            if (genres[i].toLowerCase().includes("funk")) return '#ffff00';
            if (genres[i].toLowerCase().includes("blues")) return '#66ffff';
            if (genres[i].toLowerCase().includes("jazz")) return '#ff99ff';
        }
        return color;
    }

    function show_info(d) {
        var img = Nodes[d.name].image;
        var name = Nodes[d.name].name
        var gen = ""
        var url = "open_on_spotify('https://open.spotify.com/artist/" + d.name + "');";
        Nodes[d.name].genres.forEach(element => gen += element + ", ");
        gen = gen.slice(0, -2);

        $("#image").attr("src",img);;
        $("#name").text(name);
        $("#genres").text(gen);
        $("#open").attr("onclick", url);

        artId = d.name;

        $.ajax({
            type: 'GET',
            data: {'id' : artId},
            url: '/get_last_album/',
            success: function (result) {
                $("#player").attr('src', result['url']);
            },
            error: function (jqXHR) {
                showError(jqXHR);
            }
        });

    }

    function first_info(id) {
        var img = Nodes[id].image;
        var name = Nodes[id].name
        var gen = ""
        var url = "https://open.spotify.com/artist/" + id;
        Nodes[id].genres.forEach(element => gen += element + ", ");
        gen = gen.slice(0, -2);

        $("#artistCard").html(
        `<img src= '`+ img +` ' class='rounded mx-auto d-block' alt='`+id+`' width='45%' id='image' style='margin-top: 3%;'>
                 <h5 style='color: #1DB954; margin-top: 3%;'>Nome:&nbsp;</h5>
                 <h5 style='color: lightgrey' id='name'>`+name+`</h5>
                 <h5 style='color: #1DB954;'>Generi:&nbsp;</h5>
                 <h5 style='color: lightgrey' id='name'>`+gen+`</h5>
                 <button style="margin: 1%;" class="btn open" id='open' onclick="open_on_spotify('` + url +`')"><i class="fab fa-spotify"></i> Apri su Spotify</button>`);


        $.ajax({
            type: 'GET',
            data: {'id' : id},
            url: '/get_last_album/',
            success: function (result) {
                $("#player").attr('src', result['url']);
            },
            error: function (jqXHR) {
                showError(jqXHR);
            }
        });

    }
}

function open_on_spotify(url) {
    window.open(url,"_blank");
}