function buildDropdown() {
  const nameUrl = "/names";
  Plotly.d3.json(nameUrl, function (error, response) {

      console.log(response);
      const selectedElement = document.getElementById("selDataset");
      for (let i = 0; i < response.length; i++) {
          const option = document.createElement("option");
          option.text = response[i];
          option.value = response[i];
          selectedElement.appendChild(option);
      }
  });
}


function optionChanged(sample) {
  console.log(sample);
  buildPieChart(sample);
}


buildDropdown();
