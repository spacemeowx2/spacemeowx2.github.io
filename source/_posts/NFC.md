---
title: NFC
date: 2016-05-06
categories: tech
tags: [nfc]
---

## 前言
上次SSCTF线下赛有一题是关于NFC的题, 毕竟线下赛  
提供了硬件(acr-122u), 一队3张卡, 提供一台机器给你刷卡, 扣除卡内余额..  
虽然答案很简单, 听说是CRC+MD5 (顺便开个坑, 比如用 <del>P'y't'hon</del> Python 自动识别校验码)  
<!--more-->

## 硬件准备
常用的破解硬件有 Proxmark3(很贵的样子), ACR-122U, PN532, 后面两者价格差不多, 都可以当玩具玩一玩, Proxmark3 这种神器还是以后再说吧= =  
然后我入了个ACR-122U    
(PS. 最近宿舍在回收洗衣卡是不是被谁破解了呢) 

## 软件准备
当时线下赛用的是NFC-GUI 1.5, 实际上就是libnfc的GUI  
实际上的M1卡都是有KEY加密的, 而比赛那天直接跳了这步, 实践中找KEY是最重要的一步  
M1卡中是有许多 sector 的, 每个 sector 都有自己的 key , 而 mfoc 快速爆出非全加密卡的所有key  
如果卡的所有 sector 都被加密了(比如咱们的学生证) 那么只能用 mfcuk 来爆破了  
这些软件 kali 里都有自带  
[参考资料](http://drops.wooyun.org/tips/2065)

## 一些经验
1. 供电要足  
2. Windows下不稳定, 还是去 kali 比较稳定  
3. 全加密卡好像可以用 Proxmark3 快速的搞出来, 毕竟贵  
4. 有 Key 的话数据修改可以在 Windows  
5. 修改时小心把控制位改了, 听说有人把不完整的 dump 文件写进卡里然后差点报废  