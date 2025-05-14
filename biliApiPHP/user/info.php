<?php
include $_SERVER['DOCUMENT_ROOT'].'/mydb/conn.php';//导入数据库操作模块
include $_SERVER['DOCUMENT_ROOT'].'/http/get.php';//导入get操作模块

header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');

function get_sates($mid){//获取最近状态情况
    $movies=array();
    $sql="
SELECT video,videolike,follower,updaterate,avg_duration as duration,upsqldate FROM up 
WHERE mid = '{$mid}'
ORDER BY upsqldate DESC
LIMIT 10;";
    $result=mydb_query($sql);
    while($row = $result->fetch_assoc()) {
        array_push($movies,$row);

    }
    return $movies;
    /*数据结构:
    {
        'bangumi':0.5969,
        'cinema':0.5969,
        'bangumiandcinema':0.5969,
        'avg_bangumi':0.5969,
        'avg_cinema':0.5969
    }
    */
}
function get_vlist($mid){//获取最近更新视频
    $errnum=0;
    $url='http://api.bilibili.com/x/space/wbi/arc/search?pn=1&ps=6&order=pubdate&tid=0&mid='.$mid;
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
    if($data['code']==0){
        $response=[];
        $response=$data['data']['list']['vlist'];
    }
    return $response;
}

function get_info($mid){
    $errnum=0;
    $url='http://api.bilibili.com/x/web-interface/card?mid='.$mid;
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
    if($data['code']==0){
        $response=[];
        $data=$data['data'];
        $card=$data['card'];
        $response=[
            'face'=>$card['face'],
            'name'=>$card['name'],
            'sex'=>$card['sex'],
            'sign'=>$card['sign'],
            'fans'=>$card['fans'],
            'friend'=>$card['friend'],
            'like_num'=>$data['like_num']
        ];
    }
    return $response;
}

$uid=$_REQUEST['uid'];
$info=[
    'sates'=>get_sates($uid),
    'vlist'=>get_vlist($uid),
];
$info=$info+get_info($uid);

exit(json_encode($info));

?>