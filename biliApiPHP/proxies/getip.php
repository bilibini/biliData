<?php
$filename=dirname(__FILE__)."/ip/".date("Y-m-d").".txt";
if(!file_exists($filename)){
    die("");
}
$file=fopen($filename,"r");
$contents = fread($file, filesize ($filename));
fclose($file);
echo $contents;
?>