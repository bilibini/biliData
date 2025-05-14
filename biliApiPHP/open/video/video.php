<?php
include $_SERVER['DOCUMENT_ROOT'].'/http/get.php';//导入get操作模块
header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');


$aid=null;
$bvid=null;

$errnum=0;

if(isset($_REQUEST['aid'])||isset($_REQUEST['bvid'])){
    if(isset($_REQUEST['aid'])){
        $aid=$_REQUEST['aid'];
    }
    if(isset($_REQUEST['bvid'])){
        $bvid=$_REQUEST['bvid'];
    }
}else{
    http_response_code(400);
    exit(json_encode(['message'=>'不能为空']));
}

$url='http://api.bilibili.com/x/web-interface/view?';
if(isset($aid)){
    $url=$url.'aid='.$aid;
    if(isset($bvid)){
        $url=$url.'&bvid='.$bvid;
    }
}else{
    $url=$url.'bvid='.$bvid;
}

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

exit($response);
?>