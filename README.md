# qq bot
一个基于go cqhttp的小插件
## 关于github
github只做action编译和做镜像使用，请在[gitee](https://gitee.com/pizero-hihi/qq-bot-api)上提问和贡献代码
 
## 开发代办
1. - [x] 制作基于flask的服务端
2. - [x] 添加初始化
3. - [x] 将api.py只封装go-cqhttp的api和cq码，并将应用迁移到app，并改名为GoCqhttpApi
4. - [ ] 将由configparser管理的今日人品模块迁移到pandas
5. - [ ] 屏蔽词 (pandas、configparser)
      - [ ] 屏蔽词管理员
      - [ ] 屏蔽词汇报与记录
      - [ ] 屏蔽词触发次数记录
      - [ ] 根据各群的config决定是否启用屏蔽词功能与屏蔽词管理员功能
6. - [ ] 数据可视化 (jupyter+pandas实现)
      - [ ] 词频
      - [x] 每分钟消息发送数
      - [ ] “今日人品” 每人“人品”趋势
      - [ ] 功能调用次数
      - [ ] 活跃人数的活跃时间段
      - [ ] 讨论后统计发言频率
      - [ ] 新增#top命令
7. - [ ] 优化运行速度
      - [ ] 使用cython编译
      - [ ] 将大部分go-cqhttp的api转换为def
8. - [ ] 允许使用config调整是否启用功能
      - [x] 返回(request.get)地址
      - [x] 接收地址
      - [x] 今日人品
      - [x] 允许根据群调整今日人品是否启用
      - [ ] 数据可视化
      - [x] 部分恶搞内容
9. - [ ] 测试是否可在阿里云函数(使用端口监听)上使用
10. - [ ] 完善GoCqhttpApi中go-cqhttp的api与CQ码调用
   - [ ] 添加其他api并添加初始化脚本
11. - [ ] 完善使用文档(readme等)
12.  - [x] 将使用说明添加进“#help”等机器人自带的命令查询
13. - [ ] 添加基于其他网络api的搜索音乐并分享的功能(升级点歌功能)

## 支持功能

> [ ] 内是必填选项
> < > 内是应该填的东西，没有应该会出错

1. 今日人品 `今日人品`
2. 人品查询 `#人品查询 <qq号>`
3. 基于songid的点歌 `#点歌 [QQ|qq|qqyy|qq音乐|QQ音乐|wyyyy|网易云音乐|wy|网易] <songid>`
4. 让机器人戳你不方便戳的人 `#[poke|戳一戳|戳] <QQ号>`
5. 自定义问答 `[Q:|Q：] <问题>` 配置见下方
6. 数据可视化
   - top20 `#top20` （群内单月发消息榜单）
   - 活跃时间 `#活跃时间`
   - 该功能需开启*msglog_group_type*和*msglog_private_type*
7. 其余见 `#[help|帮助]`

## 使用方式

1. 下载python，这个自行百度
2. 下载最新的tag，不会就搜
3. shift+右键打开Windows powershell
4. 执行代码
   ```powershell
   python -m venv apps
   cp ./* apps/
   cd apps
   ./Scripts/activate.ps1
   pip install -r requirePackage.txt
   ```
5. 找到 go-cqhttp 的[release 网址](https://github.com/Mrs4s/go-cqhttp/releases)
6. 下载最新的release，如果你是window一般直接下**go-cqhttp_windows_amd64.exe**
7. 双击打开点两次*__确认__*生成启动脚本
8. 点击启动脚本就那个 **.bat** 结尾的启动脚本
9. 关闭go-cqhttp启动脚本弹出的cmd窗口
10. 打开**config.yml**和**device.json**按照[官网](https://docs.go-cqhttp.org/guide/config.html#%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)配置并保存
11. 回到powershell窗口
    ```powershell
    python check.py
    ```
12. 资源管理器切换到**apps**文件夹填写app-config.cfg
    ```cfg
    [Function] #功能
    jrrp = True #今日人品
    look_for_group_type = True #某个群关注发言次数是否超过3条每秒
    fuck_type = True #是否启用：让可乐兔再次快乐
    poke_type = True #是否启用：摸摸吉祥物
    debug = True #如果你遇到了无法解决的问题，可以把这东西打开，虽然平时建议关闭，这东西可能会影响性能
    msglog_private_type = True #是否记录私聊聊天记录（存放在msglog/uid+qq号 文件夹中）
    msglog_group_type = True #是否启用群聊聊天记录（存放在msglog/gid+群号 文件夹中）
    
    [id]
    mascot_id = 123456789 #吉祥物id，没有就默认
    admin_id = 123456789 #管理员id，不用聊天频率警告就默认
    robot_id = 123456789 #不用at看bot是否在线就默认
    klt_id = 123456789 #不迫害可乐兔就默认
    look_for_group_id = 123456789 #监视摸个群，写群号，不用就默认
    
    [main]
    host = 127.0.0.1 #如果go-cqhttp跑在本机就默认。
    port = 20301  #上报端口，gq-cqhttp默认是5701，
    [request]
    request-host = 127.0.0.1 #go-cqhttp的IP，不知道或者跑在本机就默认
    request-post = 20300 #上报给go-cqhttp的端口，一般是5700，如果想改请在config.yml与这个同步改
    ```
13. 运行go-cqhttp的启动脚本
14. 在powershell里运行这个服务端
    ```powershell
    python server.py
    ```

- 自定义问答
  1. 打开apps文件夹下的QAs.csv
  2. 用你喜欢的编辑器编辑QAs.csv，左边是问，右边是答
  3. 请记得写长点，因为是查询问是否在QAs.csv，超出了就没有了
  4. 别用英文逗号，那玩意是分隔符

## 提问须知

1. go-cqhttp本体的问题可以问，但我可能没有一个好的解决方案
2. server.py的问题请把debug模式打开，然后发给我log.txt(记得复现，你这样的log.txt是空的)，如果涉及自定义问答请把QAs.csv发过来
   ```cfg
   [Function]
   ...
   debug = True
   ...
   ```

   ```powershell
   python server.py > log.txt
   ```