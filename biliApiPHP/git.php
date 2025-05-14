<?php

$server_info = array();

// 获取服务器操作系统
$server_info['OS'] = php_uname('s') . ' ' . php_uname('r'); 

// 获取Web服务器类型及版本号
$server_info['Web Server'] = $_SERVER['SERVER_SOFTWARE'];  

// 获取PHP版本号
$server_info['PHP Version'] = phpversion();  

// 获取MySQL版本号 
$server_info['MySQL Version'] = mysqli_get_server_info(mysqli_connect('localhost', 'root', 'password'));

// 获取主机名 
$server_info['Hostname'] = gethostname();  

// 显示服务器信息
foreach ($server_info as $key => $value) {
    echo $key . ': ' . $value . '<br>';
}

?>