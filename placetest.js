var map;
var infowindow;
// creates new map centered at place1, displays it, and searches for types within radius of place1 (in this case, restaurants)
$(document).ready(function(){
    $("#FindPlaces").click(function(){
      if (document.getElementById('origin').value === "" || document.getElementById('radius').value === ""){
        alert("Please enter origin and search radius.");
      } else if (isNaN(document.getElementById('radius').value)){
        alert("Please enter a numerical radius.");
      } else {
        try {
          // clears list of places at right of map
          // gets addresses from input boxes and formats them for url
          $("#placeListOl").empty();
          var $originraw = $('#origin').val();
          var $rad = $('#radius').val()*1609.34;
          var $originurl = $originraw.replace(/ /g, "+");
          var type = $("#locbtn select option:selected").val();
          var zoom = 0;

          // determines zoom level for map
          if ($('#radius').val() <= 2.1){
            zoom = 14;
          } else if ($('#radius').val() <= 3.8){
            zoom = 13;
          } else if ($('#radius').val() <= 6.8){
            zoom = 12;
          } else if ($('#radius').val() <= 15){
            zoom = 11;
          } else if ($('#radius').val() <= 40){
            zoom = 10;
          } else if ($('#radius').val() <= 80){
            zoom = 9;
          } else {
            zoom = 8;
          }

          // gets JSON data from url and stores in jtext
          $.getJSON('https://maps.googleapis.com/maps/api/geocode/json?address='+$originurl+'&key=AIzaSyA7OXa-HwyjlSJKa89x0yyXbxSn1EfTCEQ', function(jtext){
            // gets lat/long of origin and destination
            var orig = jtext.results[0].geometry.location

            // creates new map object
            map = new google.maps.Map(document.getElementById('mapInterest'), {
              center: orig,
              scrollwheel: true,
              zoom: zoom
            });

            infowindow = new google.maps.InfoWindow();

            var service = new google.maps.places.PlacesService(map);
            service.nearbySearch({
              location: orig,
              radius: $rad,
              types: [type]
            }, callback);

          });

          function callback(results, status) { 
            // if successful, place markers at found locations and add their names and addresses to element with id placeList
            if (status === google.maps.places.PlacesServiceStatus.OK) {
              for (var i = 0; i < results.length; i++) {
                createMarker(results[i]);
                $('#placeListOl').append('<li>'+results[i].name+', '+results[i].vicinity+'</li>');
              }
            }
          }
          
          // helper function to create marker
          function createMarker(place) {
            var placeLoc = place.geometry.location;
            var marker = new google.maps.Marker({
              map: map,
              position: placeLoc
            });

            google.maps.event.addListener(marker, 'click', function() {
              infowindow.setContent(place.name);
              infowindow.open(map, this);
            });
          }
        } catch(err){
          alert("An error occurred.");
        }
      }
    });
});

// helper function to create markers
function createMarker(place) {
    var marker = new google.maps.Marker({
        map: map,
        position: place
    });

    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(place.name);
        infowindow.open(map, this);
    });
}

// helper function to create map
function initMap() {
    var map = new google.maps.Map(document.getElementById('mapInterest'), {
      center: {lat: 40.324716, lng:-74.128610},
      zoom: 6
    });
    var infoWindow = new google.maps.InfoWindow({map: map});

    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        infoWindow.setPosition(pos);
        infoWindow.setContent('Location found.');
        map.setCenter(pos);
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
}

// error handling helper function
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'You are here!' :
                          'You are here!');
}