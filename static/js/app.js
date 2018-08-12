var defaultURL1 = "/samples/BB_940";
var defaultURL2 = "/metadata/BB_940";
var otuURL = "/otu";
function init() {
    Plotly.d3.json(defaultURL1, function(error, response) {
        if (error) {
            return console.warn(error);
        }
        var data = response[0];
        var labels = [];
        var values = [];
        for (var i = 0; i < 10; i++) { 
            labels.push(data["otu_ids"][i]);
            values.push(data["sample_values"][i]);
        }
        var data = [{
            values: values,
            labels: labels,
            type: "pie"
        }];
        var layout = {
            title: "Sample values by OTU ID",
            height: 500,
            width: 500
        };
        Plotly.newPlot("piechart", data, layout);
    })

    Plotly.d3.json(defaultURL1, function(error, response) {
        if (error) {
            return console.warn(error);
        };    
        var datavalues = response[0];
        var x = []
        var y = []
        var size = []
        for (var i = 0; i < datavalues["otu_ids"].length; i++) { 
            x.push(datavalues["otu_ids"][i]);
            y.push(datavalues["sample_values"][i]);
            size.push(datavalues["sample_values"][i]*.5);
        };

        Plotly.d3.json(otuURL, function(error, response) {
            if (error) {
                return console.warn(error);
            };
            var text = response;
            var trace1 = {
                x: x,
                y: y,
                text: text,
                mode: 'markers',
                marker: {
                    color: y,
                    size: size
                }
            };
            var data = [trace1];
            var layout = {
                title: 'Count of Bacterias',
                showlegend: false,
                height: 400,
                width: 1000
            };
            Plotly.newPlot("bubblechart", data, layout);
        });
    });
};

function updatePie(values, labels) {  
    Plotly.restyle("piechart", "values", [values]);
    Plotly.restyle("piechart", "size", [labels]);
  }
function updateBubble(x, y, size) {
    Plotly.restyle("bubblechart", "x", [x]);
    Plotly.restyle("bubblechart", "y", [y]);
    Plotly.restyle("bubblechart", "marker.size", [size]);
    Plotly.restyle("bubblechart", "marker.color", [x] );
}

var samplesURL = "/samples/";
var metadataURL = "/metadata/";

function optionChanged(dataset) {
    var url = samplesURL + dataset;
    Plotly.d3.json(url, function(error, response) {
        if (error) {
            return console.warn(error);
        }
        var data = response[0];
        var labels = [];
        var values = [];
        for (var i = 0; i < 10; i++) { 
            labels.push(data["otu_ids"][i]);
            values.push(data["sample_values"][i]);
        }
        updatePie(values, labels);
    });   
    Plotly.d3.json(url, function(error, response) {
        if (error) {
            return console.warn(error);
        };    
        var datavalues = response[0];
        var x = []
        var y = []
        var size = []
        for (var i = 0; i < datavalues["otu_ids"].length; i++) { 
            x.push(datavalues["otu_ids"][i]);
            y.push(datavalues["sample_values"][i]);
            size.push(datavalues["sample_values"][i]*0.5);
        };
        console.log(x);
        console.log(y);
        console.log(size);
        updateBubble(x, y, size);
    });

    var metaURL = metadataURL + dataset;
    var metadata = document.getElementById("metadata");
    metadata.innerHTML = "";
    Plotly.d3.json(metaURL, function(error, response) {
        if (error) {
            return console.warn(error);
        }
        var meta = response;
        metaKeys = Object.keys(meta);
        for (var i = 0; i < metaKeys.length; i++) { 
            var mdata = metaKeys[i] + ":" + meta[metaKeys[i]];
            var p = document.createElement("P");
            p.innerText = mdata;
            metadata.appendChild(p);
        }
    })

}

document.addEventListener('DOMContentLoaded', function() {
    var selDataset = document.getElementById("selDataset");
    var namesURL = "/names";
    Plotly.d3.json(namesURL, function(error, response) {
        if (error) {
            return console.warn(error);
        }

        var names = response
        for (var i = 0; i < names.length; i++) { 
            var option = document.createElement("option");
            option.innerText = names[i];
            selDataset.appendChild(option);
        }

    });

    var metadata = document.getElementById("metadata");
    Plotly.d3.json(defaultURL2, function(error, response) {
        if (error) {
            return console.warn(error);
        }
        var meta = response;
        metaKeys = Object.keys(meta);
        for (var i = 0; i < metaKeys.length; i++) { 
            var mdata = metaKeys[i] + ":" + meta[metaKeys[i]];
            var p = document.createElement("P");
            p.innerText = mdata;
            metadata.appendChild(p);
        }
    })

    init();
});// connect to the api/names url and create our sample dropdown list
