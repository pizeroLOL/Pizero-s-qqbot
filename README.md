# qq bot
一个基于go cqhttp的小插件
## 关于github
github只做action编译和做镜像使用，请在[gitee](https://gitee.com/pizero-hihi/qq-bot-api)上提问和贡献代码

## 许可
在写明出处的情况下允许任何法律范围内的使用，作者不对使用后果负责，请仔细审阅代码。
 
## 开发代办
1. - [ ] 添加初始化
      - [x] robot_id、admin_id、Mascot_id
      - [x] klt_id、klt_id_default
      - [x] poke_Mascot、 poke_Mascot_default
      - [ ] 测试可用
2. - [x] 将api.py只封装go-cqhttp的api和cq码，并将应用迁移到app，并改名为GoCqhttpApi
3. - [ ] 将由configparser管理的今日人品模块迁移到pandas
4. - [ ] 屏蔽词 (pandas)
      - [ ] 屏蔽词管理员
      - [ ] 屏蔽词汇报与记录
      - [ ] 屏蔽词触发次数记录
      - [ ] 根据各群的config决定是否启用屏蔽词功能与屏蔽词管理员功能
5. - [ ] 数据可视化 (jupyter+pandas实现)
      - [ ] 词频
      - [ ] 每分钟消息发送数
      - [ ] “今日人品” 每人“人品”趋势
      - [ ] 功能调用次数
      - [ ] 活跃人数的活跃时间段
      - [ ] 讨论后统计发言频率
6. - [ ] 优化运行速度
      - [ ] 使用cython编译
      - [ ] 将大部分go-cqhttp的api转换为def
      - [ ] 允许使用config调整是否启用功能
         - [ ] 返回(request.get)地址
         - [ ] 今日人品
         - [ ] 数据可视化
         - [x] 部分恶搞内容
7. - [ ] 测试是否可在阿里云函数(使用端口监听)上使用
8. - [ ] 完善GoCqhttpApi中go-cqhttp的api与CQ码调用
   - [ ] 添加其他api并添加初始化脚本
9.  - [ ] 完善使用文档(readme等)
10.  - [x] 将使用说明添加进“#help”等机器人自带的命令查询
11. - [ ] 添加基于其他网络api的搜索音乐并分享的功能(升级点歌功能)

## 支持功能
1. 今日人品
2. 人品查询
3. 基于songid的点歌
4. 让机器人戳你不方便戳的人

<待填写>

## 使用方式

<待填写>

## 提问须知

<待填写>