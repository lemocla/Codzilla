$(document).ready(function () {
    // variables
    let groupName;
    let dataCheck;
    let existing;
    // Make sure group name is unique
    $("#group_name").change(function () {
        groupName = $("#group_name").val();
        dataCheck = $("#group_name").attr("data-check");
        if (dataCheck != null) {
            existing = dataCheck;
        } else {
            existing = "none";
        }
        $.ajax({
            url: "/check_name",
            data: {
                "group_name": groupName,
                "existing": existing
            },
            type: 'POST',
            success: function (response) {

                if (response == "match") {
                    $("p[data-error=group_name]").html("Group name already exists, please choose a different one.").removeClass("hide");
                } else if (response === "no match") {
                    $("p[data-error=group_name]").html("Please enter a valid last name between 1 and 32 characters.").addClass("hide");
                }
            }
        });
    });

})