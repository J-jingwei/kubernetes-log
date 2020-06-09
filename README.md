# kubernetes-log
kubernetes简易日志查询工具



### 使用方法：

```
使用方法:根据kubernetes命名空间，以及获取一个token填入指定位置，即可使用，也可打包exe使用！
查看命名空间: 
		kubectl get namespaces

获取token:    
		kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')

打包exe命令:
		pyinstaller -F search_log3.2.py
```



#### 主程序： search_log3.2.py



#### 应用场景：

​		由于公司kubernetes集群，开发虽然可以通过elk查询日志，但是特定项目组的日志格式并未规范，呈多行，且日志中并无服务关键字，所以通过elk无法准确查询到该服务日志，需要频繁通过运维查询日志，因此通过kuberntes-client python写了一个简易的日志查询用于开发使用，查询定位日志。



#### 简易日志查询，3.2更新日志


更新信息：
3.0 更新为token方式获取√;
    更新滚动条√;
    满足日志过滤条件上下文查找√;
    加入日志显示正序倒序选项√;
    页面轻微调整√。
	
3.1 简单更新了个字体。

3.2 更新pod状态区显示启动时间;
    增加pod状态区锁定;
    更新日志关键字行高亮显示;


注意： 
1、服务关键字中不要包含多余的空格！！！
2、日志关键字暂不支持自动区分大小写！！！
（日志关键字需自行确认大小写）

目前，可以根据该工具确定pod服务状态，以及启动时间
(以确定服务多久未更新，刚上传的更新是否成功)
日志查询不用跑。

目前已经确认最大的问题：
	性能问题：对于长时间为更新的服务，日志过大处理效率严重过低！

更多需求，与bug更新，可以反馈！


![在这里插入图片描述](https://img-blog.csdnimg.cn/2019121316150924.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDk1NjQ1MA==,size_16,color_FFFFFF,t_70)
