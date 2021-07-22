  $(document).ready(function () {
    $('.dropdown-button').dropdown({});

    /*https://stackoverflow.com/questions/17048223/correct-syntax-for-this-label-jquery*/
    $("[required]").each(function () {
      $('label[for=' + this.id + ']').append('<span class="required"> *</span>');
    });
  });