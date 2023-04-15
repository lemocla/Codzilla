$(document).ready(function () {

    // Groups and events action 
    // Set location hash prior event and group action 
    $(".btn-tab").click(function () {
        window.location.hash = $(this).children("a").attr("href");
    });

    // Function calling python function 
    function actionGroupEvent(user_id, target_id, action) {
        // Ajax requestion to python function attend
        $.ajax({
            url: `${action}`,
            type: "POST",
            data: {
                "user_id": `${user_id}`,
                "target_id": `${target_id}`
            },
            dataType: "json",
            success: function (response) {
                //https://stackoverflow.com/questions/18490026/refresh-reload-the-content-in-div-using-jquery-ajax
                if (response == "success") {
                    location.reload();
                }
            }
        });
    }

    // Attend 
    $(".btn.btn-attend").click(function () {
        if ($(this).attr("data-status") == "active") {
            let user_id = $(this).attr("data-user");
            let event_id = $(this).attr("data-event");
            actionGroupEvent(user_id, event_id, "/attend");
        }
    });

    // Attending
    $(".btn.btn-attending").click(function () {
        let event_id = $(this).attr("data-event");
        $(`.btn.btn-unattend[data-event=${event_id}]`).toggleClass("hide");
    });

    // Unattend
    $(".btn.btn-unattend").click(function () {
        let event_id = $(this).attr("data-event");
        let user_id = $(this).attr("data-user");
        actionGroupEvent(user_id, event_id, "/unattend");
    });

    // Toggle interest bookmarked
    $(".btn-interest").click(function () {
        if ($(this).attr("data-status") == "active") {
            let event_id = $(this).attr("data-event");
            let user_id = $(this).attr("data-user");
            actionGroupEvent(user_id, event_id, "/bookmark_interest");
        }
    });

    // Remove interest
    $(".btn-interested").click(function () {
        let event_id = $(this).attr("data-event");
        let user_id = $(this).attr("data-user");
        actionGroupEvent(user_id, event_id, "/remove_interest");
    });

    //Follow group
    $(".btn-follow").click(function () {
        if ($(this).attr("data-status") == "active") {
            let group_id = $(this).attr("data-group");
            let user_id = $(this).attr("data-user");
            actionGroupEvent(user_id, group_id, "/follow");
        }
    });

    // Display unfollow button
    $(".btn.btn-following").click(function () {
        let group_id = $(this).attr("data-group");
        $(`.btn.btn-unfollow[data-group=${group_id}]`).toggleClass("hide");
    });

    // Unfollow group
    $(".btn-unfollow").click(function () {
        let group_id = $(this).attr("data-group");
        let user_id = $(this).attr("data-user");
        actionGroupEvent(user_id, group_id, "/unfollow");
    });
});