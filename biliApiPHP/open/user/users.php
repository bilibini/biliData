<?php
include $_SERVER['DOCUMENT_ROOT'].'/mydb/conn.php';//导入数据库操作模块
header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');

$level=array();//等级分布
$sex=array();//性别分布
$vip=array();//vip分布
$movies=array();//追剧情况

$unsign=0.0;//没有签名比例
$silence=0.0;//被封比例
$fans_badge=0.0;//有粉丝勋章比例
$up=0.0;//up主比例
$following=0.0;//关注数平均值
$follower=0.0;//粉丝数平均值
$video=0.0;//投稿视频平均值
$favourite=0.0;//收藏夹平均值


function get_unsign(){//获取没有签名人数比例
    $result=mydb_query("SELECT COUNT(*)/(SELECT COUNT(*) FROM user) as unsign FROM user WHERE sign='';");
    while($row = $result->fetch_assoc()) {
        $unsign=$row["unsign"];
    }
    return $unsign;
    //数据结构：0.6932
}
function get_silence(){//获取被封禁人数比例
    $result=mydb_query("SELECT COUNT(*)/(SELECT COUNT(*) FROM user) as silence FROM user WHERE silence=1;");
    while($row = $result->fetch_assoc()) {
        $silence=$row["silence"];
    }
    return $silence;
    //数据结构：0.0051
}

function get_fans_badge(){//获取拥有粉丝勋章人数比例
    $result=mydb_query("SELECT COUNT(*)/(SELECT COUNT(*) FROM user) AS fans_badge FROM user WHERE fans_badge=1;");
    while($row = $result->fetch_assoc()) {
        $fans_badge=$row["fans_badge"];
    }
    return $fans_badge;
    //数据结构：0.0051
}
function get_up(){//获取up人数比例
    $result=mydb_query("SELECT COUNT(*)/(SELECT COUNT(*) FROM user) as up FROM user WHERE video>0;");
    while($row = $result->fetch_assoc()) {
        $up=$row["up"];
    }
    return $up;
    //数据结构：0.51
}

function get_vip(){//获取VIP分布情况
    /*
1：月度大会员
3：年度大会员
7：十年大会员
15：百年大会员
    */
    $vip_num_list=array();
    $result=mydb_query("SELECT vip as name,COUNT(*)*100/(SELECT COUNT(*) FROM user) as value FROM user GROUP BY vip;");
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
    $result=mydb_query("SELECT concat(level,'级') as name,COUNT(*)*100/(SELECT COUNT(*) FROM user) as value FROM user GROUP BY level;");
    while($row = $result->fetch_assoc()) {
        array_push($level_num_list,$row);
    }
    return $level_num_list;
    /*数据结构:
    [{'level':1,'num':22},{'level':2,'num':16}...]
    */
}
function get_sex(){//获取性别分布情况
    $level_num_list=array();
    $result=mydb_query("SELECT sex as name,COUNT(*)*100/(SELECT COUNT(*) FROM user) as value FROM user GROUP BY sex;");
    while($row = $result->fetch_assoc()) {
        array_push($level_num_list,$row);
    }
    return $level_num_list;
    /*数据结构:
    [{'sex':'保密','num':22},{'sex':'女','num':16}...]
    */
}
function get_movies(){//获取追番情况
    $movies=array();
    $sql="
SELECT 
(SELECT COUNT(*)/b.countnu FROM user WHERE bangumi>0) as bangumi ,
(SELECT COUNT(*)/b.countnu FROM user WHERE cinema>0) as cinema,
(SELECT COUNT(*)/b.countnu FROM user WHERE cinema>0 AND bangumi>0) as bangumiandcinema,
AVG(a.bangumi) as avg_bangumi,
AVG(a.cinema) as avg_cinema
FROM user a JOIN (SELECT COUNT(*) as countnu FROM user) b;
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
function get_scale(){//获取所有用户相关数据
    $scale=array();
    $sql="
SELECT 
(SELECT COUNT(*)/b.countnu FROM user WHERE sign='') as unsign ,
(SELECT COUNT(*)/b.countnu FROM user WHERE silence=1) as silence,
(SELECT COUNT(*)/b.countnu FROM user WHERE fans_badge=1) as fans_badge,
(SELECT COUNT(*)/b.countnu FROM user WHERE video>0) as up,
AVG(a.following) as following,
AVG(a.follower) as follower,
AVG(a.video) as video,
AVG(a.favourite) as favourite
FROM user a JOIN (SELECT COUNT(*) as countnu FROM user) b;
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
$movies=get_movies();

$data=[
    'level'=>$level,
    'sex'=>$sex,
    'vip'=>$vip,
    'movies'=>$movies,
];
$data=$data+get_scale();

exit(json_encode($data));


?>