import random

class PyJokers:
    def __init__(self):
        self.jokes = {
            '冷笑话': [
                "我和蚊子是朋友，所以他每次叮我都会打招呼。",
                "为什么电梯坏了？因为他有楼梯恐惧症。",
                "为什么鸡过马路？因为它要去对面。",
                "鸭子为什么喜欢下水？因为它不会上树。",
                "为什么书本总是冷冰冰的？因为它们有封面。"
            ],
            '程序员笑话': [
                "为什么程序员喜欢用黑色的键盘？因为他怕白屏。",
                "程序员的日常：写代码，调试，写代码，调试，写代码，调试...（无限循环）",
                "为什么程序员不会饿？因为他们总是有代码（吃）饱。",
                "程序员的梦是什么？代码一次通过。",
                "为什么程序员喜欢开窗？因为他们讨厌bug。"
            ]
        }

    def get_joke(self, category='随机'):
        if category == '随机':
            category = random.choice(list(self.jokes.keys()))
        if category in self.jokes:
            return random.choice(self.jokes[category])
        else:
            return "抱歉，没有这种类型的笑话。"

# 使用示例
if __name__ == "__main__":
    joke_gen = PyJokers()
    print(joke_gen.get_joke('程序员笑话'))
    print(joke_gen.get_joke('冷笑话'))
    print(joke_gen.get_joke())  # 随机类别
