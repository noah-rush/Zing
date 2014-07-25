function do_stuff() {
	var hiddenBox = $("#blank" );
	var login = $("#submit");
	login.hide();
	var hiddenBox = $("#blank" );
  hiddenBox.hide();

}


function show_venues(){
	$.ajax({
  		url: "/venues",
		success: display_venues
	});
}

function display_venues(data){
	console.log(data);
	$("#venuelist").html(data);
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
	var logout = $("#logout")
	var name = $("#name");
	var yesuser = $("#yesuser")
	yesuser.show();
	name.show();
	logout.show();
	
}

$( "#venues").on( "click",  show_venues)
}
$(document).ready(start);