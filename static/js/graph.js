function render_graph(name) {
    $("#graphDiv").html(`<div class='spinner-grow'  style='color: #1DB954; margin-top: 40%;' role='status'>  <span class='sr-only'>Retrieving data...</span></div>
                                 <p>Sto caricando...</p>`);
    let diameter = 3;
    if(name===null){
        name = $("#art").val();
        diameter = $("#type").val();
    }
    $.ajax({
            type: 'GET',
            url: '/get_graph/',
            data: {
                "name": name,
                "diameter" : diameter,
            },
            dataType: 'json',
            success: function (result) {

                $("#graphDiv").html("");
                $("#sidebar").css("background-color", "#29323c").css("border", "1px solid black").css("border-radius", "10px")
                    .css("padding-top", "1%").css("height", "100vh");
                if(!$("#artistCard").length){
                    $("#sidebar").append('<div class="card" id="artistCard"></div>')
                        .append('<iframe id="player" src="https://open.spotify.com/embed/playlist/37i9dQZEVXbMDoHDwVN2tF" style="margin-top: 5%;" width="280" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>');
                    $("#artistCard").css("height", "60%");
                }
                drawArtistsGraph(result["links"], result["nodes"], name, result["id"]);
                window.scrollTo(0, document.body.scrollHeight);
            },
            error: function (jqXHR) {
                showError(jqXHR);
            }
        });

}

function drawArtistsGraph(links, Nodes, name, id){
    first_info(id);
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
        .linkDistance(20)
        .charge(-350)
        .on("tick", tick)
        .start();

    var svg = d3.select("#graphDiv").append("svg")
        .attr("id", "artistsGraph")
        .attr("width", width)
        .attr("height", height);

    svg.append("text").attr("x", 10).attr("y", 10).text("Distances:")
        .style("font-size", "15px").style("fill", "white").attr("alignment-baseline","middle");
    svg.append("circle").attr("cx",20).attr("cy",30).attr("r", 6).style("fill", "#FF0000");
    svg.append("circle").attr("cx",20).attr("cy",60).attr("r", 6).style("fill", '#7c9ecc');
    svg.append("circle").attr("cx",20).attr("cy",90).attr("r", 6).style("fill", '#2271b3');
    svg.append("circle").attr("cx",20).attr("cy",120).attr("r", 6).style("fill", '#214b74');
    svg.append("circle").attr("cx",20).attr("cy",150).attr("r", 6).style("fill", '#18273a');
    svg.append("circle").attr("cx",20).attr("cy",180).attr("r", 6).style("fill", '#111720');
    svg.append("text").attr("x", 30).attr("y", 30).text("0").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 60).text("1").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 90).text("2").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 120).text("3").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 150).text("4").style("font-size", "15px")
        .style("fill", "white").attr("alignment-baseline","middle");
    svg.append("text").attr("x", 30).attr("y", 180).text("5").style("font-size", "15px")
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
        var path = Nodes[d.name].path;
        var color = ['#FF0000', '#7c9ecc', '#2271b3', '#214b74', '#18273a' , '#111720'];
        return color[path]
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