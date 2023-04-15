$(document).ready(function () {

    // Variables
    let valid;
    let toValidate;
    let validated;
    // Add asterix to labels for required fields 
    $("[required]").each(function () {
        $("label[for=" + this.id + "]").append('<span class="required"> *</span>');
    });

    // Forms validation on submit

    // Display error message if input is invalid as per attributes 

    $("input").change(function () {
        //  https://stackoverflow.com/questions/14384593/jquery-how-to-know-when-input-have-a-invalid-selector 
        if ($(this).is(":invalid")) {
            // display message
            $(`p[data-error=${this.id}]`).removeClass("hide");
        } else if ($(this).is(":valid")) {
            // hide field if valid
            $(`p[data-error=${this.id}]`).addClass("hide");
        }
    });

    // Function to return if form is valid
    function validate(invalidId) {
        toValidate = $("p.error-text").length;
        validated = $("p.error-text.hide").length;
        valid = false;
        if (toValidate === validated) {
            valid = true;
            $(`#${invalidId}`).addClass("hide");
        } else {
            valid = false;
            $(`#${invalidId}`).removeClass("hide");
        }
        return valid;
    }

    // Signup form validation
    $("#signup").submit(function (e) {
        let invalidId = "invalid-data";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Complete profile form validation
    $("#complete-profile").submit(function (e) {
        let invalidId = "invalid-data";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Edit personal info modal form validation
    $("#form-edit-info").submit(function (e) {
        let invalidId;
        invalidId = "invalid-data-info";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Edit email modal form validation
    $("#form-edit-email").submit(function (e) {
        let invalidId = "invalid-data-email";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Edit password modal form validation
    $("#form-edit-password").submit(function (e) {
        let invalidId = "invalid-data-password";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Add group form validation
    $("#add_group").submit(function (e) {
        let invalidId = "invalid-data";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Add event form validation
    $("#add_event").submit(function (e) {
        let invalidId = "invalid-data";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Edit group form validation
    $("#edit_group").submit(function (e) {
        let invalidId = "invalid-data";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

    // Edit event form validation
    $("#edit_event").submit(function (e) {
        let invalidId = "invalid-data";
        valid = validate(invalidId);
        if (!valid) {
            e.preventDefault();
        }
    });

})