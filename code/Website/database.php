<?php
$mysqli = new mysqli('3.145.215.29', 'xhy', 'root', 'trashbin');

if($mysqli->connect_errno) {
	printf("Connection Failed: %s\n", $mysqli->connect_error);
	exit;
}
?>