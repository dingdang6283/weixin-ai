# 微信 AI 程序介绍
### 鸣谢
本项目使用了 wxauto 库，该库提供了微信的自动化操作功能。

在此感谢wxauto库的开发者，提供了强大的库支持。

- wxauto库的在线文档：[wxauto 库文档](https://docs.wxauto.org/)
### 免责声明
 本项目的开发者不承担因使用不当本项目而导致的任何 法律责任。
 本项目的开发者不承担因使用不当本项目而导致的任何 损失或损害。
## 概述
本程序是一个基于微信的自动化工具，可监听特定用户的消息，支持自定义关键词和更新时间。

## 启动方式
### 基本启动
在 cmd 窗口中运行以下命令启动程序：
```bash
python main.py --start
```

### 其他参数
- `--download`：下载所需的库。
- `--debug`：启动调试模式。

## 配置
首次运行程序时，会弹出初始化窗口，需要输入管理员名、组关键词、个人关键词和更新时间（1 - 300 秒）。这些配置会保存到 `setting.ini` 文件中。
## 注意事项
注意，首次配置完毕后要退出程序，检查‘lintenter.txt’（监听列表文件）是否为   ‘，ADMIN_USER（用户名）’如果是，则请手动删去ADMIN_USER（用户名）前的‘，’

## 文件说明
- `app.log`：日志文件。
- `dirty_words.txt`：不明意义的文件。
- `lintenter.txt`：存储监听用户列表的文件。
- `main.py`：程序主文件。


## 问题
### 会封号吗？

 #### 不完全会！
 该项目基于Windows官方API开发，不涉及任何侵入、破解、抓包微信客户端应用，完全以人操作微信的行为执行操作

 但是如果你有以下行为，即使手动操作也有风控的风险：
-   曾用hook类或webhook类微信工具，如dll注入、itchat及其衍生产品
-   频繁且大量的发送消息、添加好友等，导致风控
-    高频率发送机器人特征明显的消息，导致被人举报，致使行为风控
-    扫码手机与电脑客户端不在同一个城市，导致异地风控
-    低权重账号做太多动作，低权重账号可能包括：
  新注册账号
  长期未登录或不活跃账号
  未实名认证账号
  未绑定银行卡账号
  曾被官方处罚的账号
  …
 因此，使用本项目时，请遵守微信的相关规定，不要使用本项目进行违法违规的行为。
# 常见问题
## 为什么会掉线 
掉线是微信客户端在3.9.9+版本以后新增的安全机制，主要发生在微信号在陌生电脑设备登录后触发，不会涉及封号，没有完美解决方案，以下提供两个思路：

- 微信号在同一台电脑上登录，几乎不会掉线
- 想办法使用3.9.8版本微信客户端，完全不掉线（绕过微信版本检测的风险自行承担）
- plus版本提供掉线检测、二维码获取、自动登录等方法
## 支持企业微信吗 
不支持。法律风险较高，影响腾讯收入，严抓

    如果你的企业开启了在个人微信中接受企业消息的功能，可以在个人微信手动将企业微信群拖出来使用wxauto监听模式进行操作
    
![Issues WeCom](https://docs.wxauto.org/images/issues_wecom.png)
# 用户协议与隐私政策
### 来自[wxauto 库文档](https://docs.wxauto.org/)

## 最后更新日期：2025年05月23日

感谢您使用 wxauto(x)（以下简称“本项目”）。为明确用户责任，特制定本用户协议（以下简称“协议”）。请在使用前仔细阅读并同意以下条款。您使用本项目即视为您已接受并同意遵守本协议。

使用许可及限制

## 1. 合法用途 
### 用户应仅将本项目用于合法用途，包括但不限于：

- 个人学习和研究。
- 非商业用途。

### 在不违反适用法律法规及第三方协议（如微信用户协议）的情况下个人使用。

## 2. 禁止行为 
### 用户不得将本项目用于以下用途，包括但不限于：

- 不得使用本项目开发、分发或使用任何违反法律法规的工具或服务。

- 不得使用本项目开发、分发或使用任何违反第三方平台规则（如微信用户协议）的工具或服务。

- 不得使用本项目从事任何危害他人权益、平台安全或公共利益的行为。

- 不得将本项目用于商业用途，包括但不限于开发、销售或以任何方式直接或间接获利的行为。



## 3. 风险与责任 
- 用户在使用本项目时，须自行确保其行为的合法性及合规性。 任何因使用本项目而产生的法律风险、责任及后果，由用户自行承担。用户应确保其使用行为不违反任何适用的法律法规及相关协议，且不侵犯第三方的权益。


 ### 隐私政策 
本项目尊重并保护用户隐私，项目使用过程中，不会收集、使用、传输、披露用户的任何数据。PlusV2版本的授权过程仅传输由用户硬件码生成的哈希值与授权服务器进行授权动作，不涉及用户本地数据传输。
