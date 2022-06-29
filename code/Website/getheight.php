<?php
require 'sqlfunction.php';

header("Content-Type: application/json"); // Since we are sending a JSON response here (not an HTML document), set the MIME Type to application/json


$json_str = file_get_contents('php://input');
//This will store the data into an associative array
$json_obj = json_decode($json_str, true);

//Variables can be accessed as such:
$id = $json_obj['id'];

$res=user::getHeightById($id);

echo json_encode(array(
    "height" => $res
));
exit;

?>