function do_stuff() {
	var hiddenBox = $("#blank" );
	var login = $("#submit");
	login.hide();
	var hiddenBox = $("#blank" );
  hiddenBox.hide();

}
function signup(){
	//$("#panelsignup").show();
	console.log("signup");
	$.ajax({
		success: show_signup,
		url: "/signupform"
	})
}
function signin(){
	//$("#panelsignup").show();
	console.log("signin");
	$.ajax({
		success: show_signin,
		url: "/signinform"
	})
}
function autocomp(){
	
	$('#query').autocomplete({serviceUrl: '/autocomplete/allshows'});
}; 

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
		autocomp();
		//panelMove();
}
function show_signin(data){
		$("#jumbo").html(data);
		//panelMove();
}
function login_rout(data){
	console.log(data);
	var str = data.substring(0,3);
	var somethingwrong = $("#somethingWrong")
	console.log(data)
	switch(str){
		case "Log":
			window.location.href = "/";
			break;
		case "Use":
			somethingwrong.show();
			alert("Username not found. Try again.");
			setTimeout(function(){window.location.href = "/#signin"},3000);
			break;
		case "Inc":
			somethingwrong.show();
			alert("Incorrect Password. Try again.");
			setTimeout(function(){window.location.href = "/#signin"},3000);
			break;
		}
}


function login_func(){
	var user = $("#loginUsername").val();
	var password = $("#loginPassword").val();
	console.log(user);
	console.log(password);
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
	case "#signin":
		signin();
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

