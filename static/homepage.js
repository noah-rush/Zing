
var map
function blog(){
$.ajax({
        url:"/blog",
        success: show_post,
         beforeSend: function() {
            // console.log("before");
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
  $('#loader').hide();
   
  }
    })
}
function modalReview(){
 $("#reviewModal").modal()
        $(document).unbind("scroll")

          $("input[name='stars']").change(function(){
  stars = this.value;
  
});
         $('.search3').find('input').autocomplete({serviceUrl: '/autocomplete/justshows', onSelect: function(e){
        if(e['type'] == "venue"){
            // window.location.href = '#venue/'+e['data']
        }else{
            // window.location.href = '#show/'+e['data']
            $('.search3').find('input').val(e['value'])
            $('.widget-modal-review .head').html("What did you think of " + e['value'] + "?")

            $('.widget-modal-review').slideToggle();
            $('.modalShowID').text( e['data'] );
            $('#reviewModal').animate({"top": "0%"})

         
            // $('body').append('<div class = "modal-backdrop"></div>')
        }
    
        }
      }); 
            $('#reviewModal').on('hidden.bs.modal', function (e) {
              mainPageAutoComp();
              $('.widget-modal-review').hide();
              $('.search3').find('input').val("");
              $('#reviewModal').animate({"top": "25%"})

})
}

function mainPageAutoComp(){
   $(document).on("scroll", function(){
      var searchHeight = $('.search').height() + "px"
      if($('.search').find('input').val()!=""){
        if($('.page-header-middle').hasClass("fixed")){

          $('.autocomplete-suggestions').css({"position":"fixed", "top": searchHeight})
        }else{
          $('.autocomplete-suggestions').css({"position": "absolute", "top":"190px"})

        }
      }
    })
    $('.search').find('input').on("input", function(){
      var searchHeight = $('.search').height() + "px"
      if($('.search').find('input').val()!=""){
        if($('.page-header-middle').hasClass("fixed")){

          $('.autocomplete-suggestions').css({"position":"fixed", "top": searchHeight})
        }else{
          $('.autocomplete-suggestions').css({"position": "absolute", "top":"190px"})

        }
      }
    })
    $('.search').find('input').on("click", function(){
      var searchHeight = $('.search').height() + "px"
      if($('.search').find('input').val()!=""){
        if($('.page-header-middle').hasClass("fixed")){

          $('.autocomplete-suggestions').css({"position":"fixed", "top": searchHeight})
        }else{
          $('.autocomplete-suggestions').css({"position": "absolute", "top":"190px"})

        }
      }
    })
}


//////////////Page Nav/Component Ajax Requests
function autocomp(){


 
    $('.search').find('input').autocomplete({serviceUrl: '/autocomplete/allshows', onSelect: function(e){
        if(e['type'] == "venue"){
            window.location.href = '#venue/'+e['data']
        }else{
            window.location.href = '#show/'+e['data']
        }
    
        $('.search').find('input').val('')
        }
    }); 
    $('.search2').find('input').autocomplete({serviceUrl: '/autocomplete/allshows', onSelect: function(e){
        if(e['type'] == "venue"){
            window.location.href = '#venue/'+e['data']
        }else{
            window.location.href = '#show/'+e['data']
        }
    
        $('.search2').find('input').val('')
        }
    }); 
    if($(window).width()>700){
mainPageAutoComp();
}
   
}; 

function updateOutsideArticles(){

$.ajax({
        url:"/updateArticles",
        success: function(data){
            alert(data)
        },
         beforeSend: function() {
            // console.log("before");
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
    // console.log("done")
     $('#loader').hide();
     homepage();
  }
    })

}



function getnowplaying(){
    $.ajax({
        url: "/nowPlaying",
        success: displaynowplaying
    });

};
function getzingdescript(){
    $.ajax({
        url: "/zingDescript",
        success: displayzingdescript
    });

};
function getcomingsoon(){
    $.ajax({
        url: "/comingsoon",
        success: displaycomingsoon
    });

};
function about(){
   $.ajax({
    url: "/about",
    success: show_post
   })
   $('.secondary-nav li').each(function(e){
    $(this).find('a').removeClass('active')
    if($(this).find('a').attr('href') == "#about"){
      $(this).find("a").addClass("active");
    }
   })
}

function get_all_shows(){
    $.ajax({
        url: "/allshows",
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
        success: display_all_shows
    });

};
function full_schedule(){
    $.ajax({
        url: "/fullschedule",
        success: show_post,
         beforeSend: function() {
            // console.log("before");
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
  
     $('#loader').hide();
  
  }
    });

};
function pastshows(){
    $.ajax({
        url: "/pastshows",
        success: show_post,
         beforeSend: function() {
            // console.log("before");
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
  
     $('#loader').hide();
  
  }
    });

};
function full_theater(){
    $.ajax({
        url: "/fulltheater",
        success: show_post,
         beforeSend: function() {
            // console.log("before");
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
  
     $('#loader').hide();
  
  }
    });

};
function full_reviews(){
    $.ajax({
        url: "/fullreviews",
        success: show_full_reviews,
         beforeSend: function() {
            // console.log("before");
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
  
     $('#loader').hide();
  
  }
    });

};
function ads(){
        $.ajax({
        url: "/topPanel",
        success: displayAds
    });
}

function profile(){
    $.ajax({
        url: "/profile",
        success: show_post
    });

};

function show_venues(){
    $.ajax({
        url: "/venues",
        success: display_venues
    });
}

function show_nowPlaying(){
    $.ajax({
        url: "/nowPlaying",
        success: display_nowPlaying
    });
}

function find(data){
  
    window.location.hash = data;
    $.ajax({
        url: '/show',
        data: {
            show: data
        },
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
        success: display_show
    })
}
function post(data){
    id = data
    // window.location.hash = data;
    $.ajax({
        url: '/post',
        data: {
            id: id
        },
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
        success: show_post
    })
}
function reviews(data){
    pub = data
    
    $.ajax({
        url: '/source',
        data: {
            pub: pub
        },
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
        success: show_full_reviews
    })
}

function show(data){

    $.ajax({
        url: '/show',
        data: {
            show: data
        },
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
        success: display_show
    })
};
function venue(data){
    $.ajax({
        url: '/venue',
        data: {
            venue: data
        },
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
        success: display_venue
    })
};

function homepage(){
    $.ajax({
        success: show_homepage,
        url:"/home"
    })
}
function open_editor(){
    $.ajax({
        success: show_editor,
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
        url:"/edit"
    })
}
function manageReviews(){
    $.ajax({
        success: show_manager,
        url:"/manageReviews",
           beforeSend: function() {
            
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  }
    })
}
function manageOutReviews(){
    $.ajax({
       
        url:"/manageOutReviews",
        beforeSend: function() {
            // console.log("before");
             $(".page-content").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
    // console.log("done")
     $('#loader').hide();
     show_out_manager();
  },
  success:show_out_manager
    })
}
function survey(){
    $.ajax({
        url: "/getsurvey",
        success: show_survey
    })
}
function survey2(){
    $.ajax({
        url: "/getsurvey",
        success: show_survey2
    })
}
function signin(){
    var email = $("#loginEmail").val();
    var hidden = $("#loginPassword").val();
    $.ajax({
        type:"POST",
        url:"/signin",
        data:
        {email:email,
        hidden:hidden
        },
        success: show_password
    })
}
//////////////////////End Ajax Page Requests 



//////////////////////Login/Logout User Data

////////Facebook loading api asynchrously
function facebook(){
     function statusChangeCallback(response) {
    // console.log('statusChangeCallback');
    // console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().

    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI();
      // console.log("connected")
      
    } else if (response.status === 'not_authorized') {
        // console.log("not authorized");
    } else {
        // console.log("other else");
    }
  }

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

  window.fbAsyncInit = function() {
  FB.init({
    appId      : 698403073548094,
    cookie     : true,  // enable cookies to allow the server to access 
                        // the session
    xfbml      : true,  // parse social plugins on this page
    version    : 'v2.0' // use version 2.0
  });


  // Now that we've initialized the JavaScript SDK, we call 
  // FB.getLoginStatus().  This function gets the state of the
  // person visiting this page and can return one of three states to
  // the callback you provide.  They can be:
  //
  // 1. Logged into your app ('connected')
  // 2. Logged into Facebook, but not your app ('not_authorized')
  // 3. Not logged into Facebook and can't tell if they are logged into
  //    your app or not.
  //
  // These three cases are handled in the callback function.

FB.getLoginStatus(function(response) {
  if($('#userInSession').text() == "none"){
    statusChangeCallback(response);
  }
  });


  };
  

  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function testAPI() {
    // console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
        // console.log('Successful login for: ' + response.name);
        // console.log(JSON.stringify(response));
        // console.log(response)
        var name = response.first_name;
        // console.log(response.first_name);
        name = response.first_name;
        $.ajax({
        type:"POST",
        url: "/fblogin",
        success: handle_login,
        data: {
            firstname: response.first_name,
            lastname: response.last_name,
            email: response.email
        }
    });

    });


    


  }
}
///////////////////////////

function handle_login(data){
    // console.log(data);
    if(data.substring(0,4) == "<h3>"){
        $("#loginModal").html(data);
        $("#loginModal").modal('show');


    }
    $('body').html(data);


}







function signup(){
    
    var lastname = $("#newlast").val();
    var firstname = $("#newfirst").val();
    var email = $("#newemail").val();
    var password = $("#newpassword").val();
    // console.log(lastname, firstname, email, password);
    // var month = $("#month").val();
    // var day = $("#day").val();
    // var year = $("#year").val();
     $.ajax({
        type: "POST",
        url: "/zingnewuser",
        data: {
            email:  email,
            firstname: firstname,
            lastname: lastname,
            password: password,
         
        },
        success: show_password
    });
}

function login_rout(data){
    // console.log(data);
    var str = data.substring(0,3);
    var somethingwrong = $("#somethingWrong")
    switch(str){
        case "Log":
            var user = data.substring(18);
            // console.log(user);
            $("#loginscreen").hide();
            var nouser = $("#nouser");
            nouser.hide();
            var logout = $("#logout");
            var name = $("#name");
            var yesuser = $("#yesuser");
            yesuser.text(user)
            yesuser.show();

            logout.show();
            name.show();
            break;
        case "Use":
            somethingwrong.show();
            somethingwrong.text("Username not found. Try again.");
            break;
        case "Inc":
            somethingwrong.show();
            somethingwrong.text("Incorrect Password. Try again.");
            break;
        }
}
function logout(){
    var fbresponse = false
    FB.getLoginStatus(function(response) {
     if (response.status === 'connected') {
      // Logged into your app and Facebook.
      fbresponse = true 
      
    }
  });
    if(fbresponse){
    FB.logout(function(response) {
    });
    }
    var check = $("#user");
    check.text(" Login ");
    var check = $("#panelheaderuser");
    check.html( "<a class=\"btn btn-default btn-sm\" href = \"#login\" type=\"button\" ><span class = \"glyphicon glyphicon-user\"></span><span id = \"user\" >  Login</span></a>");
    $.ajax({
        url: "/logout",
        success:function(){window.location.href = ""}
        
    });



}

function login_func(){
    $("#loginModal").modal();
   
    $( "#signintrigger" ).trigger( "click" );
}

function login_func_sidebar(){
    $("#loginModal").modal();
  
    $( "#signuptrigger" ).trigger( "click" );
    
}

function show_modal(data){
    if(data == 'true'){
        $('#myModal').modal();
    }else{
        $('#loginModal').modal();
    }
}

function facebookLogin(){
  console.log("got to there ")
     FB.login(function(response) {
FB.api('/me', function(response) {
    name = response.first_name;
    console.log(response);
 
        
              $.ajax({
        type: "POST",
        url: "/login",
        success: function(){
          window.location.href = ""
        },
        data: {
           
            firstname: response.first_name,
            lastname: response.last_name,
            email: response.email
        }
    });
       
  })
  
 }, {scope: 'public_profile,email'});
}
function show_survey(data){
    
    $("#emailModal").find('.panel').html(data);
    $("#emailModal").modal();
    $( "#sortable1").sortable({
        update: function( event, ui ) {
$(".ui-state-default").each(function(e,val){$(val).text((e+1)+ ") "+$(val).text().substring(3))})


        }
    }).disableSelection();
$(".ui-state-default").each(function(e,val){$(val).text((e+1)+ ") "+$(val).text())})
}
function show_survey2(data){
    
    $(".widget-survey").html(data)
    $('a[href="#doneSurvey"]').text("Save");
    $('a[href="#doneSurvey"]').attr("href", "#doneSurvey2")
   $('.surveyDescript').hide();
    $( "#sortable1").sortable({
        update: function( event, ui ) {
$(".ui-state-default").each(function(e,val){$(val).text((e+1)+ ") "+$(val).text().substring(3))})


        }
    }).disableSelection();
$(".ui-state-default").each(function(e,val){$(val).text((e+1)+ ") "+$(val).text())})
}

function donesurvey(){
    // console.log("HERERERER")
    var preferences = {};
    var yes = false;
    var no = false;
$(".ui-state-default").each(function(e,val){
    // $(val).text((e+1)+ ") "+$(val).text())
    // console.log($(val).attr('value'))
    preferences[$(val).attr('value')] = e+1;
})
if($('#Yes').prop('checked')){
yes = true;
}
if($('#No').prop('checked')){
no = true;
}
var commitment
 $('.theatergoing input:checked').each(function() {
            console.log(this.value);
            commitment = this.value;
            
        });
// console.log(yes);
// console.log(no);
// console.log(preferences);

$.ajax({
    url: "/donesurvey",
    data: {prefs: JSON.stringify(preferences), 
            yes: yes, 
            no: no,
            commitment: commitment
            },
    success:  function(){$("#emailModal").find('.panel').html('<h3>Thank you for signing up! Please check your email to verify your account. Welcome to Zing!</h3>');
             
            }
})


}

function donesurvey2(){
    // console.log("HERERERER")
    var preferences = {};
    var yes = false;
    var no = false;
$(".ui-state-default").each(function(e,val){
    // $(val).text((e+1)+ ") "+$(val).text())
    // console.log($(val).attr('value'))
    preferences[$(val).attr('value')] = e+1;
})
if($('#Yes').prop('checked')){
yes = true;
}
if($('#No').prop('checked')){
no = true;
}
var commitment
 $('.theatergoing input:checked').each(function() {
            console.log(this.value);
            commitment = this.value;
            
        });
// console.log(yes);
// console.log(no);
// console.log(preferences);

$.ajax({
    url: "/donesurvey",
    data: {prefs: JSON.stringify(preferences), 
            yes: yes, 
            no: no,
            commitment: commitment
            },
            beforeSend: function() {
            
             $(".widget-popular").html("<div id = 'loader'><img src = 'static/ajax-loader.gif'></img></div>");
     $('#loader').show();
  },
  complete: function(){
   
     $('#loader').hide();
     
  },
    success:  function(){
              if($('.grid-cont').hasClass('user-profile')){
                profile()
              }
            }
})


}

function setLoginModal(){
$("#signintrigger").click(function(){

    $(".signInForm").show();
      $(".signUpForm").hide();
    $(this).addClass("active");
    $("#signuptrigger").removeClass("active");

    $("#loginPassword").keyup(function(event){
    if(event.keyCode == 13){
        $("#signinbutton").click();
    }
});
})
$("#signuptrigger").click(function(){
    $(".signUpForm").show();
      $(".signInForm").hide();
    $(this).addClass("active");
    $("#signintrigger").removeClass("active");
})
}


function show_password(data){
    
    
    if(data[0] == "U"){
        // $('#panelheaderuser').html(' <div class="dropdown">\
        //                         <button class="btn btn-default btn-sm dropdown-toggle" type="button" data-toggle="dropdown">\
        //                             <span class="glyphicon glyphicon-user"></span>\
        //                             <span id="user">{{useron}}</span>\
        //                             <span class="caret"></span>\
        //                         </button>\
        //                         <ul class="dropdown-menu" role="menu">\
        //                             <li><a href="#logout">Logout</a>\
        //                             </li>\
        //                         </ul>\
        //                     </div>');
        // $('#user').text(" " + data.substring(10));
        // $("#loginModal").modal('hide');
        window.location.reload();

    }
     if(data[0] == "P"){
       $('#somethingWrong').html('Please Login with Facebook <br><hr><br>');
       $('#somethingWrong').css({"color" : "red"});
       $('#somethingWrong').show()


    }
    if(data[0] == "E"){
        $('#signintrigger').trigger('click');
        $('#somethingWrong').html('An account with that email already exists. <br> Please sign in or use a different email. <br> If you signed up with facebook, please log in with facebook <br> <hr><br>')
        $('#somethingWrong').css({"color" : "red"});
        $('#somethingWrong').show()

    }
    if(data[0] == "I"){
        $('#somethingWrong').html('Incorrect Password. Try Again<br><hr><br>')
        $('#somethingWrong').css({"color" : "red"});
        $('#somethingWrong').show()
    }
    if(data[0] == "N"){  
      $('#loginModal').modal('hide')
      survey() 
   }
    if(data[0] == "A"){
        $('#loginModal').modal('hide')
          survey();
    }
    if(data[0] == "F"){
        
       $('#somethingWrong').html('No account was found with that email address.<br><hr><br>');
       $('#somethingWrong').css({"color" : "red"});
       $('#somethingWrong').show()
    }       
}
////////////////////////End of Login Stuff





/////////////////Retrieval From Ajax, this can be compressed
function display_show(data){
    jQuery('body').animate({"scrollTop":0})
    $(".page-content").html(data);
    $('.WriteReviewMobile').click(function(){
  modalReview()
  $('.search3').find('input').val($('#myModalLabel').text());
  $('.widget-modal-review .head').html("What did you think of " + $('#myModalLabel').text() + "?")
  $('.widget-modal-review').slideToggle();
  $('.modalShowID').text($('#showid').text());
  $('#reviewModal').animate({"top": "0%"})


})
    $('.loginSidebar').click(function(){
        login_func_sidebar();
})
    jQuery('.field-content p br:first-child').remove()
    $('a[href="/barrymore-awards/2015/recommended"]').remove();
    $('[data-toggle="tooltip"]').tooltip()
    $("#sawthis").on("click", 
      function(){
        $.ajax({
          url : "/sawthis",
          data: {id: $("#showid").text()},
          success: function(data){
            $('.showCount').text(data)
          }
        })
      })
    var initRating = $("#startRating").text();
    $(".total-star-rating i").css("width", initRating +"%");
    $('.bar').append(Math.round( initRating) + "%");
     $("input[name='stars']").change(function(){
  stars = this.value;
  
});
    $('#widgets-switcher').on('click', function()
  {
    // console.log(this);
              $('.widgets-switcher').siblings().slideToggle();

    if( $(this).parent().hasClass('hidden') )
    {
      $(this).removeClass('fa-flip-horizontal');
      $(this).parent().prev().removeClass('grid-col-11').addClass('grid-col-8');      
      $(this).parent().removeClass('hidden').removeClass('grid-col-1').addClass('grid-col-4');
    }
    else
    {
      $(this).addClass('fa-flip-horizontal');
      $(this).parent().prev().removeClass('grid-col-8').addClass('grid-col-11');
      $(this).parent().addClass('hidden').removeClass('grid-col-4').addClass('grid-col-1');
    }
    return false;
  });
};

function display_venue(data){
    jQuery('body').animate({"scrollTop":0})
    $(".page-content").html(data);
    $('.showAtVenueDescript').remove();
    jQuery('.field-content p br:first-child').remove()
    $('a[href="/barrymore-awards/2015/recommended"]').remove();
    var address = $("#address").text();
 $('#widgets-switcher').on('click', function()
  {
                  $('.widgets-switcher').siblings().slideToggle();

    // console.log(this);
    if( $(this).parent().hasClass('hidden') )
    {
      $(this).removeClass('fa-flip-horizontal');
      $(this).parent().prev().removeClass('grid-col-11').addClass('grid-col-8');      
      $(this).parent().removeClass('hidden').removeClass('grid-col-1').addClass('grid-col-4');
    }
    else
    {
      $(this).addClass('fa-flip-horizontal');
      $(this).parent().prev().removeClass('grid-col-8').addClass('grid-col-11');
      $(this).parent().addClass('hidden').removeClass('grid-col-4').addClass('grid-col-1');
    }
    return false;
  });
    var urlsearch = 'https://maps.googleapis.com/maps/api/geocode/json?address=' +address + '&key=AIzaSyAIlo8iZZm7IfAlLbbqPV42jeGHxanPgyg'
    $.ajax({
    url: urlsearch,
    success: initialize
    })
    google.maps.event.trigger(map, 'resize')
}
function initialize(data) {
    // console.log(data);
    var map_canvas = $('#map_canvas')[0];
    var lat = data.results[0]['geometry']['location']['lat'];
    var lng = data.results[0]['geometry']['location']['lng'];
    var map_options = {
      center: new google.maps.LatLng(lat, lng),
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(map_canvas, map_options);
    var myLatlng = new google.maps.LatLng(lat,lng);
    var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title: $(".title").text()
    });
    var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 style = "font-size: 14pt" id="firstHeading" class="firstHeading">' +$(".title").text() + '</h1>'+
      '<div id="bodyContent">'+
      '</div>'+
      '</div>';
    var infowindow = new google.maps.InfoWindow({
        content: contentString
    });
    google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map,marker);
    });
    marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
    marker.setMap(map);
    $(window).resize(function() {
        
    });
   google.maps.event.trigger(map, 'resize')
    $.ajax({
    url: "/yelp",
    data: {
        lat: lat,
        lng: lng
    },
    success: yelpresults
    })

}
function yelpresults(data){
    data = jQuery.parseJSON(data);

    markers = Array();
    

$('#findRestaurants').on("click", function(e){

    for(i=0; i<data.length; i++){
        data[i];
        
        var myLatlng = new google.maps.LatLng(data[i][1],data[i][2]);
var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<a href = "' + data[i][5] + '"><h1 style = "font-size: 14pt" id="firstHeading" class="firstHeading">' +data[i][0] + '</h1></a>'+
      '<div id="bodyContent">'+
      '</div>'+
      '<img src = "' + data[i][4]+'">'
      '</div>';
    var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    html: contentString,
     animation: google.maps.Animation.DROP,
    title:data[i][0],
  
});
   var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 style = "font-size: 14pt" id="firstHeading" class="firstHeading">' +data[i][0] + '</h1>'+
      '<div id="bodyContent">'+
      '</div>'+
      '</div>';
infowindow = new google.maps.InfoWindow({
    content: "holding..."
})

google.maps.event.addListener(marker, 'click', function(){
    infowindow.setContent(this.html);
    infowindow.open(map,this);
})


    
}

})
}
function show_post(data){
     $(".page-content").html(data);
     pager()
         jQuery('.field-content p br:first-child').remove()
jQuery('.fullschedule .showAtVenueDescript').remove()
     jQuery('body').animate({"scrollTop":0})
      $('a[href="/barrymore-awards/2015/recommended"]').remove();

 
}
function show_full_reviews(data){
     $(".page-content").html(data);
     $('.fullreviews .reviewDescript img').remove();
     $('.fullreviews .reviewDescript a').attr("target", "_blank");
     jQuery('body').animate({"scrollTop":0})
     $('.paperlogo[href = "#reviews/philcom"]').css({"width": "30%"})
     $('.paperlogo[href = "#reviews/city-paper"]').css({"width": "27%"})
     $('.paperlogo[href = "#reviews/phin"]').css({"width": "32%"})
     
     // jQuery('.showAtVenue').each(function(){
     //    $(this).prepend($(this).find('img'))
     
     // })
     //  jQuery('img').each(function(){
     //    if($(this).attr('src').indexOf('~ff')>0){
     //        $(this).remove();
     //    }

     //    if($(this).attr('src').indexOf('feedburner')>0){
     //        $(this).remove();
     //    }
     // })
 jQuery('.showAtVenue').each(function(){
       
        if($(this).find('img').length==0){
            // console.log(this);
            // $(this).find('.showAtVenueTitle').css({"width":"90%"
            // })
            // $(this).find('.reviewDescript').css({"width":"90%"
            // })
        }
     })

 
}
function show_out_manager(data){
    jQuery('body').animate({"scrollTop":0})
    $(".page-content").html(data);
    var addingTagID
   
     $('.anOutReview').each(function(){
      $(this).find('.addAtag').autocomplete({serviceUrl: '/autocomplete/allshows', onSelect: function(e){
        if(e['type'] == "venue"){
            
        }else{
        
        $(this).val(e['value'])
        $(this).parent().find('.addTag').val(e['data'])
        }
  }
}
)
$(this).find('.addTag').click(function(){
  var showid = $(this).val()
  var reviewid = $(this).parent().find('.removeOutReview').val()
  // console.log(showid);
  // console.log(reviewid)
  $.ajax({
    url: "/addtag",
    data: {
      showid: showid,
      reviewid: reviewid
    },
    success:
    manageOutReviews
  })
})


}
)
 
    $('.removeOutReview').click(function(){
         $.ajax({
            success: manageOutReviews,
            data: {articleid: this.value},
            url: "/removeOutReview"
        });
    })
    $('.removeTag').click(function(){
        var articleid = this.value.substring(1, this.value.indexOf(","));
        var showid = this.value.substring(this.value.indexOf(",")+2, this.value.length-1 );
        $.ajax({
            success: manageOutReviews,
            data: {articleid: articleid,
                showid:showid},
            url: "/removeTag"
        });
    })
}

function show_manager(data){
    jQuery('body').animate({"scrollTop":0})
    $(".page-content").html(data);
    autocomp();
    $('.removeReview').click(function(){
        var showid = this.value.substring(1, this.value.indexOf(","));
        var userid = this.value.substring(this.value.indexOf(",")+2, this.value.length-1 );
        // console.log(this.value.substring(1, this.value.indexOf(",")));
        // console.log(this.value.substring(this.value.indexOf(",")+2, this.value.length-1 ));
        $.ajax({
            success: manageReviews,
            data: {showid: showid, 
                userid: userid},
            url: "/removeReview"
        });
    })
}
function show_editor(data){
    jQuery('body').animate({"scrollTop":0})
    $(".page-content").html(data);
     $('#addtags').autocomplete({serviceUrl: '/autocomplete/justshows', onSelect: function(e){
          console.log(e)
      }}); 
    CKEDITOR.replace( 'editor1' );
    CKEDITOR.replace( 'editor2' );
    $('#addtag').on('click', function(e){
        $('.tag-drop').append('<span>' + $('#addtags').val() + '<a class = "close">x</a></span>');
        $('.close').on('click', function(e){
      e.currentTarget.parentElement.remove();
    }
    )
    }
    )
    $('#fileupload').fileupload({
        dataType: 'json',
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                
                $('#photopath').val(file);
                $('.modal-body').html( '<img src = "static/images/' + file + '" width = "100%">');
                $('.modal-header').html( file);
                $("#imageModal").modal('show');
                var column = $("#addphoto").parent()
                column.append('<br><br><a data-toggle="modal" data-target="#imageModal" class = "btn btn-info">View Photo</a>')
                $('#addphoto').text("Change Photo")
               
            });
        }
    }
    )
    $('#addphoto').on('click', function(e){
       
        $('#fileupload').trigger('click');
    });




}
var stars = 0;

// function displayAds(data){
//      $('#panelads').find(".panel-body").html(data);
   

//      $(".sidebar-link-top").hover(function(e){
       
// if(e['type'] == 'mouseenter'){
//     $(e['currentTarget']['lastElementChild']).slideToggle();
// }else{
//       $(e['currentTarget']['lastElementChild']).slideToggle();
// }
// });
//   }
// function displaynowplaying(data){
	
// 	$("#panelc2").html(data);
// }
// function displayzingdescript(data){
	
// 	$("#paneldescript").html(data);
// }
// function displaycomingsoon(data){
	



// 	$("#panelc3").html(data);
//     // console.log($(".page2"));
//     if($(".page2").length == 0){
//         $(".page-turn-links").hide();
//     }
//     //    if($($(".list-group-item")[0]).width()<300){
//     //     console.log("yup");
//     //     $("#starsspot").hide();
//     // }
//     // if($($(".list-group-item")[0]).width()>300){
//     //     console.log("yup");
//     // }
// }









function show_reviews(){
	$("#writeuserreview").show();
}



function pager(){
  var pages = Math.floor($('.blog-list .item').length/6)
  // console.log(Math.floor($('.blog-list .item').length/6))
  for(var i = 0; i<=pages; i++){
    pagenum = i+1
    if(pagenum ==1 ){
      $('.pager').append('<a class = "active pager' + pagenum + '" href="#page' + pagenum+'">'+ pagenum + '</a>');
    }else{
    $('.pager').append('<a class = "pager' + pagenum + '" href="#page' + pagenum+'">'+ pagenum + '</a>');
  }
  }
}

function popularItems(){
var thisweekCount = $('#popuplar-news-1').find('a').length;
var trendcount = $('#popuplar-news-2').find('a').length;
var topcount = $('#popuplar-news-3').find('a').length;
// console.log(thisweekCount);
// console.log(trendcount);
// console.log(topcount);
if(thisweekCount>3){
  $('.toggle-shows-right').click(function(){
    if($('a[href="#popuplar-news-1"]').hasClass('active')){
      var firsthidden = $($('#popuplar-news-1').find('.pic-hidden')[0])
     firsthidden.css("display", "inline-block");
     firsthidden.removeClass('pic-hidden');
      var firstshown = $($('#popuplar-news-1').find('a')[0])
   
    $('#popuplar-news-1').append(firstshown);

     firstshown.hide();
     firstshown.addClass('pic-hidden');
   
    // firstshown.addClass('pic-hidden');

    }
  })
}
if(trendcount>3){
  $('.toggle-shows-right').click(function(){
    if($('a[href="#popuplar-news-2"]').hasClass('active')){
      var firsthidden = $($('#popuplar-news-2').find('.pic-hidden')[0])
     firsthidden.css("display", "inline-block");
     firsthidden.removeClass('pic-hidden');
      var firstshown = $($('#popuplar-news-2').find('a')[0])
   
    $('#popuplar-news-2').append(firstshown);

     firstshown.hide();
     firstshown.addClass('pic-hidden');
   
    // firstshown.addClass('pic-hidden');

    }
  })
}
if(topcount>3){
  $('.toggle-shows-right').click(function(){
    if($('a[href="#popuplar-news-3"]').hasClass('active')){
      var firsthidden = $($('#popuplar-news-3').find('.pic-hidden')[0])
     firsthidden.css("display", "inline-block");
     firsthidden.removeClass('pic-hidden');
      var firstshown = $($('#popuplar-news-3').find('a')[0])
   
    $('#popuplar-news-3').append(firstshown);

     firstshown.hide();
     firstshown.addClass('pic-hidden');
   
    // firstshown.addClass('pic-hidden');

    }
  })
}


}



function publish(){
  var article = CKEDITOR.instances.editor1.getData();
  var descript = CKEDITOR.instances.editor2.getData();
  var title = $('#post-title').val();
  var author = $('#post-author').val();
  var tags = $('.tag-drop');
  var photo = $('#photopath').val();

  finalTags = []
  for(i = 0; i<tags[0].children.length; i++){
  
    finalTags.push(tags[0]['children'][i]['firstChild']['textContent'])

  }
 
  var column = $('#addphoto').parent();
  column[0].children[0]['innerText'] = "Update";
  column[0].children[0]['href'] = "#update";
  finalTags = JSON.stringify(finalTags)
  $.ajax({
    url: "/contentPost",
    data: {title: title,
        descript: descript,
        tags: finalTags,
           author: author,
           photo: photo,
            article: article}
  })

}


function show_reviews(){
	$("#writeuserreview").show();
	$("#submitreview").show();
	
}







function modal_submit_review(){
var goods = [];
        $('#reviewModal #checkboxlistgood input:checked').each(function() {
          
          goods.push(this.name)
        });
    var bads = [];
        $('#reviewModal #checkboxlistbad input:checked').each(function() {
          
          bads.push(this.name)
        });
       
  var text = $("#reviewModal #writeuserreview").val();
 var showid = $('.modalShowID').text()
   $.ajax({
    url: "/submitreview",
    data: {
      show: showid,
      text: text,
      stars: stars,
      goods: JSON.stringify(goods),
      bads: JSON.stringify(bads)
    },
    beforeSend: function() {
             $('#reviewModal').modal('hide');
  },

    success: function(){
    
      
      show(showid);
    }
  });
    //  var url = window.location.href;
    //  var idfirst = url.lastIndexOf("/");
    //  var id = url.substring(idfirst +1);
    
    // window.location.href = "#show/"+id;

}




function submit_review(){

	var goods = [];
        $('#checkboxlistgood input:checked').each(function() {
        	
        	goods.push(this.name)
        });
    var bads = [];
        $('#checkboxlistbad input:checked').each(function() {
        	
        	bads.push(this.name)
        });
       
	var text = $("#writeuserreview2").val();
	var showname = $("#showname").text();
	var showid = $('#showid').text();
  // console.log(showid);
	 $.ajax({
		url: "/submitreview",
		data: {
			show: $('#showid').text(),
			text: text,
			stars: stars,
			goods: JSON.stringify(goods),
			bads: JSON.stringify(bads)
		},
    beforeSend: function() {
            // console.log("before");
         
  },

    success: function(){
    
      
      show(showid);
    }
	});
    
    
    // window.location.href = "#show/"+id;
	  


}

function start (){
	// getzingdescript();
	//getnowplaying();
	// getcomingsoon();
	// homepage();
    // inputs();
    pager();
    popularItems();
$(window).hashchange( function test(){
	var hash = location.hash;
	if(hash.substring(0,5) == "#show")
	{
		// console.log(hash);
		show(hash.substring(6));
	}
	if(hash.substring(0,6) == "#venue")
	{
		
		venue(hash.substring(7));
	}
    if(hash.substring(0,5) == "#post")
    {
     
        post(hash.substring(6));
    }
     if(hash.substring(0,8) == "#reviews")
    {
        // console.log("here")
        reviews(hash.substring(9));
    }
     if(hash.substring(0,5) == "#page")
    {
        page = hash.substring(5);
        var pages = Math.floor($('.blog-list .item').length/5)
      
        for(var i = 0; i<=pages; i++){

          pagenum = i+1
          // console.log(pagenum)
          $('.page' + pagenum).hide();
        }
        for(var i = 0; i<=pages; i++){

         pagenum = i+1
          $('.pager' + pagenum).removeClass('active');
          if(page == pagenum){
            $('.pager' + pagenum).addClass('active');
          }
        }
        
        $(".page" + page).show()
        jQuery('body').animate({"scrollTop":jQuery('.postsList .head').offset().top - $('.fixed').height()})
        nextPage = parseInt(page) + 1
        prevPage = parseInt(page) - 1
   
        if($(".page" + nextPage).length > 0){
           $(".pager .next").show()
            $(".pager .next").attr('href',"#page" + nextPage);
           
             
        }else{
             $(".pager .next").hide()
        }
        if(prevPage != 0){
           $(".pager .prev").show();
            $(".pager .prev").attr('href', "#page" + prevPage);
           
        }else{
            $(".pager .prev").hide();
        }

        
    }
    // console.log(hash);
	switch(hash){
	case "#venues":
		show_venues();
		break;
	case "#nowplaying":
		show_nowPlaying();
		break;
	case "#createEvent":
		alert();
		break;
	case "#login":
		login_func();
		break;
    case "#login_sidebar":
        login_func_sidebar();
        break;
	case "#signup":
		signup();
		break;
	case "#logout":
		logout();
		break;
	case "#createAccount":
		create_Account();
		break;
	case "#facebookLogin":
		facebookLogin()
		break;
	case "#signin":
		signin()
		break;
	case "#home":
		homepage()
		break;
	case "#profile":
		profile()
		break;
	case "#submitreview":
		submit_review()
		break;
    case "#allshows":
        get_all_shows()
        break;
    case "#fullschedule":
        full_schedule()
        break;
    case "#fulltheatres":
        full_theater()
        break;
    case "#fullreviews":
        full_reviews()
        break;
    case "#editpage":
        open_editor();
        break;
    case "#publish":
        publish();
        break;
    case "#update":
        publish(); 
        break;
    case "#about":
        about();
        break;
    case "#moreShows":
        break;
    case "#updateOutsideArticles":
        updateOutsideArticles()
        break;
    case "#manageReviews":
        manageReviews();    
        break;
    case "#manageOutReviews":
        manageOutReviews();    
        break;
    case "#doneSurvey":
        donesurvey();
        break;
    case "#userSurveyTest":
        survey();
        break;
    case "#profile":
        profile();
        break;
    case "#editSurvey":
        survey2();
        break;
    case "#doneSurvey2":
        donesurvey2();
        break;
    case "#pastshows":
        pastshows();
        break;
    case "#blog":
        blog();
        break;
    case "#emailNotYet":
        $("#emailNotYetModal").modal()
          $('#emailNotYetModal').on('hidden.bs.modal', function (e) {
             
              window.history.back();
})
        break;
    case "#reviewModal":
       
        break;


                                                            
	}
});

// $("#find").click(function(){
//         show($('#rate').val());
//        }
//        );
// $("#modalReview").click(function(){
//         show($('#rate').val());
//         quickReview = true;
//        }
//        );

if($('#fromEmail').text() == 'a'){
   $('#emailModal').modal()

}
$('.facebookLogin').on("click",function(){
  facebookLogin();
})
$(window).hashchange();
$("#submitshowreview").on("click", submit_review); 
facebook();

autocomp();
setLoginModal();
$('.page-title').click(function(){
  window.location.href = ""
})
$('#signinbutton').click(function(){
  // console.log("signing in")
  signin()
})


$('.loginSidebar').click(function(){
        login_func_sidebar();
})




$('.writeReviewModal').click(function(){
  modalReview()
})

$('.WriteReviewMobile').click(function(){
  modalReview()
})


// trackScrolling();
// ads();
  //  $('.slickReviews').slick({
  //     slidesToShow: 2,
  // slidesToScroll: 1,
  // autoplay: false,
  // autoplaySpeed: 5000,
  // adaptiveHeight: true,
  // dots:true
  //   });
// $("#venues").on("click", show_venues);
// $("#NowPlaying").on( "click", show_nowPlaying);
// $("#panela").hide();
}

$(document).ready(start);
