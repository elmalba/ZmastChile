<?php

if($_POST){

    $name = $_POST['name'];

    $email = $_POST['email'];

    $message = nl2br($_POST['text']);

	
	// To send HTML mail
	$to = "wedothewebs@gmail.com";

	// subject

	$subject = 'From Cube+';

	// To send HTML mail, the Content-type header must be set

	$headers  = 'MIME-Version: 1.0' . "\r\n";

	$headers .= 'Content-type: text/html; charset=iso-8859-1' . "\r\n";

	

	// Additional headers
	$headers .= 'From: '.$name.' <'.$email.'>' . "\r\n";

	// Mail it
  	mail($to, $subject, $message, $headers);

}

?>