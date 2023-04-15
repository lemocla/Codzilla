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

  // Back to previous page
  $("button[data-action=back]").click(function () {
    window.history.back();
  });

});