function clicButtonLogIn(){
    var modal = document.getElementById('log_in_modal');
    modal.style.display = "block";
}

function clicButtonCloseModalLogIn(){
    var modal = document.getElementById('log_in_modal');
     modal.style.display = "none";
}

function logIn(){
    var form = document.getElementById('authentication_form');
    var user_name;
    var password;
    $.ajax({
      type: "POST",
      url: form.action,
      data: {
          'user_name' : user_name,
          'password' : password
      },
      success: function(data){
          if(data) {
              console.log("bla");
          }
      },
      error:function(data){
          console.log("error");
      }
});
}