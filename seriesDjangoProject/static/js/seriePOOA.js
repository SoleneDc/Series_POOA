$('document').ready(function(){
    $('#authentication_form').submit(function(e){
    e.preventDefault();
    });

});

function clicButtonLogIn(){
    var modal = document.getElementById('log_in_modal');
    modal.style.display = "block";
}

function clicButtonCloseModalLogIn(){
    var modal = document.getElementById('log_in_modal');
     modal.style.display = "none";
}


function logIn(){
    var form = $('#authentication_form');
    $.ajax({
      type: "POST",
      url: form['0'].action,
      data: form.serialize(),
      success: function(data){
          if(data.status=="OK"){
               console.log("Bientôt on fera la redirection");
          }else if(data.status=="KO"){
              $('#authentication_error').attr('hidden',false);
          }

      },
      error:function(data){
          console.log("Unkown error")

      }
});
}