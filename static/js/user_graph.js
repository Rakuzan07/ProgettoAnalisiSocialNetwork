function render_graph() {
    $("#graphDiv").html(`<div class='spinner-grow'  style='color: #1DB954; margin-top: 40%;' role='status'>  <span class='sr-only'>Retrieving data...</span></div>
                                 <p>Sto caricando...</p>`);
    // let diameter = 3;
    $.ajax({
            type: 'GET',
            url: '/get_user_graph/',
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
        .style("fill", '#00ff00')
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



    function show_info(d) {
        var img = Nodes[d.name].image;
        var name = Nodes[d.name].name

        if( img==null){
            img="https://managedserver.it/wp-content/uploads/2017/08/sistemista-linux.png"
        }

        $("#image").attr("src",img);
        $("#name").text(name);

    }

    function first_info(id) {
        var img = Nodes[id].image;
        var name = Nodes[id].name;

        if( img==null){
            img="https://managedserver.it/wp-content/uploads/2017/08/sistemista-linux.png"
        }

        $("#artistCard").html(
        `<img src= '`+ img +` ' class='rounded mx-auto d-block' alt='`+id+`' width='45%' id='image' style='margin-top: 3%;'>
                 <h5 style='color: #1DB954; margin-top: 3%;'>Nome:&nbsp;</h5>
                 <h5 style='color: lightgrey' id='name'>`+name+`</h5>`);
    }
   }

function open_on_spotify(url) {
    window.open(url,"_blank");
}
