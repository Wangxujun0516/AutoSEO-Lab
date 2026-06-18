import time

# ==========================================
# 1. 模拟从前线抓回来的“脏数据”集装箱（List 列表）
# ==========================================
# 里面夹杂了：换行符 \n、大写标签 <TITLE>、首尾巨长的空格
dirty_html_list = [
    "<html><title>  12V Electric Jacks Capacity | Henghong </title></html>",
    "<html>\n<TITLE>\n   Hydraulic Valve Durability Report   \n</TITLE>\n</html>",
    "<html><TiTlE>B2B Sourcing Guide 2026</title></html>",
    "<html>没有写标题标签的坏网页</html>" # 这是一个故意捣乱的脏数据
]

# ==========================================
# 2. 核心加工厂：单件清洗函数（昨天的内功）
# ==========================================
def clean_single_html(html_content: str) -> str:
    """接收一段HTML，洗出一个干净的标题。如果找不到，返回定位错误。"""
    html_lower = html_content.lower()
    start_tag = "<title>"
    end_tag = "</title>"
    
    if start_tag in html_lower and end_tag in html_lower:
        start_index = html_lower.find(start_tag) + len(start_tag)
        end_index = html_lower.find(end_tag)
        # 去原版账本里切片，并用 .strip() 拔掉两边的空格换行
        return html_content[start_index:end_index].strip()
    
    return "ERROR: Missing <title> tag!"

# ==========================================
# 3. 总控制室：批量流水线函数（今天的合体技）
# ==========================================
def run_cleaner_pipeline(html_box: list) -> None:
    """遍历集装箱，带上计数器，排着队清洗所有数据。"""
    total_tasks = len(html_box)
    print(f"🏭 标题清洗流水线启动！检测到待处理任务数：{total_tasks}\n" + "="*50)
    
    # 用 enumerate 自动数数 (1, 2, 3...)
    for index, raw_html in enumerate(html_box, start=1):
        print(f"⚙️ 正在加工第 [{index}/{total_tasks}] 件原材料...")
        
        # 调用前面的加工厂，拿到洗干净的结果
        clean_result = clean_single_html(raw_html)
        
        print(f"✨ 产出成品: {clean_result}")
        
        # 模拟流水线传送带的微小延迟，顺便打印分割线
        if index < total_tasks:
            time.sleep(0.5)
            print("-" * 30)
            
    print("="*50 + "\n🎉 全线完工！所有脏数据清洗完毕。")

# ==========================================
# 4. 触发开关
# ==========================================
if __name__ == "__main__":
    run_cleaner_pipeline(dirty_html_list)