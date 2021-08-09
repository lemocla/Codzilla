$(document).ready(function () {

    //Search address using google place library
    $('#event_location').focusin(function () {
        const input = document.getElementById("event_location");
        const option = {
            fields: ["formatted_address", "name", "geometry"]
        }
        const searchBox = new google.maps.places.SearchBox(input, option);

        searchBox.addListener("places_changed", function () {

            const places = searchBox.getPlaces();
            const place = places["0"];
            //
            if (place.types[0] == "premise" || place.types[0] == "street_address")
                input.value = place.formatted_address;
            else {
                input.value = place.name + ", " + place.formatted_address;
            }
        })
    });

});