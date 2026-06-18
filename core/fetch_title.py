import requests  # 引入我们刚装的工具箱（网络请求库）


def get_website_title(url: str) -> str:
    """这是一个自定义函数，输入一个网址(url)，它的目标是返回这个网页的标题。

    :str 表示我们希望传进来的参数是一个字符串。 -> str 表示这个函数执行完会吐出一个字符串。
    """
    try:
        # 第一步：假装自己是浏览器，顺着网线去抓取网页的全部源代码
        # headers 是我们的“伪装面具”，告诉网站我们不是恶意的冷酷机器人
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)

        # 第二步：检查网络是不是顺畅（状态码 200 表示成功通车）
        if response.status_code == 200:
            html_content = response.text  # 这就是网页的纯文本源代码

            # 第三步：用最原始的字符串切片，把 <title> 和 </title> 中间的文字抠出来
            # 别慌！这只是在找位置：先找到 <title> 在第几个字，再找到 </title> 在第几个字
            start_tag = "<title>"
            end_tag = "</title>"

            if start_tag in html_content and end_tag in html_content:
                start_index = html_content.find(start_tag) + len(start_tag)
                end_index = html_content.find(end_tag)
                title = html_content[start_index:end_index]

                return title.strip()  # 成功拿到，把两边的空格修剪干净，返回！
            else:
                return "错误：网页源代码里竟然没有找到 <title> 标签！"
        else:
            return f"网络请求失败，谷歌返回了状态码：{response.status_code}"

    except Exception as e:
        # 如果断网了、或者网址写错了，代码不会崩溃，而是会走到这里
        return f"发生了一点意外：{str(e)}"


# ==========================================
#  下面的代码是执行区域（把上面的大玩具开起来）
# ==========================================
if __name__ == "__main__":
    # 拿你最熟悉的样板站来做实验
    test_url = "https://web.blogx.de5.net/"

    print("📡 正在尝试抓取网页...")
    result_title = get_website_title(test_url)

    print("\n📊 --- 实验结果 ---")
    print(f"目标网址: {test_url}")
    print(f"抓到的标题: {result_title}")