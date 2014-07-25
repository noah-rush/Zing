function do_stuff() {
	var hiddenBox = $("#blank" );
	var login = $("#submit");
	login.hide();
	var hiddenBox = $("#blank" );
  hiddenBox.hide();

}
function signup(){
	$("#panelsignup").show();
	console.log("signup");
	$.ajax({
		success: show_signup,
		url: "/signupform"
	})
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
		$("#panelsignup").html(data);
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
	$("#venuel").html(data);
}

function display_nowPlaying(data){
	console.log(data);
	$("#venuel").html(data);
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
		alert();
		break;
	case "#login":
		login_func()
		break;
	case "#signup":
		signup();
		break;

	}

});




$(window).hashchange();
 $("#writebutton").on("click", show_reviews);
  $("#months").on("click", printmonth);
// $("#venues").on("click", show_venues);
// $("#NowPlaying").on( "click", show_nowPlaying);
}
$(document).ready(start);