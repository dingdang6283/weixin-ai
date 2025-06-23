import logging
import argparse
from math import e
import random
import time
import requests
from wxauto import *
import os
import tkinter as tk
from tkinter import messagebox
import configparser
import pyautogui
import threading
pyautogui.FAILSAFE=False
txt=""

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--start', action='store_true', help='启动程序')
parser.add_argument('--download', action='store_true', help='下载所需的库')
parser.add_argument('--debug', action='store_true', help='启动调试模式')
args = parser.parse_args()
print('请确保要使用的微信账号登录并且打开微信')
time.sleep(2)
if not any([args.start, args.download, args.debug]):
    print('请添加必要的参数来启动程序，可用参数有： --start（启动程序）， --download（下载所需的库）， --debug（启动调试模式）')
    time.sleep(1)
    input('按回车键退出...') 
    import sys
    #sys.exit(1)
    

if args.download:
    import subprocess
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    print('安装结束')
    import sys
    input('按回车键继续...')
    

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
if not args.start and not os.path.exists('setting.ini'):
    print('请使用 --start 参数来启动程序进行初始化。')
    import sys
    input('按回车键退出...')
    sys.exit(1)

if args.start:
    # 检测 setting.ini 文件
    if not os.path.exists('setting.ini'):

        # 弹出初始化窗口
        def save_settings():
            admin_name = entry_admin.get()
            group_keywords = entry_group_keywords.get()
            personal_keywords = entry_personal_keywords.get()
            update_time = entry_update_time.get()
            try:
                update_time = int(update_time)
                if 1 <= update_time <= 300:
                    config = configparser.ConfigParser()
                    config['Settings'] = {
                        'AdminName': admin_name,
                        'GroupKeywords': group_keywords,
                        'PersonalKeywords': personal_keywords,
                        'UpdateTime': str(update_time)
                    }
                    with open('setting.ini', 'w', encoding='utf-8') as configfile:
                        config.write(configfile)
                    # 去掉销毁窗口代码，保留窗口
                    root.destroy()
                else:
                    messagebox.showerror("错误", "更新时间必须在 1 - 300 秒之间。")
            except ValueError:
                messagebox.showerror("错误", "更新时间必须是一个整数。")

        root = tk.Tk()
        root.title("初始化设置")

        tk.Label(root, text="管理员名:").grid(row=0, column=0)
        entry_admin = tk.Entry(root)
        entry_admin.grid(row=0, column=1)

        tk.Label(root, text="组关键词:").grid(row=1, column=0)
        entry_group_keywords = tk.Entry(root)
        entry_group_keywords.grid(row=1, column=1)

        tk.Label(root, text="个人关键词:").grid(row=2, column=0)
        entry_personal_keywords = tk.Entry(root)
        entry_personal_keywords.grid(row=2, column=1)

        tk.Label(root, text="更新时间 (1 - 300s):").grid(row=3, column=0)
        entry_update_time = tk.Entry(root)
        entry_update_time.grid(row=3, column=1)

        tk.Button(root, text="保存设置", command=save_settings).grid(row=4, column=0, columnspan=2)

        root.mainloop()

# 读取配置文件
config = configparser.ConfigParser()
# 修改为以 utf-8 编码读取文件
config.read('setting.ini', encoding='utf-8')
ADMIN_USER = config.get('Settings', 'AdminName')
GROUP_KEYWORDS = config.get('Settings', 'GroupKeywords').split(',')
PERSONAL_KEYWORDS = config.get('Settings', 'PersonalKeywords').split(',')
UPDATE_TIME = int(config.get('Settings', 'UpdateTime'))
while True:
    try:
        nicknames = []
        # 获取微信窗口对象
        wx = WeChat()
        print("-------------------------------------------------------------------------------------")
        # 可以通过的词语
        pass_WORLD = ['抖音']

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'lintenter.txt')

        new_ts = f'''
        欢迎使用小柯v1.0.3，在聊天中含有关键词“{GROUP_KEYWORDS}”或{PERSONAL_KEYWORDS}即可与我对话
            '''


        def add_user_to_file(username):
            try:
                try:
                    # 尝试以只读模式打开文件
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        if content:
                            # 如果文件不为空，将内容按中文逗号分割成用户列表
                            users = [user.strip() for user in content.split('，')]
                            if username not in users:
                                # 若用户不存在于列表中，则添加该用户
                                users.append(username)
                                new_content = "，".join(users)
                            else:
                                result_msg = f"用户 {username} 已存在，无需重复添加。"
                                print(result_msg)
                                return result_msg
                        else:
                            # 如果文件为空，直接添加新用户
                            new_content = username
                except FileNotFoundError:
                    # 如果文件不存在，创建新内容并准备写入
                    new_content = username

                # 以写入模式打开文件，如果文件不存在会自动创建
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                result_msg = f"用户 {username} 已添加到文件，/更新用户列表 即可更新。"
                print(result_msg)
                return result_msg
            except Exception as e:
                error_msg = f"添加用户时出现错误: {e}"
                print(error_msg)
                return error_msg


        add_user_to_file(ADMIN_USER)


        def read():
            wx.SwitchToChat()
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 拼接文件路径
            file_name = 'lintenter.txt'
            file_path = os.path.join(current_dir, file_name)

            user_list = []
            try:
                # 打开文件进行读取
                with open(file_path, 'r', encoding='utf-8') as file:
                    # 读取文件内容
                    content = file.read()
                    # 按中文逗号分割用户信息
                    raw_users = content.split('，')
                    for user in raw_users:
                        # 去除首尾空白字符和单引号
                        clean_user = user.strip().replace("'", "")
                        if clean_user:
                            user_list.append(clean_user)

                # 遍历用户列表添加监听
                for username in user_list:
                    print(f"正在添加监听用户: {username}")
                    try:
                        text = username
                        if text.startswith('\ufeff'):
                            text = text[1:]
                        print(text)
                        username=text
                    except:
                        pass
                    try:
                        
                        wx.AddListenChat(who=username)
                        print(f"成功添加监听用户: {username}")
                    except Exception as e:
                        print(f"添加监听用户 {username} 时出错: {e}")
                listen_list = user_list
            except FileNotFoundError:
                print(f"未找到文件: {file_path}")
            except Exception as e:
                print(f"读取文件时出现错误: {e}")


        # 手动更新
        def sd_read():
            # 获取当前脚本所在目录
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 拼接文件路径
            file_name = 'lintenter.txt'
            file_path = os.path.join(current_dir, file_name)

            user_list = []
            try:
                # 打开文件进行读取
                with open(file_path, 'r', encoding='utf-8') as file:
                    # 读取文件内容
                    content = file.read()
                    # 按中文逗号分割用户信息
                    raw_users = content.split('，')
                    for user in raw_users:
                        # 去除首尾空白字符和单引号
                        clean_user = user.strip().replace("'", "")
                        if clean_user:
                            user_list.append(clean_user)

                # 遍历用户列表添加监听
                for username in user_list:
                    print(f"正在添加监听用户: {username}")
                    wx.SendMsg(msg=f"正在添加监听用户: {username}", who=ADMIN_USER)
                    try:
                        text = username
                        if text.startswith('\ufeff'):
                            text = text[1:]
                        print(text)
                        username=text
                    except:
                        pass
                    try:
                        wx.AddListenChat(who=username)
                        print(f"成功添加监听用户: {username}")
                        wx.SendMsg(msg=f"成功添加监听用户: {username}", who=ADMIN_USER)
                    except Exception as e:
                        print(f"添加监听用户 {username} 时出错: {e}")
                        wx.SendMsg(msg=f"添加监听用户 {username} 时出错: {e}", who=ADMIN_USER)
                listen_list = user_list
            except FileNotFoundError:
                print(f"未找到文件: {file_path}")
                wx.SendMsg(msg=f"未找到文件: {file_path}", who=ADMIN_USER)
            except Exception as e:
                print(f"读取文件时出现错误: {e}")
                wx.SendMsg(msg=f"读取文件时出现错误: {e}", who=ADMIN_USER)
            newfriend()


        def newfriend():
            try:
                find = 0
                
                new = wx.GetNewFriends()
                for friend in new:
                    l=len(new)
                    for i in range(l):
                        friend = new[0]

                        # 接受好友请求，并且添加备注“备注张三”、添加标签wxauto
                        friend.Accept(remark=friend.name, tags=['user'])
                        print(add_user_to_file(friend.name))
                        # 获取好友申请昵称
                        # 张三

                        wx.SendMsg(new_ts, who=friend.name)
                        print(friend.msg)  # 获取好友申请信息
                        # 你好,我是xxx群的张三
                        wx.SendMsg(f"同意了-用户名： {friend.name}的好用请求", ADMIN_USER)
                        find = 1
                    # 切换回聊天页面
                if find == 1:
                        read()
                wx.SwitchToChat()

            except:
                wx.SwitchToChat()
                pass


        # 配置日志记录，将日志文件保存到当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(current_dir, 'app.log')
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=log_file_path,
            encoding='utf-8'
        )

        # 敏感词库文件路径
        DIRTY_WORDS_FILE = 'dirty_words.txt'

        # 存储导入文件信息的文件路径，确保在当前程序所在文件夹
        IMPORT_RECORD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "import.dd")

        id = '0059c453f2f0c7b7835a9e4ef051c817'


        # 读取敏感词库
        def load_dirty_words():
            try:
                with open(DIRTY_WORDS_FILE, 'r', encoding='utf-8') as f:
                    return [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                with open(DIRTY_WORDS_FILE, 'w', encoding='utf-8') as f:
                    pass
                return []


        # 保存敏感词到文件
        def save_dirty_words(words):
            existing_words = load_dirty_words()
            new_words = [word for word in words if word not in existing_words]
            if new_words:
                with open(DIRTY_WORDS_FILE, 'a', encoding='utf-8') as f:
                    for word in new_words:
                        f.write(word + ',')


        # 通过 API 过滤敏感词
        def filter_dirty_words_api(text):
            try:
                for item in pass_WORLD:
                    if not (item in text):
                        response = requests.get(f'https://api.yyy001.com/api/Forbidden?text={text}')
                        response.raise_for_status()
                        data = response.json()
                        logging.error(data)
                        ban_count = data.get('data', {}).get('banCount', 0)
                        if ban_count > 0:
                            ban_list = data.get('data', {}).get('banList', [])
                            dirty_words = [item.get('word') for item in ban_list if item.get('word')]
                            because = ban_list[0].get('explanation')
                            category = ban_list[0].get('category')
                            save_dirty_words(dirty_words)
                            return True,because,category
                        return False,None,None
                    else:
                        return False,None,None
            except (requests.RequestException, ValueError) as e:
                logging.error(f'获取敏感词 API 出错: {e}')
                return False,None,None


        # 提问函数
        def ask(ask_qu, user_id):
            has_dirty_word,because,category = filter_dirty_words_api(ask_qu)
            if has_dirty_word:
                nm = random.randint(0, 10)

                logging.critical('log 检测到敏感词: ' + ask_qu)
                return '出现敏感词\n  '+ask_qu+'  分类：'+category+'\n  因为'+because
            else:
                try:
                    inof = str('ask:' + ask_qu + '')
                    logging.info(inof)

                    ai_rul = f'http://api.zhyunxi.com/api.php?api=88&key={id}&sessionid={user_id}&text={ask_qu}'
                    response = requests.get(ai_rul)
                    response.encoding = 'utf-8'
                    response_json = response.json()
                    logging.info(str(response_json))
                    data = response_json['data']

                    answer = data[0].get('reply')

                    logging.info('ai anser: ' + answer)
                    return answer
                except Exception as e:
                    logging.error('ERROR: ' + str(e))
                    return 'ERROR: ' + str(e)


        def yy(txt):  # 语音合成
            return txt + '（音功能已禁用）'


        def remove_user_from_file(username):
            try:
                try:
                    # 尝试以只读模式打开文件
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read().strip()
                        if content:
                            # 如果文件不为空，将内容按中文逗号分割成用户列表
                            users = [user.strip() for user in content.split('，')]
                            if username in users:
                                # 若用户存在于列表中，则移除该用户
                                users.remove(username)
                                new_content = "，".join(users)
                            else:
                                result_msg = f"用户 {username} 不存在，无法删除。"
                                print(result_msg)
                                return result_msg
                        else:
                            result_msg = "文件为空，没有用户可删除。"
                            print(result_msg)
                            return result_msg
                except FileNotFoundError:
                    result_msg = "文件不存在，没有用户可删除。"
                    print(result_msg)
                    return result_msg

                # 以写入模式打开文件，如果文件不存在会自动创建
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                result_msg = f"用户:   {username}   已从文件中删除，/更新用户列表 即可更新。"
                print(result_msg)
                return result_msg
            except Exception as e:
                error_msg = f"删除用户时出现错误: {e}"
                print(error_msg)
                return error_msg


        def send_notice_to_users(wx, content, blocked_users):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content_str = file.read().strip()
                    if content_str:
                        # 按中文逗号分割获取用户列表
                        users = [user.strip() for user in content_str.split('，')]
                        for user in users:
                            if user not in blocked_users:
                                    try:
                                        # 直接使用 wx.SendMsg 发送消息到指定用户
                                        wx.SendMsg(content, user)
                                        print(f"通知内容已发送给用户 {user}。")
                                        # 向管理员反馈
                                        feedback_msg = f"已将通知发送到 {user}"
                                        wx.SendMsg(feedback_msg, ADMIN_USER)
                                    except Exception as inner_e:
                                        print(f"向用户 {user} 发送通知时出现错误: {inner_e}")
                        result_msg = "通知已逐个发送给所有未屏蔽的用户。"
                        return result_msg
                    result_msg = "文件中没有可用用户，无法发送通知。"
                    print(result_msg)
                    return result_msg
            except FileNotFoundError:
                result_msg = "文件不存在，没有用户可发送通知。"
                print(result_msg)
                return result_msg
            except Exception as e:
                error_msg = f"发送通知时出现错误: {e}"
                print(result_msg)
                return result_msg


        # 处理用户输入的函数
        def handle_user_input():
            while True:
                try:
                    command = input("> ")
                    if command.startswith("/添加用户 "):
                        username = command.split("/添加用户 ")[1].strip()
                        result = add_user_to_file(username)
                        print(result)
                    elif command.startswith("/删除用户 "):
                        username = command.split("/删除用户 ")[1].strip()
                        result = remove_user_from_file(username)
                        print(result)
                    elif command.startswith("/通知 "):
                        parts = command.split(" ", 2)
                        if len(parts) == 3:
                            blocked_users_str = parts[1]
                            notice_content = parts[2].strip()
                            if blocked_users_str == "no":
                                blocked_users = []
                            else:
                                blocked_users = [user.strip() for user in blocked_users_str.split("，")]
                            result = send_notice_to_users(wx, notice_content, blocked_users)
                            print(result)
                        else:
                            result_msg = "通知格式错误，请使用 /通知 + 要屏蔽的用户（没有则为 no）+ 内容 的格式。"
                            print(result_msg)
                    elif command.startswith("/更新用户列表"):
                        print('开始更新用户列表')
                        sd_read()
                        print('更新用户列表结束')
                    elif command.startswith("/菜单"):
                        print(
                            "               菜单  \n*=================*\n/添加用户 《用户名》\n/删除用户 《用户名》\n/更新用户列表\n/通知 《要屏蔽的用户》 《内容》")
                    else:
                        print(
                            f"错误的指令：{str(command)}\n               菜单  \n*=================*\n/添加用户 《用户名》\n/删除用户 《用户名》\n/更新用户列表\n/通知 《要屏蔽的用户》 《内容》\n输入  /菜单 再次显示")

                except Exception as e:
                    print(e)
            # 初始化完成，启动 1.py
            # subprocess.Popen(['python', '1.py'])
                
        read()

        newfriend()
        # 启动处理用户输入的线程
        input_thread = threading.Thread(target=handle_user_input)
        input_thread.daemon = True


        # 运行主循环
        time_time = 0
        last_friend_message_time = time.time()
        # 主循环
        wx.SwitchToChat()
        print('\nok')
        input_thread.start()

        while True:

                time.sleep(1)
                time_time += 1
                if time_time % UPDATE_TIME == 0:
                    read()
                    newfriend()

                msgs = wx.GetListenMessage()
                has_friend_message = False
                for chat in msgs:
                    one_msgs = msgs.get(chat)
                    # 获取消息内容
                    # 回复收到
                    for msg in one_msgs:
                        print(msg.type)
                        if msg.type == 'sys':
                            print(f'【系统消息】{msg.content}')
                            logging.critical(f'【系统消息】{msg.content}')
                        elif msg.type == 'group':
                            a = 0
                            sender = msg.sender
                            logging.critical(f'{sender.rjust(20)}：{msg.content}')
                            if '@小柯 ' in msg.content or any(keyword in msg.content for keyword in GROUP_KEYWORDS):
                                a = 1
                                chat.SendMsg(ask(msg.content, sender.rjust(20).replace(" ", "")))

                        elif msg.type == 'friend':
                            has_friend_message = True

                            last_friend_message_time = time.time()
                            sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名

                            print(f'{sender.rjust(20).replace(" ", "")}：{msg.content}')

                            try:
                                print(sender.rjust(20).replace(" ", ""))
                                print(ADMIN_USER)
                                print(msg.content)
                                print(str('/' in msg.content ))
                                print((any(keyword in msg.content for keyword in GROUP_KEYWORDS)))
                                if (not (sender.rjust(20).replace(" ", "") != ADMIN_USER and '/' in msg.content) and (any(keyword in msg.content for keyword in PERSONAL_KEYWORDS))or (any(keyword in msg.content for keyword in GROUP_KEYWORDS))):

                                        print(f'rx→：{msg.content}')
                                        txt = msg.content.replace("*", "")
                                        # ！！！ 回复收到，此处为`chat`而不是`wx` ！！！
                                        if '，语音' in txt:
                                            chat.SendMsg(
                                            f'@{sender.rjust(20).replace(" ", "")}  ' + yy(
                                                ask(txt.replace("，语音", "").replace("PERSONAL_KEYWORDS", ""),
                                                    sender.rjust(20).replace(" ", ""))))  # 此处将msg.content传递给大模型，再由大模型返回的消息回复即可实现ai聊天
                                        else:
                                            chat.SendMsg(
                                                f'@{sender.rjust(20).replace(" ", "")}  ' + ask(txt,
                                                                                            sender.rjust(20).replace("PERSONAL_KEYWORDS",
                                                                                                                        "").replace(
                                                                                                " ", "")))  # 此处将msg.content传递给大模型，再由大模型返回的消息回复即可实现ai聊天
                                elif sender.rjust(20).replace(" ", "") == ADMIN_USER and '/' in msg.content:
                                    for chat in msgs:
                                        one_msgs = msgs.get(chat)  # 获取消息内容
                                        for msg in one_msgs:
                                            if msg.type == 'friend':
                                                print("运行命令"+msg.content)
                                                sender = msg.sender
                                                content = msg.content
                                                if content.startswith("/添加用户 "):
                                                    username = content.split("/添加用户 ")[1].strip()
                                                    result = add_user_to_file(username)
                                                    chat.SendMsg(result)
                                                elif content.startswith("/删除用户 "):
                                                    username = content.split("/删除用户 ")[1].strip()
                                                    result = remove_user_from_file(username)
                                                    chat.SendMsg(result)
                                                elif content.startswith("/通知 "):
                                                    parts = content.split(" ", 2)
                                                    if len(parts) == 3:
                                                        blocked_users_str = parts[1]
                                                        notice_content = parts[2].strip()
                                                        if blocked_users_str == "no":
                                                            blocked_users = []
                                                        else:
                                                            blocked_users = [user.strip() for user in blocked_users_str.split("，")]
                                                        result = send_notice_to_users(wx, notice_content, blocked_users)
                                                        chat.SendMsg(result)
                                                    else:
                                                        result_msg = "通知格式错误，请使用 /通知 + 要屏蔽的用户（没有则为 no）+ 内容 的格式。"
                                                        chat.SendMsg(result_msg)
                                                    # 手动更新监听列表
                                                elif content.startswith("/更新用户列表"):
                                                    wx.SendMsg(msg='开始更新用户列表', who=ADMIN_USER)
                                                    sd_read()
                                                    wx.SendMsg(msg='更新用户列表结束', who=ADMIN_USER)

                                                elif content.startswith("/菜单"):
                                                    chat.SendMsg(
                                                        "               菜单  \n*=================*\n/添加用户 《用户名》\n/删除用户 《用户名》\n/更新用户列表\n/通知 《要屏蔽的用户》 《内容》")

                                                else:
                                                    chat.SendMsg(
                                                        f"错误的指令：{str(content)}\n            菜单  \n*=================*\n/添加用户 "
                                                        f"《用户名》\n/删除用户 《用户名》\n/更新用户列表\n/通知 《要屏蔽的用户》 《内容》\n输入  /菜单 再次显示")
                            except Exception as e:
                                    wx.SendMsg(msg=str(e), who=ADMIN_USER)
                        elif msg.type == 'self':
                            print(f'{msg.sender.ljust(20).replace(" ", "")}：{msg.content}')
                            logging.critical(f'{msg.sender.ljust(20)}：{msg.content}')

                        elif msg.type == 'time':
                            print(f'\n【时间消息】{msg.time}')
                            logging.critical(f'\n【时间消息】{msg.time}\n')

                        elif msg.type == 'recall':
                            print(f'【撤回消息】{msg.content}')
                            logging.critical(f'【撤回消息】{msg.content}')



    except Exception as e:
        print(e)
        time.sleep(1)
        try:
            wx = WeChat()
            print("微信连接正常")
        except Exception as e:
            print(e)
            print("微信连接失败,请启动微信")
        
        
