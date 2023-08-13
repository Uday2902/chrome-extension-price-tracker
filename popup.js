document.addEventListener('DOMContentLoaded', function() {
  var graph = document.getElementById('graph');
  var detailsForm = document.getElementById('detailsForm');
  detailsForm.addEventListener('submit', function(event) {
    event.preventDefault();
    var email = detailsForm.email.value;
    var price = detailsForm.price.value;
    console.log('Email:', email);
    console.log('Price:', price);
  });

  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var product_url = tabs[0].url;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'http://localhost:5000/generate_graph?product_url=' + encodeURIComponent(product_url), true);
    xhr.responseType = 'blob';
    xhr.onload = function(e) {
      if (this.status == 200) {
        var blob = this.response;
        var objectURL = URL.createObjectURL(blob);
        graph.src = objectURL;
      }
    };
    xhr.send();
  });
});
