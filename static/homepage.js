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
function profile(){
	$.ajax({
  		url: "/nowPlaying",
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
      
    } else {
      // The person is not logged into Facebook, so we're not sure if
      // they are logged into this app or not.
      

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
        var check = $("#panelheaderuser");
        check.html("<div class=\"dropdown\"><button class=\"btn btn-default btn-sm dropdown-toggle\"  type=\"button\" data-toggle=\"dropdown\">\<span class =\"glyphicon glyphicon-user\"></span><span id = \"user\" >  {{useron}}</span>\<span class=\"caret\"></span>\</button><ul class=\"dropdown-menu\" role=\"menu\">\<li><a href=\"#\">Profile</a></li>\ <li><a href=\"#\">Account Settings</a></li>\  <li><a href=\"#logout\">Logout</a></li>\ </ul>\</div>");
        var name = response.first_name;
        console.log(response.first_name);
        name = response.first_name;
        console.log(user);
          $("#user").text(" " + response.first_name + " ");
        $.ajax({
  		url: "/login",
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

function handle_login(data){
	console.log(data);
}
function displaynowplaying(data){
	
	$("#panelc2").html(data);
}
function displaycomingsoon(data){
	
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
	
  var lastname = $("#newlast").val();
	var firstname = $("#newfirst").val();
	var email = $("#newemail").val();
	var password = $("#newpassword").val();
	console.log(lastname, firstname, email, password);
	 $.ajax({
		url: "/facebookcreate",
		data: {
			email:  email,
			firstname: firstname,
			lastname: lastname,
			password: password
		},
		success: show_password
	});
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
		
	});
}

function login_func(){
	$.ajax({
		success: login_display,
  		url: "/signinform",
		
	});
}
function login_display(data){
	$("#panelc").find('.panel-body').html(data);
}

// function create_Account(){
// 	console.log("got here")
// 	var day = $("#day").val();
// 	var year = $("#year").val();
// 	console.log(year);
// 	console.log(day);
// 	var firstname = $("#first").val();
// 	var lastname = $("#last").val();
// 	var password = $("#password").val();
// 	var passConfirm = $("#confPassword").val();
// 	var email = $("#email").val();
// 	var month = $("#month").val();
// 	$.ajax({
// 		success: show_signup,
//   		url: "/usercreate",
// 		data: {
// 			firstname: firstname,
// 			lastname: lastname,
// 			password: password,
// 			passwordConfirm: passConfirm,
// 			email: email,
// 			month: month,
// 			day: day,
// 			year: year
// 		}
// 	});
// }

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
	$("#panelc").find('.panel-body').html(data);
	 var initRating = $("#startRating").text();
 $(".total-star-rating i").css("width", initRating +"%");
};
function display_venue(data){
	$("#panelc").find('.panel-body').html(data);
	var address = $("#address").text();
	console.log(address)
	var urlsearch = 'https://maps.googleapis.com/maps/api/geocode/json?address=' +address + '&key=AIzaSyAIlo8iZZm7IfAlLbbqPV42jeGHxanPgyg'
	  $.ajax({
  	url: urlsearch,
  	success: initialize
  })

}

var map
 function initialize(data) {
    var map_canvas = document.getElementById('map_canvas');
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
    title: $("#showname").text()
});
   var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 style = "font-size: 14pt" id="firstHeading" class="firstHeading">' +$("#showname").text() + '</h1>'+
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

	for(i=0; i<data.length; i++){
		data[i];
		console.log(data[i]);
		var myLatlng = new google.maps.LatLng(data[i][1],data[i][2]);
	var marker = new google.maps.Marker({
    position: myLatlng,
    map: map,
    title:data[i][0]
});
	var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 style = "font-size: 14pt" id="firstHeading" class="firstHeading">' +data[i][0] + '</h1>'+
      '<div id="bodyContent">'+
      '</div>'+
      '</div>';

  var infowindow = new google.maps.InfoWindow({
      content: contentString
  });
   google.maps.event.addListener(marker, 'click', function() {
    infowindow.open(map,marker);
  });
	marker.setMap(map);
}
}


function show(data){
	$.ajax({
		url: '/show',
		data: {
			show: data
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
		success: display_venue
	})
};
function show_reviews(){
	$("#writeuserreview").show();
	$("#submitreview").show();
	
}


function display_nowPlaying(data){
	
	$("#venuel").html(data);
};
function facebookLogin(){
	 FB.login(function(response) {
   console.log(response);
   console.log(response.email);
FB.api('/me', function(response) {
	name = response.first_name;
      $.ajax({
   		success: show_password,
		url: "/facebookcreateform",
		data: {
			email:  response.email,
			firstname: response.first_name,
			lastname: response.last_name
		}
	});
  })
  
 }, {scope: 'public_profile,email'});
}
function home(){
	$.ajax({
		success: show_container,
		url:"/home"
	})
}


function show_container(data){
	$("#panelc").find('.panel-body').html(data);
}

function show_password(data){
	$("#panelc").find('.panel-body').html(data);
	if(data.indexOf("placeholder=\"Password\"")==-1){
		  var check = $("#panelheaderuser");
        check.html("<div class=\"dropdown\"><button class=\"btn btn-default btn-sm dropdown-toggle\"  type=\"button\" data-toggle=\"dropdown\">\<span class =\"glyphicon glyphicon-user\"></span><span id = \"user\" >  {{useron}}</span>\<span class=\"caret\"></span>\</button><ul class=\"dropdown-menu\" role=\"menu\">\<li><a href=\"#\">Profile</a></li>\ <li><a href=\"#\">Account Settings</a></li>\  <li><a href=\"#logout\">Logout</a></li>\ </ul>\</div>");
        
          $("#user").text(" " + name + " ");
	}
}
var name
function fbsignup(){
	var lastname = $("#lastname").text();
	var firstname = $("#firstname").text();
	var email = $("#fbemail").val();
	var password = $("#fbpassword").val();
	console.log(lastname, firstname, email, password)

	 $.ajax({
		url: "/facebookcreate",
		data: {
			email:  email,
			firstname: firstname,
			lastname: lastname,
			password: password
		},
		success: show_password
	});
}


function submit_review(){


	var text = $("#writeuserreview").val();
	var show = $("#showname").text();
	console.log(text);
	console.log(stars);

}



function signin(){
	var email = $("#loginEmail").val();
	var password = $("#loginPassword").val();
	$.ajax({
		url:"/signin",
		data:
		{email:email,
		password:password
		},
		success: show_password
	})
}



function start (){
	getnowplaying();
	getcomingsoon();
	home();
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
	if(hash.substring(0,6) == "#venue")
	{
		console.log(hash.substring(7));
		venue(hash.substring(7));
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
	case "#fbsignup":
		fbsignup();
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
		home()
		break;
	case "#profile":
		profile()
		break;
	case "#submitreview":
		submit_review()
		break;



	}

});


$(":radio").change(
  function(){
	stars = this.value
  } 
);
$('.good').click(function(){
    if($(this).is(':checked')){
        $(this).css("color",  "green");
    } 
});
var lastchecked = $("#toprated");
$("input[name='dio']").change(function() {
	$("input[name='dio']").each(function(){
    if(this.checked) {
    lastchecked.checked = false
	console.log($("input[name='dio']:checked").val());
	 $("#leftBoxTitle").text($("input[name='dio']:checked").val());
	var but = $( "input[name='dio']:checked").closest("label");
	but.css("background-color", "red");
	lastchecked.css("background-color", "#e06666");
	lastchecked = but;
	// console.log($( "input[name='dio']:checked").closest("label"))
        // do something when selected
    } else {
    	
    
        
    }
	
	

})
});


$('#popover').popover({ trigger: "hover" });
$(window).hashchange();
 $("#submitshowreview").on("click", submit_review);
$("#good").find(".checkboxFive label::after").css("border: 1px solid green");
 console.log('here');
  facebook();

// $("#venues").on("click", show_venues);
// $("#NowPlaying").on( "click", show_nowPlaying);
}
$(document).ready(start);
