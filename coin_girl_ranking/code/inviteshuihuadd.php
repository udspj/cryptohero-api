<?php

header("Access-Control-Allow-Origin: *");

$dsn = 'mysql:dbname=bnrank;host=db;port=3306';
$user = 'root';
$password = 'linkidrank233';

$addr = $_POST['address'];// 被邀请人（即打开链接的用户自己）
$ivaddr = $_POST['inviteaddress'];// 邀请人
$cardnum = intval($_POST['cardnum']);
$price = floatval($_POST['price']);

try {

  if (!empty($addr) and !empty($ivaddr) and !empty($cardnum) and !empty($price)) {
    $conn = new PDO($dsn, $user, $password);
    $datetime = date('Y-m-d H:i:s');
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $allprice = $price*$cardnum;
    $allr = $price*$cardnum*0.03;

    $stmt = $conn->prepare("insert ignore into shuihuinvite (address, inviteaddress, paid, cardcount, rebate, time) VALUES (:addr, :ivaddr, :price, :cardnum, :r, '$datetime')");
    $stmt->bindParam(':addr', $_POST['address'], PDO::PARAM_STR);
    $stmt->bindParam(':ivaddr', $_POST['inviteaddress'], PDO::PARAM_STR);
    $stmt->bindParam(':price', $allprice, PDO::PARAM_STR);
    $stmt->bindParam(':cardnum', $_POST['cardnum'], PDO::PARAM_STR);
    $stmt->bindParam(':r', $allr, PDO::PARAM_STR);
    $stmt->execute();
  }

} catch (PDOException $e) {
  echo $e->getMessage();
}

?>