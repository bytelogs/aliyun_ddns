# aliyun_ddns

根据公网IP编号更新阿里云DNS上的域名记录；公司内部的宽带没有固定的IP地址，需要通过域名解析将内部的应用发布到公网上；


# 使用方法

- 安装阿里云sdk

```python
# python3 
pip install aliyun-python-sdk-core-v3
pip install aliyun-python-sdk-alidns
pip install requests


# python2
pip install aliyun-python-sdk-core
pip install aliyun-python-sdk-alidns
pip install requests

```

- 修改comfig.json文件

将config_template.json文件复制（或修改）为config.json，并修改里面的内容；首先在阿里云dns管理上添加一条记录，IP的值可以随便填写一个；

```json

{
  "access_key_id": "mykeyid",       

  "access_key_secret": "mykeyid_secret",

  "domain": "mydomain.com",

  "sub_domain": "intranet"

}

```

- python2 和 python3兼容

```
代码默认是python3环境；
如果要在python2.7中运行，请将52行代码 response = response.decode() 注释
```

- 将 aliddns.py 加入到任务计划

```shell
*/3 * * * * /usr/sbin/python3 /usr/local/aliyun_ddns/aliddns.py
```

- 日志记录

```
如果公网IP有变化，会将当前的IP写入到文件
```
