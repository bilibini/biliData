<?php
include 'config.php';

function mydb_query($sql){
    include 'config.php';
    $conn = new mysqli($mysql_host, $mysql_user, $mysql_pw, $mysql_db,$mysql_port);
    if($conn->connect_error){
        return -1;
    }
    $conn->query("SET NAMES UTF8");
    $result=$conn->query($sql);
    $conn->close();
    return $result;
}

function mydb_insert($sql){
    include 'config.php';
    $conn = mysqli_connect($mysql_host, $mysql_user, $mysql_pw, $mysql_db,$mysql_port);
    if (!$conn) {
        die("连接失败: " . mysqli_connect_error());
    }
    return mysqli_query($conn, $sql);
}

?>