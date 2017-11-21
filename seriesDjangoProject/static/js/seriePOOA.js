$('document').ready(function(){
    $('#authentication_form').submit(function(e){
    e.preventDefault();
    });
    $('#registration_form').submit(function(e){
    e.preventDefault();
    });
    $('#searchForm').submit(function(e){
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
      success: function(data_response){
          if(data_response.status=="OK"){
              window.location.href=/index/
          }else if(data_response.status=="KO"){
              $('#authentication_error').attr('hidden',false);
          }
      },
      error:function(data_response){
          console.log("Unknown error")
      }
    });
}

function signIn(){
    var form = $('#registration_form');
    $.ajax({
      type: "POST",
      url: form['0'].action,
      data: form.serialize(),
      success: function(data_response){
          if(data_response.status=="OK"){
              window.location.href=/index/
          }
          else if(data_response.status=="KO"){
              $('#registration_error').attr('hidden',false);
          }
      },
      error:function(data_response){
          console.log("Unknown error")
      }
    });
}

function clickButtonRemoveFromFavorites(serie_id){
 url = '/remove_from_favorites/' + serie_id
    $.ajax({
      type: "GET",
      url: url,
      success: function(data){
          if(data.status=="OK"){
              location.reload();
          }else if(data.status=="KO"){
              alert("Unknown error");
          }
      },
      error:function(data){
          console.log("Unknown error");

      }
    });
}

function clickButtonAddToFavorites(serie_id){
    url = '/add_to_favorites/' + serie_id
    $.ajax({
      type: "GET",
      url: url,
      success: function(data){
          if(data.status=="OK"){
              location.reload();
          }else if(data.status=="KO"){
              alert("Unknown error");
          }
      },
      error:function(data){
          console.log("Unknown error");

      }
    });
}

function clickButtonSearch(){
    form=$('#searchForm')
    url = '/search/'
    $('#loader').removeClass("loader_hidden")
    $.ajax({
      type: "POST",
      url: form['0'].action,
      data : form.serialize(),
      success: function(data){
         $('#searchResult').replaceWith(data)
          $('#loader').addClass("loader_hidden")

      },
      error:function(data){
          console.log("Unknown error");

      }
    });
}

function clickSeriesSearch(id){
    url = '/getSeriesInformation/'
    $('#loader').removeClass("loader_hidden")
    $.ajax({
        type: "POST",
        url: url ,
        data : id,
        success: function(data){
         $('#searchResult').text(data)
          $('#loader').addClass("loader_hidden")

      },
      error:function(data){
          console.log("Unknown error");

      }
    });
}

