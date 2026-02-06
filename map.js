var lng = 0;
var lat = 0;
let map;
 
var initMap = function () {
    // get current location
    if (!navigator.geolocation) { // pedir permiso para acceder a la ubicacion actual
        alert("La Geolocalizacion no es compatible con este navegador...");
        return;
    }
 
    // lat, lng
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            //show map
            showMap(lat, lng);
        }
    );
}
 
//show map
function showMap(lat, lng) {
    // coordenadas
    const current_location = { lat: lat, lng: lng };
    // show map
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: current_location
    })
    //show marker
    new google.maps.Marker({
        position: current_location,
        map: map,
        title: "My Current Location",
        icon: {
            url: "laptop.png",
            scaledSize: new google.maps.Size(40, 40)
        }
    });
 
    //click on map
    map.addListener("click", (event) => {
        //place marker
        placeMarker(event.latLng);
    });
}

//*********************************************************************************************** */
//PRACTICA INSERTAR UNA LOCATION A PARTIR DE UN MARKER
const form = document.getElementById('locationForm');

form.addEventListener('submit', function(event) {
    event.preventDefault(); 
    const formData = new FormData(form);

    myAction(formData);
 
});

const myAction = async (formData) => {
    const data = Object.fromEntries(formData);
    const response = await fetch('http://localhost:5000/locations', {
      method: 'POST', 
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json', 
      },
      body: JSON.stringify(data),
    })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
    })
    .catch((error) => console.log("error to insert location" + error));
  };


//*********************************************************************************************** */
 
//draw marker
let placeMarker = function (location) {
    //show location
    console.log(location.lat());
    //console.log(location.Marker.coordinates.latitude);
    //lng = location.Marker.coords.lng;
    //lat = location.Marker.coords.lat;

    let txtLat = document.querySelector("#txtLat");
    txtLat.value = location.lat();
    let txtLng = document.querySelector("#txtLng");
    txtLng.value = location.lng();
 
    //create new marker
    new google.maps.Marker({
        position: location,
        map: map,
        title: location.toString()
    })
}
 