$(document).ready(function () {

  // Materialize side bar
  $('.sidenav').sidenav({
    edge: "right"
  });
  // Materialize drop down functionality
  $('.dropdown-trigger').dropdown();

  // Materialize collapsible 
  $('.collapsible').collapsible();

  // Materialize tabs
  $('.tabs').tabs();

  // Materialize modals  
  $('.modal').modal();

  // Materialize date picker
  $('.datepicker').datepicker({
    format: "d/mm/yyyy",
    yearRange: 3,
    showClearBtn: true,
    i18n: {
      done: "Select"
    }
  });

  // Materialize time picker
  $('.timepicker').timepicker({
    twelveHour: false,
    showClearBtn: true,

  });

  // Materialize form select
  $('select').formSelect();



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

  //Delete group modals
  $('[data-target=delete-group-modal]').click(function () {
    group_id = $(this).attr('id');
    $('#delete-group-btn').attr('data-group', group_id)
    $('#delete-group-btn').attr('href', `/delete-group/${group_id}`)
    $.ajax({
      url: `/delete-group-modal/${group_id}`,
      data: group_id,
      type: 'POST',
      success: function (response) {
        $('#modal-group-name').text(response)
      },
      error: function (error) {
        console.log(error);
      }
    });
  });


  // Event form

  // Change display on event type
  $('#event_type').change(function () {
    option = $(this).val()
    if (option == "in person") {
      $("#link_container").addClass("hide");
      $("#location_container").removeClass("hide");
      $("input#event_location").prop("required", true)
      $("label[for='event_location']").append('<span class="required"> *</span>');
    } else if (option == "online event") {
      $("#link_container").removeClass("hide");
      $("#location_container").addClass("hide");
      $("#event_location").removeAttr("required");
      $("label[for='event_location'] span").remove();
    }
  });

  // Display end date time if is end time is true
  $('#is_endtime').change(function () {
    $("#end_time_container").toggleClass("hide");
    // clear value from field
    if ($(this).is(":not(:checked)")) {
      $("#time_end").val("")
    }
  });

  // Checkboxes edit event
  $('#edit_event input[type=checkbox]').each(function () {
    if (($(this).attr('data-value') == "true") || ($(this).attr('data-value') == "True")) {
      $(this).prop('checked', true);
      $('#end_time_container').removeClass('hide')
    } else {
      $(this).val(false);
      $(this).prop('checked', false);
    }
  });

  // Change display on event type
  if ($('#event_type').val() == "in person") {
    $("#link_container").addClass("hide");
    $("#location_container").removeClass("hide");
    $("input#event_location").prop("required", true);
    $("label[for='event_location']").append('<span class="required"> *</span>');
  } else if ($('#event_type').val() == "online event") {
    $("#link_container").removeClass("hide");
    $("#location_container").addClass("hide");
    $("#event_location").removeAttr("required");
    $("label[for='event_location'] span").remove();
  }

  //Set location hash prior event and group action 
  $('.btn-tab').click(function () {
    window.location.hash = $(this).children("a").attr("href");
    console.log("test" + $(this).children("a").attr("href"))
  });

  // Function calling python function 
  function actionGroupEvent(user_id, target_id, action) {
    // Ajax requestion to python function attend
    $.ajax({
      url: `${action}`,
      type: 'POST',
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
      },
      error: function (error) {
        console.log(error)
      }
    });
  }

  // Attend 
  $(".btn.btn-attend").click(function () {
    if ($(this).attr("data-status") == "active") {
      user_id = $(this).attr("data-user");
      event_id = $(this).attr("data-event");
      actionGroupEvent(user_id, event_id, "/attend")
    }
  });

  // Attending
  $(".btn.btn-attending").click(function () {
    event_id = $(this).attr("data-event");
    $(`.btn.btn-unattend[data-event=${event_id}]`).toggleClass("hide");
  });

  // Unattend
  $(".btn.btn-unattend").click(function () {
    event_id = $(this).attr("data-event");
    user_id = $(this).attr("data-user");
    actionGroupEvent(user_id, event_id, "/unattend")
  });

  // Toggle interest bookmarked
  $(".btn-interest").click(function () {
    event_id = $(this).attr("data-event");
    user_id = $(this).attr("data-user");
    actionGroupEvent(user_id, event_id, "/bookmark_interest")
  });

  // Remove interest
  $(".btn-interested").click(function () {
    event_id = $(this).attr("data-event");
    user_id = $(this).attr("data-user");
    actionGroupEvent(user_id, event_id, "/remove_interest")
  });

  //Follow group
  $(".btn-follow").click(function () {
    if ($(this).attr("data-status") == "active") {
      group_id = $(this).attr("data-group");
      user_id = $(this).attr("data-user");
      actionGroupEvent(user_id, group_id, "/follow")
    }
  });

  // Display unfollow button
  $(".btn.btn-following").click(function () {
    group_id = $(this).attr("data-group");
    $(`.btn.btn-unfollow[data-group=${group_id}]`).toggleClass("hide");
  });

  // Unfollow group
  $(".btn-unfollow").click(function () {
    group_id = $(this).attr("data-group");
    user_id = $(this).attr("data-user");
    actionGroupEvent(user_id, group_id, "/unfollow")
  });

  // 
  $(".collapsible-header").click(function () {
    // Ajax requestion to python function to add to read_by
    if ($(this).attr("data-status") == "not read") {
      console.log("call is happening")
      user_id = $(this).attr("data-user");
      notification_id = $(this).attr("data-notification");
      actionGroupEvent(user_id, notification_id, "/mark_as_read")
    }
  });
});