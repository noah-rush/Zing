<?php
if( isset($_POST['name']) && isset($_POST['hidden']) && $_POST['hidden'] == '' )
{
	/////////////////////////////////////////
	/////////////////////////////////////////
	$to = 'your_email_goes_here@demo.com';///
	/////////////////////////////////////////
	/////////////////////////////////////////
	
	$subject = $_POST['subject'];
	$headers = 'From: ' . $_POST['name'] . '<' . $_POST['email'] . '>' . "\r\n" . 'Reply-To: ' . $_POST['email'];	
	
	$message = 'Name: ' . $_POST['name'] . "\n" .
	           'E-mail: ' . $_POST['email'] . "\n" .
	           'Subject: ' . $_POST['subject'] . "\n" .
	           'Message: ' . $_POST['message'];
	
	mail($to, $subject, $message, $headers);
}
?>