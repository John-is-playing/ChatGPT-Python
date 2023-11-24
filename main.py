import openai
import json
import os


class ChatGPT:
    # 初始化
    def __init__(self, user):
        # 设置用户名
        self.user = user
        # 设置个性
        self.messages = [{"role": "system", "content": "一个有10年各项编程语言开发经验的资深算法工程师"}]
        self.filename = "./user_messages.json"
        # 设置ChatGPT API密钥
        self.json = self.get_api_key()
        openai.api_key = self.json["api"]
        # 设置代理
        os.environ["HTTP_PROXY"] = self.json["Proxy"]
        os.environ["HTTPS_PROXY"] = self.json["Proxy"]

    # 获取 api
    @staticmethod
    def get_api_key():
        # 可以自己根据自己实际情况实现
        # 以我为例子，我是存在一个 openai_key 文件里，json 格式
        """
        {"api": "你的 api keys", "Proxy":"http://127.0.0.1:33210}
        """
        openai_key_file = './envs/openai_key.json'
        with open(openai_key_file, 'r', encoding='utf-8') as f:
            openai_key = json.loads(f.read())
        return openai_key

    def ask_gpt(self):
        # 向ChatGPT-3.5-TurBo模型提问
        rsp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        return rsp.get("choices")[0]["message"]["content"]

    def write_tojson(self) -> object:
        try:
            # 判断文件是否存在
            if not os.path.exists(self.filename):
                with open(self.filename, "w"):
                    # 创建文件
                    pass
            # 读取
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read()
                msgs = json.loads(content) if len(content) > 0 else {}
            # 追加
            msgs.update({self.user: self.messages})
            # 写入
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(msgs, f)
            return 1
        except Exception as e:
            print(f"错误代码：{e}")
            return 0


def main():
    user = input("请输入用户名称: ")
    chat = ChatGPT(user)

    # 循环
    while 1:
        # 限制对话次数
        if len(chat.messages) >= 11:
            print("******************************")
            print("*********强制重置对话**********")
            print("******************************")
            # 写入之前信息
            chat.write_tojson()
            user = input("请输入用户名称: ")
            chat = ChatGPT(user)

        # 提问
        q = input(f"【{chat.user}】")

        # 逻辑判断
        if q == "0":
            print("**************************")
            print("*********退出程序**********")
            print("**************************")
            # 写入之前信息
            chat.write_tojson()
            break
        elif q == "1":
            print("**************************")
            print("*********重置对话**********")
            print("**************************")
            # 写入之前信息
            chat.write_tojson()
            user = input("请输入用户名称: ")
            chat = ChatGPT(user)
            continue
        elif q == "":
            print("【ChatGPT】Don't send empty message!")
            continue

        # 提问-回答-记录
        chat.messages.append({"role": "user", "content": q})
        answer = chat.ask_gpt()
        print(f"【ChatGPT】{answer}")
        chat.messages.append({"role": "assistant", "content": answer})


if __name__ == '__main__':
    main()
