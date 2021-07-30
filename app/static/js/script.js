  $(document).ready(function () {

    // Materialize drop down functionality
    $('.dropdown-button').dropdown({});

    // Add asterix to labels for required fields 
    $("[required]").each(function () {
      $('label[for=' + this.id + ']').append('<span class="required"> *</span>');
    });

    // Toggle password visibility
    //https://www.w3schools.com/howto/howto_js_toggle_password.asp
    $(".password-visible").click(function () {
      id = $(this).attr("data-target");
      console.log(id)
      if ($(`#${id}`).attr("type") == "password") {
        $(`#${id}`).attr("type", "text");
        $(this).removeClass('fa-eye').addClass('fa-eye-slash');
      } else if ($(`#${id}`).attr("type") == "text") {
        $(`#${id}`).attr("type", "password");
        $(this).removeClass('fa-eye-slash').addClass('fa-eye');
      }
    });


    // Sign up form validation 
    $("input").change(function () {
      //  https://stackoverflow.com/questions/14384593/jquery-how-to-know-when-input-have-a-invalid-selector 
      if ($(this).is(":invalid") && $(`p[for=${this.id}]`).length > 0) {
        // fetch label text and build error message
        let label = $(`label[for=${this.id}]`).text().replace('*', '');
        let errorMsg = `Please enter a valid ${label}.`;
        // first and last name error messages
        if (($(this).attr("id") === "fname" || $(this).attr("id") === "lname")) {
          errorMsg = errorMsg + " Only the special characters - . _ are accepted. Digits are not accepted";
        }
        // display message
        $(`p[for=${this.id}]`).html(errorMsg).removeClass("hide");
      } else if ($(this).is(":valid") && $(`p[for=${this.id}]`).length > 0) {
        // hide field if valid
        $(`p[for=${this.id}]`).addClass("hide").html("");
      }
    });

    // Modals  
    $('.modal').modal();

    // Checkboxes profile page 
    $('#form-edit-preferences input[type=checkbox]').each(function () {
      if ($(this).attr('value') == "true") {
        $(this).prop('checked', true);
      } else {
        $(this).val(false);
        $(this).prop('checked', false);
      }
    });

    // Edit Email & passowrds validation 
    $('[data-check=check]').change(function () {
      check_val = $("#" + $(this).attr('data-target')).val();
      label = $(this).attr('data-target');
      if ($(this).val() != check_val) {
        // fetch label text and build error message
        let errorMsg = `Please make sure that both ${label}s match.`;
        // display message
        $(`p[for=${this.id}]`).html(errorMsg).removeClass("hide");
      } else {
        // hide field if valid
        $(`p[for=${this.id}]`).addClass("hide").html("");
      }
    });

    // Check boxes edit preferences form
    // https://stackoverflow.com/questions/3442322/jquery-checkbox-event-handling
    $('#form-edit-preferences input[type=checkbox]').change(function () {
      console.log($(this).attr('id') + "is changing");
      if ($(this).val() === "false") {
        $(this).prop('checked', true);
        $(this).val(true);
      } else {
        $(this).prop('checked', false);
        $(this).val(false);
      }
    });

    /* Call python check password on user input
       https://www.bogotobogo.com/python/Flask/Python_Flask_with_AJAX_JQuery.php
       https://healeycodes.com/javascript/python/beginners/webdev/2019/04/11/talking-between-languages.html
    */
    $('#current-pwd').change(function () {
      email = $('#user_email').text().replace(" ", "")
      check = $('#current-pwd').val()
      $.ajax({
        url: `/check_password/${email}/${check}`,
        data: email,
        type: 'POST',
        success: function (response) {
          if (response === "no match") {
            $('#message-error').html("Current password is incorrect").removeClass('hide');
          } else if (response === "match") {
            $('#message-error').html("").addClass('hide');
          }
        },
        error: function (error) {
          console.log(error);
        }
      });
    });
  });