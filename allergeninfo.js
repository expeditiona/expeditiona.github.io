// Food Allergen Finder
function allergenfinder() {
	//Reset Page
	document.getElementById('outputgood').innerHTML = ""
	document.getElementById('outputbad').innerHTML = ""

	//Restaurant selected
	var storename = document.getElementById("storepicker").value;

	//Connect to database depending on restaurant
	var myFirebaseRefAllergen = new Firebase("https://crackling-inferno-9505.firebaseio.com/foods/" + storename);

	//Determines which allergens are selected
	myFirebaseRefAllergen.on("child_added", function(snapshot, prevChildKey) {
		var newPost2 = snapshot.val();
		var allergencheckarray = [];
		for (i=0; i < 9; i++) {
			var x = document.getElementsByName("allergencheck")[i]
			if (x.checked == true) {
				allergencheckarray.push(x.value)
			}
			else {}
		}

		//Places all food allergens for specific food in array
		var allergenarray = [newPost2.allergen1, newPost2.allergen2, newPost2.allergen3, newPost2.allergen4, newPost2.allergen5];
		var check = true

		//Compares allergens for each food with allergens selected by user
		for (i=0; i < 5; i++) {
			for(y=0; y < allergencheckarray.length; y++) {
				//If no match found, then food is good to eat
				if (allergenarray[i] != allergencheckarray[y]) {	
				}
				else {
					var check = false
				}	
			}	
		}

		//Display good foods
		if (check == true) {
			console.log("Name: " + newPost2.name);
			document.getElementById('outputgood').innerHTML += (newPost2.name + "<br />")
		}

		//Display bad foods
		else {
			document.getElementById('outputbad').innerHTML += (newPost2.name + "<br />")
		}
	});

}
