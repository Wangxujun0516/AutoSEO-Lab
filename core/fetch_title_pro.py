def get_clean_title(html_content: str) -> str:
    """
    升级版：能够自动识别大小写、自动修剪空格的网页标题提取器。
    """
    # 核心防御 1：不管三七二十一，先复制一份全小写的源代码用来“找位置”
    # 这样可以100%防御大写的 <TITLE> 或者 <Title>
    html_lower = html_content.lower()
    
    start_tag = "<title>"
    end_tag = "</title>"
    
    # 在小写账本里找位置
    if start_tag in html_lower and end_tag in html_lower:
        # 找起点：同样要加上标签自身的长度
        start_index = html_lower.find(start_tag) + len(start_tag)
        end_index = html_lower.find(end_tag)
        
        # 🚨 注意看这里！
        # 我们找位置是在小写账本（html_lower）里找的
        # 但切片的时候，我们必须去【原版账本（html_content）】里切！
        # 这样才能保证切出来的中文或英文大小写是原汁原味的，不会被强行变成小写。
        raw_title = html_content[start_index:end_index]
        
        # 核心防御 2：用 .strip() 拔掉两边可能存在的换行符和空格
        clean_title = raw_title.strip()
        
        return clean_title
    else:
        return "错误：未能在网页中检测到标准的标题标签。"

# ==========================================
# 模拟各种“脏数据”测试区域
# ==========================================
if __name__ == "__main__":
    # 模拟一个非常糟糕、大小写混杂且两边全是空格和换行的网页源代码
    dirty_html = """
    <html>
        <TITLE>   
            恒宏RV智能调平系统 - 2026 B2B出海旗舰款  
        </TITLE>
    </html>
    """
    
    print("📡 正在清洗并提取数据...")
    result = get_clean_title(dirty_html)
    
    print("\n📊 --- 清洗结果 ---")
    print(f"提取出的完美标题: |{result}|") # 用竖线包起来，方便肉眼看清两边还有没有空格