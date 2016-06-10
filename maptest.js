$(document).ready(function(){ // when document is ready
    $("#btn1").click(function(){ // when button 1 is clicked
    	if (document.getElementById('origin1').value === "" || document.getElementById('dest1').value === "") { // if one of boxes is blank
			//nothing inputted
    		alert("Please enter an origin and destination.");
		} else {
    		// gets addresses from input boxes and formats them for url
			var origin = new Object();
			var dest = new Object();
        	var $originraw = $('#origin1').val();
			var $destraw = $('#dest1').val();
			var $originurl = $originraw.replace(/ /g, "+");
			var $desturl = $destraw.replace(/ /g, "+");

			// gets JSON data from url and stores in jtext
			$.getJSON('https://maps.googleapis.com/maps/api/directions/json?origin='+$originurl+'&destination='+$desturl+'&key=AIzaSyA7OXa-HwyjlSJKa89x0yyXbxSn1EfTCEQ', function(jtext){
				// gets lat/long of origin and destination
				$('#distance').empty()
				$('#duration').empty()

				try {
					// pulls data from retrieved JSON
					origin = jtext.routes[0].legs[0].start_location;
					dest = jtext.routes[0].legs[0].end_location;
					distance = jtext.routes[0].legs[0].distance.text;
					duration = jtext.routes[0].legs[0].duration.text;
					steps = jtext.routes[0].legs[0].steps;

					// empties direction list before adding new ones so they don't pile up when you repeatedly create click route
					$('#directionList').empty();

					for (var step of steps){
						$('#directionList').append("<li>" + step.html_instructions + "</li>");
					}

					// creates new map object
					var map = new google.maps.Map(document.getElementById('mapRest'), {
						center: origin,
						scrollwheel: true,
						zoom: 7
					});

					// renders map
					var directionsDisplay = new google.maps.DirectionsRenderer({
						map: map
					});

					// Set destination, origin and travel mode.
					var request = {
						destination: dest,
						origin: origin,
						travelMode: google.maps.TravelMode.DRIVING
					};

					// Pass the directions request to the directions service.
					var directionsService = new google.maps.DirectionsService();
					directionsService.route(request, function(response, status) {
						if (status == google.maps.DirectionsStatus.OK) {
						// Display the route on the map.
						directionsDisplay.setDirections(response);
						}
					});

					// generates rest stop locations
					var locs = calcStops(steps, 0, []);

					// places a marker at each location
					for (var loc of locs){
						var marker = new google.maps.Marker({
	    					position: loc,
	    					title:""
						});
						marker.setMap(map);
					}
				} catch(err){
					alert("Directions could not be found between these two locations.");
				}
			});
		}
	});
	$('#btn2').click(function () {
		doc.fromHTML($('#direction').html(), 15, 15, {
			'width': 170,
			'elementHandlers': specialElementHandlers
		});
		doc.save('Route_Directions.pdf');
	});
});

//recursive, returns list of rest stop locations (by long/lat)
function calcStops(steps, initBuf, locs){
	var maxtime = 14400;							// recommended driving time before break is 4 hrs = 14400 secs (for coding convenience)
	var accumulated = initBuf;						// normally 0 but if there's carry-over time from the previous stop (see below) initBuf is not 0
	var i = 0;
	for (var step of steps){
		if (accumulated + step.duration.value <= maxtime){ // if still below limit after this step
			accumulated += step.duration.value;
		} else {
			if (step.duration.value <= 600){				// this if-else prevents cases where, say, first step is 10 minutes but second step is 7 hours... 
				locs.push(step.end_location);							// this way it won't tell you to take a break after only 10 minutes
				return calcStops(steps.slice(i+1, steps.length), 0, locs);			// recursion: steps are only the ones after the last step calculated in the current calculation
															// ie if steps 1, 2, 3, 4 in last iteration of calcStops will start with step 5 in the next
			} else {
				var remaining = maxtime - accumulated;			// time you can drive this step before you hit the limit
				var cut = step.duration.value - remaining;		// how much time left on this step after you rest
				var portion = remaining / step.duration.value;	// 0 < portion < 1, how far to go on the step
				var final_long = (step.end_location.lng - step.start_location.lng) * portion + step.start_location.lng;	// final longitude before stop
				var final_lat = (step.end_location.lat - step.start_location.lat) * portion + step.start_location.lat; 	// final latitude before stop
				locs.push({"lat": final_lat, "lng": final_long})
				var added_long = final_long;					// these two vars only used if condition in while loop below is true
				var added_lat = final_lat;
				while (cut > 14400){
					added_long += (step.end_location.lng - step.start_location.lng) * 14400/step.duration.value; //that last term takes the place of portion in lines 81/82
					added_lat += (step.end_location.lat - step.start_location.lat) * 14400/step.duration.value;
					locs.push({"lat": added_lat, "lng": added_long})
					cut -= 14400
				}
				return calcStops(steps.slice(i+1, steps.length), cut, locs); // recursion
			}
		}
		i++; // increments stepper iterating through steps of directions
	}
	return locs; // final return
}

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
    var map = new google.maps.Map(document.getElementById('mapRest'), {
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

//Checks if the input is numerical (valid)
function idiotProof() {
	if (document.getElementById('origin1').value === "" || document.getElementById('dest1').value === "") {
		//nothing inputted
    	alert("You did not enter anything.");
	} 
}

// loads modal when window loads
$(window).load(function(){
    $('#myModal').modal('show');
});

// prepares PDF
var doc = new jsPDF();
var specialElementHandlers = {
	'#editor': function (element, renderer) {
		return true;
	}
};