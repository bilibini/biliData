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
$mid='';
$password='';
if(isset($_REQUEST['username'])&&isset($_REQUEST['password'])&&isset($_REQUEST['mid'])){
    $username=$_REQUEST['username'];
    $mid=$_REQUEST['mid'];
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

$result=mydb_query("SELECT id  FROM login WHERE username='".$username."' ;");
$data=$result->fetch_assoc();
if($data){
    $response['code']="400";
    $response['data']['message']="用户名已被使用";
    http_response_code(400);
    exit(json_encode($response));
}

$password=md5($password.'$qwq$');
$token=hash('sha256',$username.$password);
$token="QWQ".$token."END";
$sql_str="INSERT INTO `login` (`id`, `username`, `password`, `role`, `mid`, `token`) VALUES (NULL, '".$username."', '".$password."', '0', '".$mid."', '".$token."');";

$result=mydb_insert($sql_str);
if($result){
    $response['code']="200";
    $response['data']['message']="注册成功,欢迎你的加入";
    http_response_code(200);
    exit(json_encode($response));
}else{
    $response['code']="400";
    $response['data']['message']="注册失败";
    http_response_code(400);
    exit(json_encode($response));
}


?>