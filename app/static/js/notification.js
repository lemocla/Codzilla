$(document).ready(function () {

    // Variables

    let val;
    let newval;

    // Notifications
    $(".collapsible-header").click(function () {
        // Ajax requestion to python function to add to read_by
        if ($(this).attr("data-status") === "not read") {

            // Data to send 
            let user_id = $(this).attr("data-user");
            let notification_id = $(this).attr("data-notification");

            // Hide new basge
            $(this).attr("data-status", "read");
            $('span.badge').addClass("hide");

            $.ajax({
                url: "/mark_as_read",
                type: 'POST',
                data: {
                    "user_id": `${user_id}`,
                    "target_id": `${notification_id}`
                },
                success: function (response) {
                    // https://stackoverflow.com/questions/18490026/refresh-reload-the-content-in-div-using-jquery-ajax
                    // Update number of notification 
                    if (response == "success") {
                        val = $(".new-notification").text();
                        newval = parseInt(val) - 1;
                        if (newval > 0) {
                            $(".new-notification").text(newval);
                        } else {
                            $(".new-notification").addClass('hide');
                        }
                    }
                }
            });
        }
    });

});