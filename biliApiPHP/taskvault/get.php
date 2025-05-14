<?php
include $_SERVER['DOCUMENT_ROOT'].'/mydb/conn.php';//导入数据库操作模块
header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');

$type=$_REQUEST['type'];
$num=$_REQUEST['num'];

if(!$type){
    die("null");
}
if(!$num){
    $num=1;
}



print_r($type);
print_r($num);

?>