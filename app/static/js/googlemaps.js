$(document).ready(function () {

    //Search address using google place library
    $('#event_location').focusin(function () {
        const input = document.getElementById("event_location");
        const option = {
            fields: ["formatted_address", "name", "geometry"]
        };
        const searchBox = new google.maps.places.SearchBox(input, option);
        input.setAttribute("data-place", "search");

        searchBox.addListener("places_changed", function () {

            const places = searchBox.getPlaces();
            const place = places["0"];
            // Add address to input field and set data-place to selected
            if (place.types[0] == "premise" || place.types[0] == "street_address") {
                input.value = place.formatted_address;
                input.setAttribute("data-place", "selected");
                $("p[data-error=event_location]").addClass("hide");

            } else {
                input.value = place.name + ", " + place.formatted_address;
                input.setAttribute("data-place", "selected");
                $("p[data-error=event_location]").addClass("hide");
            }
            // Remove error message
            if (input.getAttribute("data-place") === "search") {
                document.getElementById("location_error").classList.removeClass("hide");
            }
        });
    });

    //check if input field has been completed from places
    $('#event_location').focusout(function () {
        if ($(this).attr("data-place") === "search") {
            // display message
            $("[data-error=event_location]").removeClass("hide");
        }
        if ($(this).attr("data-place") === "selected") {
            // hide field if valid
            $("[data-error=event_location]").addClass("hide");
        }
    });

});