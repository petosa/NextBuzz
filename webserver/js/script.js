
function changeFunc() {
  var selectBox = document.getElementById("stopSelect");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  var url = "http://localhost:5000/getdata/" + selectedValue;
  $("#timeTable").find("tr:gt(0)").remove();
console.log(url);
var settings = {
  "async": true,
  "crossDomain": true,
  "url": url,
  "method": "GET",
  "headers": {}
}


$.ajax(settings).done(function (response) {

  function secToMin(sec) {
    return Math.floor(sec/60) + "m " + sec%60 + "s";
  }

  response = JSON.parse(response);
  for (var i = 0, len = response.length; i < len; i++) {
    var route = response[i][2];
    var oldPrediction = secToMin(response[i][11]);
    $("#timeTable").find("tbody").append("<tr><td>" + route + "</td><td>Approved</td><td class=\"right aligned\">" + oldPrediction + "</td></tr>");
  }
});
}

function geoFindMe() {
  var output = document.getElementById("out");

  if (!navigator.geolocation){
    console.log("Geolocation is not supported by your browser");
    return;
  }

  function success(position) {
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;
    var url = "http://localhost:5000/gps?lat=" + latitude + "&lon=" + longitude;
    
	console.log(url);
	var settings = {
	  "async": true,
	  "crossDomain": true,
	  "url": url,
	  "method": "GET",
	  "headers": {}
	}

	$.ajax(settings).done(function (response) {
	  $('#stopSelect').dropdown('set selected', response);    
	});

  }

  function error() {
    console.log("Unable to retrieve your location");
  }

  navigator.geolocation.getCurrentPosition(success, error);
}


