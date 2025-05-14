<?php
include $_SERVER['DOCUMENT_ROOT'].'/mydb/conn.php';//导入数据库操作模块
header("Access-Control-Allow-Origin: *");
header('Content-Type:application/json; charset=utf-8');

function get_sqlinfo(){//获取数据库情况
    $movies=array();
    $sql="
    SELECT (SELECT COUNT(v.aid) FROM video v) as video,(SELECT COUNT(u.mid) FROM up u) as up,(SELECT COUNT(user.mid) FROM user) as user;
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

function get_userinfo(){//获取数据库情况
    $userinfo_num_list=array();
    $result=mydb_query("SELECT id,username,role,mid FROM login;");
    while($row = $result->fetch_assoc()) {
        array_push($userinfo_num_list,$row);
    }
    return $userinfo_num_list;
    /*数据结构:
    [{'sex':'保密','num':22},{'sex':'女','num':16}...]
    */
}

$data=[
    'userinfo'=>get_userinfo(),
    'sqlinfo'=>get_sqlinfo()
];
exit(json_encode($data));

?>