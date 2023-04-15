$(document).ready(function () {
    // Toggle password visibility
    //https://www.w3schools.com/howto/howto_js_toggle_password.asp
    $(".password-visible").click(function () {
        let id = $(this).attr("data-target");
        if ($(`#${id}`).attr("type") == "password") {
            $(`#${id}`).attr("type", "text");
            $(this).removeClass("fa-eye").addClass("fa-eye-slash");
        } else if ($(`#${id}`).attr("type") == "text") {
            $(`#${id}`).attr("type", "password");
            $(this).removeClass("fa-eye-slash").addClass("fa-eye");
        }
    });
});