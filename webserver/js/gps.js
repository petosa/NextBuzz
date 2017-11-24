function geoFindMe() {
  var output = document.getElementById("out");

  if (!navigator.geolocation){
    console.log("Geolocation is not supported by your browser");
    return;
  }

  function success(position) {
    var latitude  = position.coords.latitude;
    var longitude = position.coords.longitude;
    console.log(latitude);
    console.log(longitude);
  }

  function error() {
    console.log("Unable to retrieve your location");
  }

  navigator.geolocation.getCurrentPosition(success, error);
}
