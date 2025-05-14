<?php
include $_SERVER['DOCUMENT_ROOT'].'/mydb/conn.php';//导入数据库操作模块
header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');

$level=array();//等级分布
$sex=array();//性别分布
$vip=array();//vip分布
$movies=array();//追剧情况

// $unsign=0.0;//没有签名比例
// $silence=0.0;//被封比例
// $fans_badge=0.0;//有粉丝勋章比例
// $up=0.0;//up主比例
$following=0.0;//关注数平均值
$follower=0.0;//粉丝数平均值
$video=0.0;//投稿视频平均值
// $favourite=0.0;//收藏夹平均值


function get_vip(){//获取VIP分布情况
    /*
1：月度大会员
3：年度大会员
7：十年大会员
15：百年大会员
    */
    $vip_num_list=array();
    $sql_str="SELECT vip as name,
    COUNT(*)*100/(SELECT COUNT(*) FROM view_ups_group) as value 
    FROM view_ups_group GROUP BY vip;";
    $result=mydb_query($sql_str);
    while($row = $result->fetch_assoc()) {
        array_push($vip_num_list,$row);
    }
    return $vip_num_list;
    /*数据结构:
    [{'vip':0,'num':220},{'vip':2,'num':16}...]
    */
}
function get_level(){//获取等级分布情况
    $level_num_list=array();
    $result=mydb_query("SELECT concat(level,'级') as name,COUNT(*)*100/(SELECT COUNT(*) FROM view_ups_group) as value FROM view_ups_group GROUP BY level;");
    while($row = $result->fetch_assoc()) {
        array_push($level_num_list,$row);
    }
    return $level_num_list;
    /*数据结构:
    [{'level':1,'num':22},{'level':2,'num':16}...]
    */
}
function get_sex(){//获取性别分布情况
    $sex_num_list=array();
    $result=mydb_query("SELECT sex as name,COUNT(*)*100/(SELECT COUNT(*) FROM view_ups_group) as value FROM view_ups_group GROUP BY sex;");
    while($row = $result->fetch_assoc()) {
        array_push($sex_num_list,$row);
    }
    return $sex_num_list;
    /*数据结构:
    [{'sex':'保密','num':22},{'sex':'女','num':16}...]
    */
}

function get_movies(){//获取追番情况
    $movies=array();
    $sql="
SELECT 
(SELECT COUNT(*)/b.countnu FROM view_ups_group WHERE bangumi>0) as bangumi ,
(SELECT COUNT(*)/b.countnu FROM view_ups_group WHERE cinema>0) as cinema,
(SELECT COUNT(*)/b.countnu FROM view_ups_group WHERE cinema>0 AND bangumi>0) as bangumiandcinema,
AVG(a.bangumi) as avg_bangumi,
AVG(a.cinema) as avg_cinema
FROM view_ups_group a JOIN (SELECT COUNT(*) as countnu FROM view_ups_group) b;
    ";
    $result=mydb_query($sql);
    while($row = $result->fetch_assoc()) {
        $movies=$row;
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

function get_scale(){//获取所有up主相关数据
    $scale=array();
    $sql="
SELECT 
AVG(a.following) as following,
AVG(a.follower) as follower,
AVG(a.video) as video,
AVG(a.videolike) as videolike,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE bangumi>0) as bangumi ,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE cinema>0) as cinema,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE cinema>0 AND bangumi>0) as bangumiandcinema,
AVG(a.bangumi) as avg_bangumi,
AVG(a.cinema) as avg_cinema,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE is_senior_member=1) as senior_member
FROM view_ups_group a,(SELECT COUNT(mid) as countnu FROM view_ups_group) b;
    ";
    $sql="
SELECT 
AVG(a.following) as following,
AVG(a.follower) as follower,
AVG(a.video) as video,
AVG(a.videolike) as videolike,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE bangumi>0) as bangumi ,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE cinema>0) as cinema,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE cinema>0 AND bangumi>0) as bangumiandcinema,
AVG(a.bangumi) as avg_bangumi,
AVG(a.cinema) as avg_cinema,
AVG(a.updaterate) as updaterate,
AVG(a.avg_duration) as duration,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE is_senior_member=1) as senior_member,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE avg_duration>8) as longvideo,
(SELECT COUNT(mid)/b.countnu FROM view_ups_group WHERE official=0) as official
FROM view_ups_group a,(SELECT COUNT(mid) as countnu FROM view_ups_group) b
    ";
    $result=mydb_query($sql);
    while($row = $result->fetch_assoc()) {
        $scale=$row;
    }
    return $scale;
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




$level=get_level();
$sex=get_sex();
$vip=get_vip();

$data=[
    'level'=>$level,
    'sex'=>$sex,
    'vip'=>$vip,
];
$data=$data+get_scale();
exit(json_encode($data));


?>