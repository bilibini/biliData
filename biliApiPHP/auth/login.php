<?php
include $_SERVER['DOCUMENT_ROOT'].'/mydb/conn.php';//导入数据库操作模块
header("Access-Control-Allow-Origin: *");
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept');
header('Content-Type:application/json; charset=utf-8');

if (strtoupper($_SERVER['REQUEST_METHOD']) == 'OPTIONS') {
    exit;
}

$response=array(
    'code'=>'200',
    'data'=>[]
);
$username='';
$password='';
if(isset($_REQUEST['username'])&&isset($_REQUEST['password'])){
    $username=$_REQUEST['username'];
    $password=$_REQUEST['password'];
}else{
    $response['code']="400";
    $response['data']['message']="没有获取到内容,参数错误";
    http_response_code(400);
    exit(json_encode($response));
}
if((strpos($username, ' ') !== false)||strlen($username)<3||strlen($username)>10){
    $response['code']="400";
    $response['data']['message']="参数错误";
    http_response_code(400);
    exit(json_encode($response));
}
if((strpos($password, ' ') !== false)||strlen($password)!=32){
    $response['code']="400";
    $response['data']['message']="参数错误";
    http_response_code(400);
    exit(json_encode($response));
}

$password=md5($password.'$qwq$');
$sql_str="SELECT id,username,role as rank,mid,token 
FROM login WHERE username='".$username."' and password='".$password."' ;";

$result=mydb_query($sql_str);
$data=$result->fetch_assoc();
if(!$data){
    $response['code']="401";
    $response['data']['message']="账号或密码错误!";
    http_response_code(401);
    exit(json_encode($response));
}
$response['code']="200";
$response['data']=$data;
$response['data']['message']="登录成功欢迎回来~";
http_response_code(200);
exit(json_encode($response));




?>