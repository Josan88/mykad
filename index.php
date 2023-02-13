<html>
<img src="photo.jpg">
<br><br>
<?php
// read a json file
$json = file_get_contents('jpn1.json');
// decode the json
$json_data = json_decode($json, true);
// print the data
echo "<br>";
echo $json_data['name'];
echo "<br>";
echo $json_data['ic'];
echo "<br>";
echo $json_data['sex'];
echo "<br>";
echo $json_data['oldic'];
echo "<br>";
echo $json_data['dob'];
echo "<br>";
echo $json_data['stateofbirth'];
echo "<br>";
echo $json_data['validitydate'];
echo "<br>";
echo $json_data['nationality'];
echo "<br>";
echo $json_data['ethnicrace'];
echo "<br>";
echo $json_data['religion'];
echo "<br>";
$json = file_get_contents('jpn4.json');
$json_data = json_decode($json, true);
echo $json_data['line1'];
echo "<br>";
echo $json_data['line2'];
echo "<br>";
echo $json_data['line3'];
echo "<br>";
echo $json_data['postcode'];
echo "<br>";
echo $json_data['line5'];
echo "<br>";
echo $json_data['line6'];
echo "<br>";
echo $json_data['line7'];




?>

</html>