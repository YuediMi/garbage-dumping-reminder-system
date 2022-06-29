<?php
require 'database.php';
$id='1';
$stmt = $mysqli->prepare("SELECT time, iaq FROM trashinfo where trashid=? order by time desc LIMIT 10;");
if(!$stmt){
	printf("Query Prep Failed: %s\n", $mysqli->error);
	exit;
}
$stmt->bind_param('s',$id);
$stmt->execute();

// $stmt->bind_result($time, $iaq);
// $iaqaarray = array();
// while($stmt->fetch()){
//     $singleiaq = new static($time, $iaq);
//     printf("\t<li>%s\n",
//  		htmlspecialchars( $time ),
//  	);
//     // array_push($iaqaarray, $singleiaq);
// }

$result = $stmt->get_result();

echo "<ul>\n";
while($row = $result->fetch_assoc()){
	printf("\t<li>%s\n",
		htmlspecialchars( $row["time"] ),
	);
}
echo "</ul>\n";

$stmt->close();
?>