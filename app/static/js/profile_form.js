$(document).ready(function () {

    // Profile forms validation
    let email;
    let check;
    //clear modal when closed
    $(".modal-close[data-action=reset]").click(function () {
        location.reload();
    });

    // Checkboxes profile page complete profile form
    $("#form-edit-preferences input[type=checkbox]").each(function () {
        if ($(this).attr("value") == "true") {
            $(this).prop("checked", true);
        } else {
            $(this).val(false);
            $(this).prop("checked", false);
        }
    });

    // Check boxes edit preferences form
    // https://stackoverflow.com/questions/3442322/jquery-checkbox-event-handling
    $('#form-edit-preferences input[type=checkbox]').change(function () {
        if ($(this).val() === "false") {
            $(this).prop("checked", true);
            $(this).val(true);
        } else {
            $(this).prop("checked", false);
            $(this).val(false);
        }
    });

    // Check current password - edit profile/edit password
    /* Call python check password on user input
       https://www.bogotobogo.com/python/Flask/Python_Flask_with_AJAX_JQuery.php
       https://healeycodes.com/javascript/python/beginners/webdev/2019/04/11/talking-between-languages.html
    */
    $('#current-pwd').change(function () {
        email = $("#user_email").text().replace(" ", "");
        check = $("#current-pwd").val();
        $.ajax({
            url: `/check_password/${email}/${check}`,
            data: email,
            type: 'POST',
            success: function (response) {
                if (response === "no match") {
                    $("#message-error").html("Current password is incorrect").removeClass("hide");
                    $("p[data-error=current-pwd]").removeClass("hide");
                } else if (response === "match") {
                    $("#message-error").html("").addClass('hide');
                    $("p[data-error=current-pwd]").addClass("hide");
                }
            }
        });
    });

    // Make sure email is unique when changing email
    $('input[data-verify=new-email').change(function () {
        email = $(this).val();
        $.ajax({
            url: "/check_email_exists",
            data: {
                "email": email
            },
            type: 'POST',
            success: function (response) {
                if (response === "match") {
                    // match --> display error
                    $("p[data-error=email]").html("Email already exists").removeClass("hide");
                } else if (response === "no match") {
                    // no match --> hide error
                    $("p[data-error=email]").addClass("hide");
                }
            }
        });
    });


    // Edit Email & passwords validation 
    $('[data-check=check]').change(function () {
        let check_val = $("#" + $(this).attr('data-target')).val();
        // #https://stackoverflow.com/questions/18128882/set-input-as-invalid
        if ($(this).val() != check_val) {
            this.setCustomValidity("invalid");
            $(`p[data-error=${this.id}]`).removeClass("hide");
        } else {
            // hide field if valid
            $(`p[data-error=${this.id}]`).addClass("hide");
            this.setCustomValidity("");
        }
    });

});