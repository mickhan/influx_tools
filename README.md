influxdb 管理工具

# 操作
## RP
```
python rp_list.py # 列出所有rp
```


## CQ
```
python cq_list.py # 列出所有cq
python cq_drop.py # 删除全部cq
python cq_create_enhanced.py # 针对指定的measurement创建cq，注意要在代码中73行修改measurement列表
```


## measurement
```
python meas_list.py # 列出measurement
python meas_drop.py # 删除measurement
```


## series
```
python series_drop.py # 删除series
```

# 配置
## secret.py
```
ADMIN=管理员用户名
PASSWD=管理员密码
```
## settings.py
```
host = "1.1.1.1" # ip
port = "8086" # 端口
db = "db_name" # 库名
rp = ['1m', '10m', '1h', '6h'] # rp后缀，即rp_xxxx。从小到大排列
postfix = True # measurement是否有后缀，即measurement名字是否包含_1m这样的粒度
resample = True # cq是否需要resample
```
