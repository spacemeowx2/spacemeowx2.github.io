---
title: Promise大杂烩
date: 2016-04-15
categories: tech
tags: [js, promise]
---


## Promise简介
因为之前用Promise写东西感觉很爽, 所以干脆让整个项目Promise化..  
js中大部分费时动作都是异步的, 并且大多通过callback来处理, 写过nodejs的大概都遇到过'回调地狱'...  
<!--more-->
``` javascript
loadImg('a.jpg', function() {
    loadImg('b.jpg', function() {
        loadImg('c.jpg', function() {
            console.log('all done!'); //呵呵...
        });
    });
});
```
Promise是一种规范, 把嵌套的异步处理变成了线性, 比如以上代码改成Promise可能是这样:
``` javascript
loadImg('a.jpg').then(
    () => loadImg('b.jpg')
).then(
    () => loadImg('c.jpg')
).then(
    () => console.log('all done!')
)
```
loadImg在此处是个Promise工厂, 根据参数返回一个新的Promise  
这里的箭头函数不能省略, 因为Promise对象在new的时候就开始执行内部的代码.所以then里的东西可以叫做Promise工厂的工厂...  
then的参数可以传进去函数也可以传Promise工厂, 当then接受到普通函数时会直接运行, 并放到try块里, 遇到错误就reject出去  

一个Promise一般是这样构造的:
``` javascript
new Promise(function (resolve, reject) {
    //do something here
})
```
可以看到函数中有两个参数, 这两个参数都是回调函数, 第一个用于操作成功时调用, 当失败是调用reject, 这就是Promise的错误处理: 遇到reject停下来, 找到catch函数, 或者一直resolve, 直到结束  


## bluebird.promisifyAll
(因为在require的时候把bluebird命名成了Promise, 所以代码中写作Promise.promisifyAll)  
``` javascript
let Promise = require("bluebird");
let jsdom = Promise.promisifyAll(require('jsdom'));
```
Promise.promisify将一个 node callback 型的函数包装成Promise型的函数, promisifyAll将对象内的所有函数进行promisify将一个操作, 并把包装后的函数名后加上Async  

## Promise是个链
``` javascript
let jqueryHTML = function (html, selector) {
    let ret = jsdom.envAsync(html)
    .then(jquery);
    if (!isUndefined(selector))
        ret = ret.then($ => $(selector));
    return ret;
}
```
这是返回一个jQuery对象的函数, ret是个Promise链, 在不同的参数下可以选择是否执行最后一步'$ => $(selector)'  

## Promise的结合
Promise作为异步处理的一种方法, 自然要应对各种各样的场景. 如同时进行许多操作, 等到所有操作都完成, 可以用Promise.all  
之前那个例子不够实际, 一般加载资源都是一堆一起加载的, 很少一个个加载, 毕竟不是依赖关系.  
``` javascript
Promise.all([
    loadImg('a.jpg'),
    loadImg('b.jpg'),
    loadImg('c.jpg')
]).then(() => {
    console.log('all done!');
})
```
有时只需要其中一个完成就继续, 那么可以使用Promise.race  
  
在我的一个Chrome扩展程序中出现了一个比较少见的情况, 就是一个个加载资源, 直到遇到第一个成功的结束  
``` javascript
function untilFirstResolve(list) {
    return new Promise((resolve, reject) => {
        var itr = list[Symbol.iterator]();
        var v, next;
        next = (e) => {
            v = itr.next()
            if (!v.done) {
                v.value().then(resolve, next); //加载成功就resolve, 失败就尝试下一个
            } else {
                reject(); //如果迭代完还没成功的就reject抛出错误
            }
        };
        next();
    });
}
```

## 后记
Promise用起来很灵活, 很方便添加步骤(只要在两个then之间加一个then就能添加).  
听说async和await处理异步更加方便, 以后有空围观一下. 