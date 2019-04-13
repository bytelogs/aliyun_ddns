# aliyun_ddns

根据公网IP编号更新阿里云DNS上的域名记录；公司内部的宽带没有固定的IP地址，需要通过域名解析将内部的应用发布到公网上；


# 使用方法

- 安装阿里云sdk

```python
pip install aliyun-python-sdk-core-v3
pip install aliyun-python-sdk-alidns
pip install requests
```

- 修改comfig.json文件

将config_template.json文件复制（或修改）为config.json，并修改里面的内容；

- 将 aliddns.py 加入到任务计划

```shell
*/3 * * * * /usr/sbin/python3 /usr/local/aliyun_ddns/aliddns.py
```

