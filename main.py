import logging
import random
import time
import requests
from wxauto import *
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import configparser

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
                with open('setting.ini', 'w',encoding='utf-8') as configfile:
                    config.write(configfile)
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
config.read('setting.ini')
ADMIN_USER = config.get('Settings', 'AdminName')
GROUP_KEYWORDS = config.get('Settings', 'GroupKeywords').split(',')
PERSONAL_KEYWORDS = config.get('Settings', 'PersonalKeywords').split(',')
UPDATE_TIME = int(config.get('Settings', 'UpdateTime'))

nicknames = []
# 获取微信窗口对象
wx = WeChat()
# 可以通过的词语
pass_WORLD = ['抖音']

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'lintenter.txt')

new_ts = '''
欢迎使用小柯v1.0.2，在聊天中@我或含有关键词“*”即可与我对话
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


def read():
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


def newfriend():
    try:
        new_friend1 = []
        new = wx.GetNewFriends()
        for new in new_friend1:
            new_friend1 = new[0]

            print(add_user_to_file(new_friend1.name))
            # 获取好友申请昵称
            # 张三

            wx.SendMsg(new_ts, who=new_friend1.name)
            print(new_friend1.msg)  # 获取好友申请信息
            # 你好,我是xxx群的张三
            # 接受好友请求，并且添加备注“备注张三”、添加标签wxauto
            new_friend1.Accept(remark=new_friend1.name, tags=['wxauto'])

            # 切换回聊天页面
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
            if item in text:
                response = requests.get(f'https://api.yyy001.com/api/Forbidden?text={text}')
                response.raise_for_status()
                data = response.json()
                ban_count = data.get('data', {}).get('banCount', 0)
                if ban_count > 0:
                    ban_list = data.get('data', {}).get('banList', [])
                    dirty_words = [item.get('word') for item in ban_list if item.get('word')]
                    save_dirty_words(dirty_words)
                    return True
                return False
            else:
                return False
    except (requests.RequestException, ValueError) as e:
        logging.error(f'获取敏感词 API 出错: {e}')
        return False


# 提问函数
def ask(ask_qu, user_id):
    has_dirty_word = filter_dirty_words_api(ask_qu)
    if has_dirty_word:
        nm = random.randint(0, 10)

        logging.critical('检测到敏感词: ' + ask_qu)
        return '出现敏感词'
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
            return 'null'


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
        print(error_msg)
        return error_msg


# 初始化完成，启动 1.py
subprocess.Popen(['python', '1.py'])

# 运行主循环
time_time = 0
# 主循环
print('ok')
while True:
    time.sleep(1)
    time_time += 1
    if time_time % UPDATE_TIME == 0:
        read()
        newfriend()

    msgs = wx.GetListenMessage()
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
                else:
                    pass
            elif msg.type == 'friend':
                sender = msg.sender  # 这里可以将msg.sender改为msg.sender_remark，获取备注名

                print(f'{sender.rjust(20).replace(" ", "")}：{msg.content}')

                if (not (sender.rjust(20).replace(" ", "") != ADMIN_USER and '/' in msg.content)) and (
                        any(keyword in msg.content for keyword in PERSONAL_KEYWORDS) or (
                        '@小柯' in msg.content) or ('@pc' in msg.content)):

                    try:
                        print(f'rx→：{msg.content}')
                        txt = msg.content.replace("*", "")
                        # ！！！ 回复收到，此处为`chat`而不是`wx` ！！！
                        if '，语音' in txt:
                            chat.SendMsg(
                                f'@{sender.rjust(20).replace(" ", "")}  ' + yy(ask(txt.replace("，语音", ""),
                                                                                  sender.rjust(20).replace(" ", ""))))
                        else:
                            chat.SendMsg(
                                f'@{sender.rjust(20).replace(" ", "")}  ' + ask(txt,
                                                                                sender.rjust(20).replace(" ", "")))
                    except Exception as e:
                        wx.SendMsg(msg=str(e), who=ADMIN_USER)
                elif sender.rjust(20).replace(" ", "") == ADMIN_USER and '/' in msg.content:
                    for chat in msgs:
                        one_msgs = msgs.get(chat)  # 获取消息内容
                        for msg in one_msgs:
                            if msg.type == 'friend':
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
                # 此处将msg.content传递给大模型，再由大模型返回的消息回复即可实现ai聊天
                # 手动更新监听列表
                if (sender.rjust(20).replace(" ", "") == ADMIN_USER) and ('/更新用户列表' in msg.content):
                    wx.SendMsg(msg='开始更新用户列表', who=ADMIN_USER)
                    sd_read()
                    wx.SendMsg(msg='更新用户列表结束', who=ADMIN_USER)
            elif msg.type == 'self':
                print(f'{msg.sender.ljust(20)}：{msg.content}')
                logging.critical(f'{msg.sender.ljust(20)}：{msg.content}')

            elif msg.type == 'time':
                print(f'\n【时间消息】{msg.time}')
                logging.critical(f'\n【时间消息】{msg.time}\n')

            elif msg.type == 'recall':
                print(f'【撤回消息】{msg.content}')
                logging.critical(f'【撤回消息】{msg.content}')