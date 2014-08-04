var stars

function do_stuff() {
	var hiddenBox = $("#blank" );
	var login = $("#submit");
	login.hide();
	var hiddenBox = $("#blank" );
  hiddenBox.hide();

}

function getnowplaying(){
	$.ajax({
  		url: "/nowPlaying",
		success: displaynowplaying
	});

}


function displaynowplaying(data){
	console.log(data);
	$("#panelc2").html(data);
}






$(document).ready(start);

function login_rout(data){
	console.log(data);
	var str = data.substring(0,3);
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
	$("#submitreview").show();
	
}

function display_venues(data){
	console.log(data);
	$("#panelc").html(data);
}

function display_nowPlaying(data){
	console.log(data);
	$("#venuel").html(data);
}


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
function reload(){
	location.reload();
}




function start (){

var check = $("#variable").text();
	if(check == "none")
	{
		var login = $("#loginscreen");
		var nouser = $("#nouser");
		nouser.show();
		login.show();
	    
} else {
	var logout = $("#logout");
	var name = $("#name");
	var yesuser = $("#yesuser");
	yesuser.show();
	name.show();
	logout.show();
	
}

$(window).hashchange( function test(){
	var hash = location.hash;
	console.log(hash);
	show_venues;
	switch(hash){
	case "#venues":
		show_venues()
		break;
	case "#nowplaying":
		show_nowPlaying()
		break;
	case "#createEvent":
		break;
	case "#login":
		login_func()
		break;

	}

});


$(":radio").change(
  function(){
	stars = this.value
  } 
)

$(window).hashchange();
 $("#writebutton").on("click", show_reviews);
 $("#submitreview").on("click", submit_review);
 var initRating = $("#startRating").text();
 var yourInitRating = $("#yourRating").text();
 $(".total-star-rating i ").css("width", initRating +"%" );
 $(".star-rating i").css("border", yourInitRating + "%")

getnowplaying();
// $("#venues").on("click", show_venues);
// $("#NowPlaying").on( "click", show_nowPlaying);
}
$(document).ready(start);

