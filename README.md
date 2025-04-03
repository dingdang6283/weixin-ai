# weixin-ai
# 小柯 v1.0.2 微信聊天机器人系统介绍
一、系统概述
小柯 v1.0.2 是一款基于微信平台的聊天机器人系统，旨在实现自动回复消息、过滤敏感词、管理用户列表等功能。系统通过配置文件读取相关设置，利用 API 进行敏感词检测和获取 AI 回复，并可对用户列表进行添加、删除和更新操作，同时支持向指定用户发送通知。
二、功能模块
1. 初始化设置
配置文件检测：程序启动时会检测 setting.ini 文件是否存在。若不存在，会弹出初始化窗口，要求用户输入管理员名、组关键词、个人关键词和更新时间（1 - 300 秒）。
保存设置：用户输入的设置信息会保存到 setting.ini 文件中，方便后续读取和使用。
2. 用户列表管理
添加用户：通过 /添加用户 [用户名] 命令，可将新用户添加到 lintenter.txt 文件中。若用户已存在，会提示无需重复添加。
python
def add_user_to_file(username):
    try:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if content:
                    users = [user.strip() for user in content.split('，')]
                    if username not in users:
                        users.append(username)
                        new_content = "，".join(users)
                    else:
                        result_msg = f"用户 {username} 已存在，无需重复添加。"
                        print(result_msg)
                        return result_msg
                else:
                    new_content = username
        except FileNotFoundError:
            new_content = username

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        result_msg = f"用户 {username} 已添加到文件，/更新用户列表 即可更新。"
        print(result_msg)
        return result_msg
    except Exception as e:
        error_msg = f"添加用户时出现错误: {e}"
        print(error_msg)
        return error_msg


删除用户：使用 /删除用户 [用户名] 命令，可从 lintenter.txt 文件中删除指定用户。若用户不存在或文件为空，会给出相应提示。
python
def remove_user_from_file(username):
    try:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if content:
                    users = [user.strip() for user in content.split('，')]
                    if username in users:
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

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        result_msg = f"用户:   {username}   已从文件中删除，/更新用户列表 即可更新。"
        print(result_msg)
        return result_msg
    except Exception as e:
        error_msg = f"删除用户时出现错误: {e}"
        print(error_msg)
        return error_msg
更新用户列表：执行 /更新用户列表 命令，系统会重新读取 lintenter.txt 文件，并为文件中的每个用户添加监听。
python
def sd_read():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = 'lintenter.txt'
    file_path = os.path.join(current_dir, file_name)

    user_list = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            raw_users = content.split('，')
            for user in raw_users:
                clean_user = user.strip().replace("'", "")
                if clean_user:
                    user_list.append(clean_user)

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
3. 敏感词过滤
API 检测：使用 filter_dirty_words_api 函数，通过调用 https://api.yyy001.com/api/Forbidden API 检测消息中是否包含敏感词。
敏感词库管理：检测到的敏感词会保存到 dirty_words.txt 文件中，避免重复保存。
python
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

def save_dirty_words(words):
    existing_words = load_dirty_words()
    new_words = [word for word in words if word not in existing_words]
    if new_words:
        with open(DIRTY_WORDS_FILE, 'a', encoding='utf-8') as f:
            for word in new_words:
                f.write(word + ',')
4. AI 回复
提问处理：使用 ask 函数，将用户的提问发送到 http://api.zhyunxi.com/api.php API 获取 AI 回复。若检测到敏感词，会返回 “出现敏感词” 提示。
python
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
5. 消息处理
消息监听：程序通过 wx.GetListenMessage 方法监听微信消息，根据消息类型（系统消息、群消息、好友消息等）进行不同处理。
自动回复：当群消息中包含 @小柯 或组关键词，或好友消息中包含个人关键词、@小柯 或 @pc 时，会调用 ask 函数获取 AI 回复并发送给用户。
python
while True:
    time.sleep(1)
    time_time += 1
    if time_time % UPDATE_TIME == 0:
        read()
        newfriend()

    msgs = wx.GetListenMessage()
    for chat in msgs:
        one_msgs = msgs.get(chat)
        for msg in one_msgs:
            if msg.type == 'sys':
                print(f'【系统消息】{msg.content}')
                logging.critical(f'【系统消息】{msg.content}')
            elif msg.type == 'group':
                sender = msg.sender
                logging.critical(f'{sender.rjust(20)}：{msg.content}')
                if '@小柯 ' in msg.content or any(keyword in msg.content for keyword in GROUP_KEYWORDS):
                    chat.SendMsg(ask(msg.content, sender.rjust(20).replace(" ", "")))
            elif msg.type == 'friend':
                sender = msg.sender
                if (not (sender.rjust(20).replace(" ", "") != ADMIN_USER and '/' in msg.content)) and (
                        any(keyword in msg.content for keyword in PERSONAL_KEYWORDS) or (
                        '@小柯' in msg.content) or ('@pc' in msg.content)):
                    txt = msg.content.replace("*", "")
                    if '，语音' in txt:
                        chat.SendMsg(
                            f'@{sender.rjust(20).replace(" ", "")}  ' + yy(ask(txt.replace("，语音", ""),
                                                                              sender.rjust(20).replace(" ", ""))))
                    else:
                        chat.SendMsg(
                            f'@{sender.rjust(20).replace(" ", "")}  ' + ask(txt,
                                                                            sender.rjust(20).replace(" ", "")))
                elif sender.rjust(20).replace(" ", "") == ADMIN_USER and '/' in msg.content:
                    # 处理管理员命令
                    pass
6. 通知发送
发送通知：管理员可以使用 /通知 [要屏蔽的用户（没有则为 no）] [内容] 命令，将通知发送给 lintenter.txt 文件中的未屏蔽用户。
python
def send_notice_to_users(wx, content, blocked_users):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content_str = file.read().strip()
            if content_str:
                users = [user.strip() for user in content_str.split('，')]
                for user in users:
                    if user not in blocked_users:
                        try:
                            wx.SendMsg(content, user)
                            print(f"通知内容已发送给用户 {user}。")
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
7. 新好友处理
自动添加：使用 newfriend 函数，当有新好友申请时，会自动接受申请，添加备注和标签，并发送欢迎消息。
python
def newfriend():
    try:
        new_friend1 = []
        new = wx.GetNewFriends()
        for new in new_friend1:
            new_friend1 = new[0]
            print(add_user_to_file(new_friend1.name))
            wx.SendMsg(new_ts, who=new_friend1.name)
            print(new_friend1.msg)
            new_friend1.Accept(remark=new_friend1.name, tags=['wxauto'])
            wx.SwitchToChat()
    except:
        wx.SwitchToChat()
        pass
8. 语音合成
功能禁用：yy 函数用于语音合成，但目前语音功能已禁用，会在回复消息后添加 “（音功能已禁用）” 提示。
python
def yy(txt):
    return txt + '（音功能已禁用）'
三、日志记录
系统使用 Python 的 logging 模块记录相关信息，包括系统消息、敏感词检测、AI 回复等，日志文件保存为 app.log。
四、总结
小柯 v1.0.2 系统通过整合多种功能，实现了一个较为完整的微信聊天机器人系统。用户可以方便地进行用户管理、敏感词过滤、AI 回复和消息通知等操作，提高了微信聊天的自动化和智能化程度
