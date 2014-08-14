var stars

function getnowplaying(){
	$.ajax({
  		url: "/nowPlaying",
		success: displaynowplaying
	});

}
function getcomingsoon(){
	$.ajax({
  		url: "/comingsoon",
		success: displaycomingsoon
	});

}
function facebook(){
	 function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI();
    } else if (response.status === 'not_authorized') {
      // The person is logged into Facebook, but not your app.
      document.getElementById('status').innerHTML = 'Sign up using Facebook';
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into Facebook.';

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
    statusChangeCallback(response);
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
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
    console.log(JSON.stringify(response));
      document.getElementById('status').innerHTML =
        'Thanks for logging in, ' + response.name + '!';
        var modal = $('#signupModal');
        modal.modal('hide');
        var check = $("#user");
        check.text(response.first_name);
        check.show();

    });
  }
}

function displaynowplaying(data){
	console.log(data);
	$("#panelc2").html(data);
}
function displaycomingsoon(data){
	console.log(data);
	$("#panelc3").html(data);
}



function do_stuff() {
	var hiddenBox = $("#blank" );
	var login = $("#submit");
	login.hide();
	var hiddenBox = $("#blank" );
  hiddenBox.hide();

}
function signup(){
	//$("#panelsignup").show();
	  facebook();

  
}

function panelMove() {
var panel = $("#panelsignup");
console.log(panel.css("height"));
var px = panel.css("height").indexOf('p')
var number = parseInt(panel.css("height").substring(0, px));
number = number +4;
panel.css("height", number + "px"); // pseudo-property code: Move right by 10px
setTimeout(panelMove,10); // call doMove() in 20 msec
}

function printmonth(){
		console.log("anything")
		//panelMove();
}

function show_signup(data){
		$("#jumbo").html(data);
		//panelMove();
}
function login_rout(data){
	console.log(data);
	var str = data.substring(0,3);
	var somethingwrong = $("#somethingWrong")
	switch(str){
		case "Log":
			var user = data.substring(18);
			console.log(user);
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
			window.location.href = "/";
			break;
		case "Inc":
			somethingwrong.show();
			somethingwrong.text("Incorrect Password. Try again.");
			window.location.href = "/";
			break;
		}
}


function login_func(){
	var user = $("#username").val();
	var password = $("#password").val();
	console.log(user)
	console.log(password)
	$.ajax({
		success: login_rout,
  		url: "/loggedin",
		data: {
			username: user,
			password: password
		}
	});
}

function create_Account(){
	console.log("got here")
	var day = $("#day").val();
	var year = $("#year").val();
	console.log(year);
	console.log(day);
	var firstname = $("#first").val();
	var lastname = $("#last").val();
	var password = $("#password").val();
	var passConfirm = $("#confPassword").val();
	var email = $("#email").val();
	var month = $("#month").val();
	$.ajax({
		success: show_signup,
  		url: "/usercreate",
		data: {
			firstname: firstname,
			lastname: lastname,
			password: password,
			passwordConfirm: passConfirm,
			email: email,
			month: month,
			day: day,
			year: year
		}
	});
}

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

function show_reviews(){
	$("#writeuserreview").show();
}

function display_venues(data){
	console.log(data);
	$("#panelc").html(data);
	var iURL = "http://ajax.googleapis.com/ajax/services/search/images";
    $.ajax({
        url: iURL,
        type: 'GET',
        dataType: 'jsonp',
        data: {
            v:  '1.0',
            q:  '',
            format: 'json',
            jsoncallback:  '?'
        },
        success: function(data){
        	json.responseData.results[0].unescapedUrl
            console.log(data);
        },
        error: function(xhr, textStatus, error){
            console.log(xhr.statusText, textStatus, error);
        }
        
    });

};
function display_show(data){
	console.log(data);
	$("#panelc").find('.panel-body').html(data);
	 var initRating = $("#startRating").text();
 $(".total-star-rating i").css("width", initRating +"%");
};
function show(data){
	$.ajax({
		url: '/show',
		data: {
			show: data
		},
		success: display_show
	})
};
function show_reviews(){
	$("#writeuserreview").show();
	$("#submitreview").show();
	
}


function display_nowPlaying(data){
	console.log(data);
	$("#venuel").html(data);
};

function submit_review(){


	var text = $("#writeuserreview").val();
	var show = $("#showname").text();
	console.log(text);
	console.log(stars);
	$.ajax({
		url: "/submitrating",
		data: {
			show:  show,
			rating: stars
		}
	})
	$.ajax({
		success: reload,
		url: "/submitreview",
		data: {
			show:  show,
			review: text
		}
	})

}


function start (){
	getnowplaying();
	getcomingsoon();
var check = $("#user").text();
	if(check == "none")
	{
	    
} else {

	
};

$(window).hashchange( function test(){
	var hash = location.hash;
	if(hash.substring(0,5) == "#show")
	{
		console.log(hash.substring(6));
		show(hash.substring(6));
	}
	console.log(hash);
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
	case "#signup":
		signup();
		break;
	case "#createAccount":
		create_Account();
		break;


	}

});


$(":radio").change(
  function(){
	stars = this.value
  } 
)
$('.good').click(function(){
    if($(this).is(':checked')){
        $(this).css("color",  "green");
    } 
});

$(window).hashchange();
 $("#writebutton").on("click", show_reviews);
  $("#months").on("click", printmonth);

 $("#submitreview").on("click", submit_review);
$("#good").find(".checkboxFive label::after").css("border: 1px solid green");
 console.log('here');
  facebook()
// $("#venues").on("click", show_venues);
// $("#NowPlaying").on( "click", show_nowPlaying);
}
$(document).ready(start);
