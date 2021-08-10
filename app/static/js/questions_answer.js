 $(document).ready(function () {
 //Question
      $("#send-question").click(function () {
      window.location.hash = "#questions_answers_container";
      questionsAnswers(user_id, target_id, $('#question').val(), action) 
    });  

    // Function calling python function 
    function questionsAnswers(user_id, target_id, data, action) {
      // Ajax requestion to python function attend
      $.ajax({
        url: `${action}`,
        type: 'POST',
        data: {
          "user_id": `${user_id}`,
          "event_id": `${target_id}`
          "data": `${data}`
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

 });