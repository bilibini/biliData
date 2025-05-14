<?php
include $_SERVER['DOCUMENT_ROOT'].'/http/get.php';//导入get操作模块
header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');

$uid=$_REQUEST['uid'];

$errnum=0;
$url='http://api.bilibili.com/x/space/acc/info?mid='.$uid;
$response = httpGet($url);
$data = json_decode($response, true);

while($data['code']==-401){
    $errnum=$errnum+1;
    $response = httpGet($url);
    $data = json_decode($response, true);
    if($errnum>3){
        break;
    }
}

print_r($response);
?>