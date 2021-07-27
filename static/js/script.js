  $(document).ready(function () {

    // Materialize drop down funrtionality
    $('.dropdown-button').dropdown({});

    // Add asterix to labels for required fields
    // https://stackoverflow.com/questions/17048223/correct-syntax-for-this-label-jquery 
    $("[required]").each(function () {
      $('label[for=' + this.id + ']').append('<span class="required"> *</span>');
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
      }
      else  {
        $(this).val(false);
        $(this).prop('checked', false);
      }
    });

    // https://stackoverflow.com/questions/3442322/jquery-checkbox-event-handling
    $('#form-edit-preferences input[type=checkbox]').change(function () {
        console.log($(this).attr('id') + "is changing");
        if ($(this).val() === "false") {
          $(this).prop('checked', true);
          $(this).val(true);
        } else  {
          $(this).prop('checked', false);
          $(this).val(false);
        }
      });
  });