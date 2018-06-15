<?php

header("Access-Control-Allow-Origin: *");

$dsn = 'mysql:dbname=bnrank;host=db;port=3306';
$user = 'root';
$password = 'linkidrank233';

$addr = $_GET["address"];

try {

	$conn = new PDO($dsn, $user, $password);
	$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	$sth = $conn->prepare("SELECT * from shuihuinvite where inviteaddress = :ivaddr");
    $sth->bindValue(':ivaddr', $addr, PDO::PARAM_STR);
	$sth->execute();
	$result = $sth->fetchAll(PDO::FETCH_ASSOC);
	$json = json_encode($result);
	print_r($json);

} catch (PDOException $e) {
	echo $e->getMessage();
}

?>