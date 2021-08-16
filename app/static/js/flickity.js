$(document).ready(function () {

    //Flickity caraouse initialisation
    $(".main-carousel").flickity({
      cellAlign: 'left',
      contain: true,
      pageDots: true
    });
    
    // Select cell on load if destination has been set (event actions)
    if (window.location.hash != ""){
    $(".main-carousel").flickity( "selectCell", `${window.location.hash}`);
    }

    // Retrieve the ID of carousel cell and set the destination for reload
    $('.carousel-cell button').click(function(){
     window.location.hash = $(this).parents(".carousel-cell").attr("id");
    });

});
