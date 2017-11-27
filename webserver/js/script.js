

// Runs on page load. Obtains the colors 
var settings = {
  "async": true,
  "crossDomain": true,
  "url": "/getcolors",
  "method": "GET",
  "headers": {}
}
var colors = {}
$.ajax(settings).done(function (response) {
  colors = JSON.parse(response);
});

Highcharts.setOptions({
  global : {
      useUTC : false
  }
});

// Javascript version of our arrival detection heuristic
function heuristic(before, after) {
  return (before < 80) && (after - before > 40);
}

function changeFunc() {
  removeChart();
  var selectBox = document.getElementById("stopSelect");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  var url = "/getdata/" + selectedValue;
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
    return Math.floor(sec/60) + "m " + parseInt(sec%60) + "s";
  }
  response = JSON.parse(response);
  for (var i = 0, len = response.length; i < len; i++) {
    var route = response[i][2];
    var tag = response[i][1];
    var oldPrediction = secToMin(response[i][11]);
    var myPrediction = secToMin(response[i][19]);
    var color = colors[route]
    var toAppend = "<tr style=\"cursor:pointer;\" onclick=\"drawChart(\'" + route + "\', \'" + tag + "\')\">" + 
    "<td><a style=\"color:#F0F0FF;background-color:" + color + "\" class=\"ui label\">" + route + "</a> <a class='ui label'>(" + tag + ")</a></td><td>" + myPrediction + "</td><td class=\"right aligned\">" + oldPrediction + "</td></tr>";
    console.log(toAppend);
    $("#timeTable").find("tbody").append(toAppend);
  }
});
}

// Triggers when user clicks on the marker icon. Attempts to acquire user's
// latitude and longitude, and then makes a request to the backend to
// find the nearest stop. On success, sets the stop in the dropdown.

function withCoords(latitude, longitude) {
  var url = "/gps?lat=" + latitude + "&lon=" + longitude;    
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

function googleBackup() {
  var settings = {
    "async": true,
    "crossDomain": true,
    "url": "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBrmRpbN22V75_aEjLxdFKkgxaods-_I5I",
    "method": "POST",
    "headers": {}
  }
  
  $.ajax(settings).done(function (response) {

    withCoords(response.location.lat, response.location.lng);
  });
}

function geoFindMe() {
  var output = document.getElementById("out");

  if (!navigator.geolocation){
    console.log("Geolocation is not supported by your browser");
    googleBackup();
    return;
  }

  function success(position) {
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;
    withCoords(latitude, longitude);
  }
    



  function error() {
    console.log("Unable to retrieve your location");
    googleBackup();
  }

  navigator.geolocation.getCurrentPosition(success, error);
}

function removeChart() {
  $('#container').remove();
  $('#outer').prepend($('<h2 id=\'container\'>Click on a route to view prediction history.</h2>'));
}

function drawChart(route, stop) {
  $('#container').remove();
$('#outer').prepend($('<div id="container"></div>'));

var url = "/gettop/" + stop + "/" + route
console.log(url);

var settings = {
  "async": true,
  "crossDomain": true,
  "url": url,
  "method": "GET",
  "headers": {}
}

$.ajax(settings).done(function (response) {
  response = JSON.parse(response).reverse();
  var nextbus = [];
  var nextbuzz = [];
  var actual = []
  var previous = 99999999;
  var previousTime = null;
  var startTime = null;
  for (var i = 0, len = response.length; i < len; i++) {
    var timestamp = parseInt(response[i][0])*1000;    
    if (startTime == null) {
      startTime = timestamp;
    }
    if (previousTime == null) {
      previousTime = timestamp;
    }
    var nb_pred = parseInt(response[i][11]);
    if (heuristic(previous, nb_pred)) {
      actual.push([startTime, (timestamp - startTime)/1000]);
      actual.push([previousTime, 0]);
      startTime = timestamp;
    }
    previous = nb_pred;
    previousTime = timestamp;
    nextbus.push([timestamp, nb_pred]);
    nextbuzz.push([timestamp, parseInt(response[i][19])]);
  }

Highcharts.chart('container', {
      chart: {
        type: 'line'
      },

      title: {
          text: 'Prediction performance over time (' + route + ', ' + stop + ')'
      },
  
      subtitle: {
          text: 'NextBuzz vs NextBus predictions'
      },
  
      yAxis: {
          title: {
              text: 'Seconds To Arrival'
          }
      },
      xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: {
          millisecond: '%H:%M:%S.%L',
          second: '%H:%M:%S',
          minute: '%I:%M %P',
          hour: '%H:%M %P',
          day: '%e. %b',
          week: '%e. %b',
          month: '%b \'%y',
          year: '%Y'
        },
        title: {
            text: 'Date'
        }
    },
    tooltip: {
      formatter: function() {
          return  '<b>' + this.series.name +'</b><br/><b>' + this.y + ' sec</b><br/>' +
              Highcharts.dateFormat('%I:%M:%S %P, %a, %b %e, %Y', new Date(this.x));      
    }
  },
      legend: {
          layout: 'vertical',
          align: 'right',
          verticalAlign: 'middle'
      },
  
      plotOptions: {
          series: {
              label: {
                  connectorAllowed: false
              }
          }
      },
  
      series: [{
        name: 'NextBus (Old prediction)',
        color: '#777777',
        data: nextbus
    }, {
        name: 'NextBuzz (Improved prediction)',
        color: colors[route],
        data: nextbuzz
    },{
      name: 'Actual Seconds to Arrival',
      color: '#999999',
      dashStyle: 'ShortDash',
      data: actual
    }],
  
      responsive: {
          rules: [{
              condition: {
                  maxWidth: 500
              },
              chartOptions: {
                  legend: {
                      layout: 'horizontal',
                      align: 'center',
                      verticalAlign: 'bottom'
                  }
              }
          }]
      }
  
  });
});
}