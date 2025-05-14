<?php
$filename=dirname(__FILE__)."/ip/".date("Y-m-d").".txt";
$contents = $_REQUEST['ips'];
if($contents=="" or empty($contents)){
    die("2333");
}else{
    $file=fopen($filename,"w+");
    fwrite($file, $contents);
    fclose($file);
    echo $contents;
}

?>