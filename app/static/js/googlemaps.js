$(document).ready(function () {

    //Search address using google place library
    $('#event_location').focusin(function () {
        const input = document.getElementById("event_location");
        const option = {
            fields: ["formatted_address", "name", "geometry"]
        }
        const searchBox = new google.maps.places.SearchBox(input, option);
        input.setAttribute("data-place", "search");

        searchBox.addListener("places_changed", function () {

            const places = searchBox.getPlaces();
            const place = places["0"];
            //
            input.setAttribute("data-place", "selected");
            if (place.types[0] == "premise" || place.types[0] == "street_address") {
                input.value = place.formatted_address;
                input.setAttribute("data-place", "selected");
                $(`p[data-error=event_location]`).addClass("hide").html("");

            } else {
                input.value = place.name + ", " + place.formatted_address;
                input.setAttribute("data-place", "selected");
                $(`p[data-error=event_location]`).addClass("hide").html("");
            }
            //
        })
    });

    //controls pac-target-input
    $('#event_location').change(function () {
        console.log("focus out happening")
        if ($(this).attr("data-place") == "search") {
            let errorMsg = "Please select a valid address";
            // display message
            $(`p[data-error=event_location]`).html(errorMsg).removeClass("hide");
        }
        if ($(this).attr("data-place") == "selected") {
            // hide field if valid
            $(`p[data-error=event_location]`).addClass("hide").html("");
        }
    });

});