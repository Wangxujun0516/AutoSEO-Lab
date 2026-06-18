import time

dirty_html_list = [
    "<html><title>  12V Electric Jacks Capacity | Henghong </title></html>",
    "<html>\n<TITLE>\n   Hydraulic Valve Durability Report   \n</TITLE>\n</html>",
    "<html><TiTlE>B2B Sourcing Guide 2026</title></html>",
    "<html>没有写标题标签的坏网页</html>"
]

def clean_single_html(html_content: str) -> str:
    html_lower = html_content.lower()
    start_tag, end_tag = "<title>", "</title>"
    if start_tag in html_lower and end_tag in html_lower:
        start_index = html_lower.find(start_tag) + len(start_tag)
        end_index = html_lower.find(end_tag)
        return html_content[start_index:end_index].strip()
    return "ERROR: Missing <title> tag!"

# ==========================================
# 核心升级：带文件写入的流水线
# ==========================================
def run_cleaner_to_file(html_box: list, output_filename: str) -> None:
    total_tasks = len(html_box)
    print(f"🏭 落地流水线启动！成品将保存至: {output_filename}\n" + "="*50)
    
    # 💡 open(..., "w", encoding="utf-8") 表示以“写入(Write)”模式打开或新建一个文件
    # with 语句是 Python 的大招，它叫上下文管理器。有了它，哪怕代码中途报错，Python 也会在后台默默把文件安全关闭，绝对不会损坏硬盘数据。
    with open(output_filename, "w", encoding="utf-8") as f:
        
        # 先在文件最开头写一行硬核的“表头/标题栏”
        f.write("--- 2026 SEO Title Extraction Report ---\n\n")
        
        for index, raw_html in enumerate(html_box, start=1):
            print(f"⚙️ 正在加工第 [{index}/{total_tasks}] 件并写入本地...")
            
            clean_result = clean_single_html(raw_html)
            
            # ✍️ 将成品塞进文件里。\n 表示换行，让数据整齐排列
            f.write(f"Task [{index}/{total_tasks}]: {clean_result}\n")
            
            if index < total_tasks:
                time.sleep(0.5)
                
    print("="*50 + f"\n🎉 恭喜！本地文件【{output_filename}】已成功生成，请去左侧目录树查看！")

if __name__ == "__main__":
    # 指定输出的文件名叫 clean_titles.txt
    run_cleaner_to_file(dirty_html_list, "clean_titles.txt")