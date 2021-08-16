$(document).ready(function () {

  // Materialize side bar
  $('.sidenav').sidenav({
    edge: "right"
  });
  // Materialize drop down functionality
  $(".dropdown-trigger").dropdown();

  // Materialize collapsible 
  $(".collapsible").collapsible();

  // Materialize tabs
  $(".tabs").tabs();

  // Materialize modals  
  $(".modal").modal();

  // Materialize date picker
  $(".datepicker").datepicker({
    format: "d/mm/yyyy",
    yearRange: 3,
    showClearBtn: true,
    i18n: {
      done: "Select"
    }
  });

  // Materialize time picker
  $(".timepicker").timepicker({
    twelveHour: false,
    showClearBtn: true,
  });

  // Materialize form select
  $("select").formSelect();

  // Back to previous page
  $("button[data-action=back]").click(function () {
    window.history.back();
  })

  // Add asterix to labels for required fields 
  $("[required]").each(function () {
    $("label[for=" + this.id + "]").append('<span class="required"> *</span>');
  });

  // Toggle password visibility
  //https://www.w3schools.com/howto/howto_js_toggle_password.asp
  $(".password-visible").click(function () {
    id = $(this).attr("data-target");
    if ($(`#${id}`).attr("type") == "password") {
      $(`#${id}`).attr("type", "text");
      $(this).removeClass("fa-eye").addClass("fa-eye-slash");
    } else if ($(`#${id}`).attr("type") == "text") {
      $(`#${id}`).attr("type", "password");
      $(this).removeClass("fa-eye-slash").addClass("fa-eye");
    }
  });

  // Check images format function
  function checkImgUrl(targetImg, formData, value) {
    if (!formData) {
      src = targetImg.attr("src");
    } else {
      src = targetImg.val();
    }
    //Check if url 
    checkUrl = ["https:", "http:"];
    checkUrlValid = [];
    //Check url valid 
    checkVal = ["svg", "png", "jpg", "jpeg", "tiff", "webp", "bmp", "heif"];
    checkArray = [];
    // check for url extension
    $.each(checkUrl, function (key, value) {
      checkUrlValid.push(src.includes(value));
    })
    // check for img extension 
    $.each(checkVal, function (key, value) {
      checkArray.push(src.includes(value));
    })
    // check image display on load
    if (!formData) {
      // Default image value if url invalid
      if (!checkUrlValid.includes(true)) {
        targetImg.attr("src", `/static/images/${value}_default.png`);
      } else {
        if (!checkArray.includes(true)) {
          // Default image value if url valid but no image extension
          targetImg.attr("src", `/static/images/${value}_default.png`);
        }
      }
    } else {
      // Display error on form imput 
      errorMsg = "Leave blank or include a valid image Url and make sure that it contains an image extension such as png, jpg..."
      // check starts with http or https
      if (!checkUrlValid.includes(true)) {
        $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).removeClass("hide");
      } else {
        $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).addClass("hide");
      }
      // Check for image extension
      if (!checkArray.includes(true)) {
        $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).removeClass("hide");
      } else {
        $(`p[data-error=${targetImg.attr("id")}]`).html(errorMsg).addClass("hide");
      }
    }
  }

  // Default images for groups 
  $("img[data-default=group]").each(function () {
    checkImgUrl($(this), false, "group");
  });

  // Default images for events
  $("img[data-default=event]").each(function () {
    checkImgUrl($(this), false, "event");
  });

  // Default images for avatars
  $("img[data-default=avatar]").each(function () {
    checkImgUrl($(this), false, "avatar");
  });

  //Check imgage url in forms 
  $("textarea[data-input=img]").change(function () {
    if ($(this).val() != "") {
      checkImgUrl($(this), true, "");
    } else {
      $(`p[data-error=${$(this).attr("id")}]`).addClass("hide");
    }
  })

  //Validate Materialize Select Field 
  // From Code Institute Task Manager mini project
  validateMaterializeSelect();

  function validateMaterializeSelect() {
    let classValid = {
      "border-bottom": "1px solid #000",
      "box-shadow": "none"
    };
    let classInvalid = {
      "border-bottom": "1px solid #000",
      "box-shadow": "none"
    };
    if ($("select.validate").prop("required")) {
      $("select.validate").css({
        "display": "block",
        "height": "0",
        "padding": "0",
        "width": "0",
        "position": "absolute"
      });
    }
    $(".select-wrapper input.select-dropdown").on("focusin", function () {
      $(this).parent(".select-wrapper").on("change", function () {
        if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () {})) {
          $(this).children("input").css(classValid);
        }
      });
    }).on("click", function () {
      if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
        $(this).parent(".select-wrapper").children("input").css(classValid);
      } else {
        $(".select-wrapper input.select-dropdown").on("focusout", function () {
          if ($(this).parent(".select-wrapper").children("select").prop("required")) {
            if ($(this).css("border-bottom") != "1px solid rgb(0, 0, 0)") {
              $(this).parent(".select-wrapper").children("input").css(classInvalid);
            }
          }
        });
      }
    });
  }

  // Make sure group name is unique
  $("#group_name").change(function () {
    groupName = $("#group_name").val();
    dataCheck = $("#group_name").attr("data-check");
    if (dataCheck != null) {
      existing = dataCheck
    } else {
      existing = "none"
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
  })

  // Profile forms validation

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
    email = $("#user_email").text().replace(" ", "")
    check = $("#current-pwd").val()
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

  // Event forms 

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

  // Change display according to event type on add event
  $('#event_type').change(function () {
    option = $(this).val()
    if (option == "in person") {
      $("#link_container").addClass("hide");
      $("#location_container").removeClass("hide");
      $("input#event_location").prop("required", true);
      $("label[for='event_location']").append('<span class="required"> *</span>');
      $("#event_link").val(null)
    } else if (option == "online event") {
      $("#link_container").removeClass("hide");
      $("#location_container").addClass("hide");
      $("#event_location").removeAttr("required");
      $("label[for='event_location'] span").remove();
      $("#event_location").val(null);
    }
  });

  // Change display on edit event type
  if ($('#event_type').val() == "in person") {
    $("#link_container").addClass("hide");
    $("#location_container").removeClass("hide");
    $("#event_link").val(null);
    $("input#event_location").prop("required", true);
    $("label[for='event_location']").append('<span class="required"> *</span>');
  } else if ($('#event_type').val() == "online event") {
    $("#link_container").removeClass("hide");
    $("#location_container").addClass("hide");
    $("#event_location").removeAttr("required");
    $("label[for='event_location'] span").remove();
    $("#event_location").val(null);
  }

  // Display end date time if is end time is true
  $('#is_endtime').change(function () {
    $("#end_time_container").toggleClass("hide");
    // clear value from field
    if ($(this).is(":not(:checked)")) {
      $("#time_end").val("");
    }
  });

  // Checkboxes edit event
  $("#edit_event input[type=checkbox]").each(function () {
    if (($(this).attr("data-value") == "true") || ($(this).attr("data-value") == "True")) {
      $(this).prop("checked", true);
      $("#end_time_container").removeClass('hide')
    } else {
      $(this).val(false);
      $(this).prop("checked", false);
    }
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
  function validate() {
    toValidate = $("p.error-text").length;
    validated = $("p.error-text.hide").length;
    valid = false;
    if (toValidate === validated) {
      valid = true;
      $("#invalid-data").addClass("hide");
    } else {
      valid = false;
      $("#invalid-data").removeClass("hide");
    }
    return valid;
  }

  // Signup form validation
  $("#signup").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Complete profile form validation
  $("#complete-profile").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Edit personal info modal form validation
  $("#form-edit-info").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Edit email modal form validation
  $("#form-edit-email").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Edit password modal form validation
  $("#form-edit-password").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Add group form validation
  $("#add_group").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Add event form validation
  $("#add_event").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Edit group form validation
  $("#edit_group").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Edit event form validation
  $("#edit_event").submit(function (e) {
    valid = validate();
    if (!valid) {
      e.preventDefault();
    }
  });

  // Groups and events action 

  //Set location hash prior event and group action 
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
      actionGroupEvent(user_id, event_id, "/attend")
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
    actionGroupEvent(user_id, event_id, "/unattend")
  });

  // Toggle interest bookmarked
  $(".btn-interest").click(function () {
    if ($(this).attr("data-status") == "active") {
      let event_id = $(this).attr("data-event");
      let user_id = $(this).attr("data-user");
      actionGroupEvent(user_id, event_id, "/bookmark_interest")
    }
  });

  // Remove interest
  $(".btn-interested").click(function () {
    let event_id = $(this).attr("data-event");
    let user_id = $(this).attr("data-user");
    actionGroupEvent(user_id, event_id, "/remove_interest")
  });

  //Follow group
  $(".btn-follow").click(function () {
    if ($(this).attr("data-status") == "active") {
      let group_id = $(this).attr("data-group");
      let user_id = $(this).attr("data-user");
      actionGroupEvent(user_id, group_id, "/follow")
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
    actionGroupEvent(user_id, group_id, "/unfollow")
  });

});