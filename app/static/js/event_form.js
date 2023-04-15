$(document).ready(function () {

  let option;

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
    option = $(this).val();
    if (option == "in person") {
      $("#link_container").addClass("hide");
      $("#location_container").removeClass("hide");
      $("input#event_location").prop("required", true);
      $("label[for='event_location']").append('<span class="required"> *</span>');
      $("#event_link").val(null);
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
      $("#end_time_container").removeClass('hide');
    } else {
      $(this).val(false);
      $(this).prop("checked", false);
    }
  });
});