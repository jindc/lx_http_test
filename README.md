# lx_http_test
lx_http_test是一个python写的http服务器测试程序，可以对服务器进行指定时间，指定次数，指定并发数并且可选记录log。测试之后有详细的统计信息。

lx_http_test.py
    程序的框架
lx_http_connector.py
    调用urllib库向服务器发起请求。请求的url要事先在urls数组变量中定义。
lx_test_statistic.py
    测试的统计信息

运行：
  编辑lx_http_connector.py,
    urls=[url1,url2]
  python lx_http_test.py -h 查看帮助选项信息及用法
  
  作者：德才  
  email:jindc@163.com

