<?php
include $_SERVER['DOCUMENT_ROOT'].'/mydb/conn.php';//导入数据库操作模块
header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');

$viewsql="
CREATE VIEW view_videos AS
select 
avg(b.duration) AS duration_avg,
avg(b.view) AS view_avg,
avg(b.danmaku) AS danmaku_avg,
avg(b.reply) AS reply_avg,
avg(b.favorite) AS favorite_avg,
avg(b.coin) AS coin_avg,
avg(b.share) AS share_avg,
avg(b.videolike) AS videolike_avg,
floor(avg(b.width)) AS width_avg,
floor(avg(b.height)) AS height_avg,
(select (count(*)/(select count(*) from view_videos_group)) from view_videos_group where (view_videos_group.width >= view_videos_group.height)) AS LandscapeVideo_scale,
(select (count(*)/(select count(*) from view_videos_group)) from view_videos_group where (view_videos_group.duration >= 480)) AS LongVideo_scale
from view_videos_group b
";

function get_videos(){//获取视频相关数据
    $result=mydb_query("SELECT * FROM view_videos;");
    while($row = $result->fetch_assoc()) {
        $unsign=$row;
    }
    return $unsign;
    // 返回数据：
    /*
    {   
        "duration_avg":"414.7143",
        "view_avg":"1873929.1429",
        "danmaku_avg":"7560.5714",
        "reply_avg":"2606.0000",
        "favorite_avg":"29612.0000",
        "coin_avg":"53757.1429",
        "share_avg":"4384.5714",
        "videolike_avg":"201568.8571",
        LandscapeVideo_scale: "0.9286",
        LongVideo_scale: "0.2857"
    }
    */
}
function get_videos_tname(){//获取视频类型比例
    $result=mydb_query("SELECT tname AS name,(COUNT(*)/(SELECT COUNT(*) FROM view_videos_group))*100 AS value FROM view_videos_group GROUP BY tname;");
    $videos_tname=array();
    while($row = $result->fetch_assoc()) {
        array_push($videos_tname,$row);
    }
    return $videos_tname;
    // 返回数据：
    /*
    [
    {
        "name": "单机游戏",
        "value": "35.7143"
    },
    {
        "name": "手机游戏",
        "value": "14.2857"
    },
    {
        "name": "搞笑",
        "value": "7.1429"
    },
    {
        "name": "预告·资讯",
        "value": "42.8571"
    }
    ]
    */
}

$videosData=get_videos();
// $tname=array("tnme"=>get_videos_tname());
// $videosData=$videosData+$tname;

exit(json_encode($videosData))

?>