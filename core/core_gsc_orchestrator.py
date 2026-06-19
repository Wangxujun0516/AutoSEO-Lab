import os
import sys
import json
import urllib.request
import urllib.parse
import argparse
from datetime import date, timedelta

# ===========================================================================
# 1. 环境强插：强行绑定本地 Clash 混合代理端口
# ===========================================================================
PROXY_PORT = 3067
os.environ["http_proxy"] = f"http://127.0.0.1:{PROXY_PORT}"
os.environ["https_proxy"] = f"http://127.0.0.1:{PROXY_PORT}"
os.environ["HTTP_PROXY"] = f"http://127.0.0.1:{PROXY_PORT}"
os.environ["HTTPS_PROXY"] = f"http://127.0.0.1:{PROXY_PORT}"

# ===========================================================================
# 2. 身份凭证安全加载与自动刷新（OAuth2 底层握手）
# ===========================================================================
def get_authenticated_token():
    """从本地 token.json 中读取访问令牌。若过期则通过代理自动完成后台刷新"""
    # 支持从多个可能路径加载 token.json
    possible_paths = [
        "token.json",
        "core/token.json",
        os.path.join(os.path.dirname(__file__), "token.json")
    ]
    
    token_path = None
    for path in possible_paths:
        if os.path.exists(path):
            token_path = path
            break
    
    if not token_path:
        print(f"[!] 找不到凭证文件: token.json。请确保您已经完成了浏览器授权。")
        print(f"[!] 尝试搜索路径: {possible_paths}")
        sys.exit(1)
        
    with open(token_path, "r") as f:
        token_data = json.load(f)
        
    # 尝试调用系统环境里现有的 google-auth 逻辑进行静默刷新
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        
        creds = Credentials.from_authorized_user_info(token_data)
        if creds and creds.expired and creds.refresh_token:
            print("[*] Access token expired. Attempting background refresh via proxy...")
            creds.refresh(Request())
            # 写回本地缓存
            with open(token_path, "w") as f:
                f.write(creds.to_json())
            return creds.token
        return creds.token
    except Exception as e:
        # 如果库残缺，直接降级尝试读取硬编码在 JSON 里的临时 token
        access_token = token_data.get("token") or token_data.get("access_token")
        if access_token:
            return access_token
        print(f"[!] 无法刷新令牌，且未找到有效备份。原因: {e}")
        sys.exit(1)

# ===========================================================================
# 3. 核心数据抓取函数（原生大动脉管道）
# ===========================================================================
def fetch_performance(site_url: str = "https://www.henghongrv.com/", days: int = 30, dimension: str = "query"):
    """
    100% 纯原生代理管道抓取 Google Search Console 核心指标
    
    Args:
        site_url: GSC 属性 URL（必须精确匹配 Google 后台注册格式）
        days: 查询天数范围
        dimension: 数据切片维度 - 'query' | 'country' | 'device' | 'page'
    """
    token = get_authenticated_token()
    
    # 动态计算日期区间
    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")

    print(f"\n[*] Connecting via Direct Native Proxy Tunnel...")
    print(f"[*] Target Property : {site_url}")
    print(f"[*] Query Range     : {start_date} → {end_date}")
    print(f"[*] Metric Slice    : grouped by [{dimension}]")

    # 显式组装原生代理处理器
    proxy_handler = urllib.request.ProxyHandler({
        'http': f'http://127.0.0.1:{PROXY_PORT}',
        'https': f'http://127.0.0.1:{PROXY_PORT}'
    })
    opener = urllib.request.build_opener(proxy_handler)

    # 规范化转义目标网址
    encoded_site = urllib.parse.quote_plus(site_url)
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"
    
    request_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": [dimension],  # 动态维度切片
        "rowLimit": 50  # 默认抓取前 50 核心记录
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(
            url=api_url,
            data=json.dumps(request_body).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with opener.open(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            rows = res_data.get("rows", [])
            return rows
            
    except urllib.error.HTTPError as e:
        print(f"\n[!] 谷歌服务器拒绝请求 (HTTP {e.code}): {e.reason}")
        if e.code == 403:
            print("[*] 提示：请确保该账号在 GSC 后台对当前网址格式拥有绝对所有权。")
        sys.exit(1)
    except Exception as e:
        print(f"\n[!] 物理连接异常: {e}")
        sys.exit(1)

# ===========================================================================
# 4. 主控与美化输出排版
# ===========================================================================
def render_output(rows: list, dimension: str):
    """根据不同维度动态渲染输出表格"""
    
    # 维度标题映射
    dimension_headers = {
        "query": "海外买家真实搜索关键词 (Query)",
        "country": "买家来源国家/地区 (Country)",
        "device": "访问设备类型 (Device)",
        "page": "高流量落地页 (Page)"
    }
    
    header_title = dimension_headers.get(dimension, "维度数据")
    
    print("\n" + "=" * 85)
    print(f"{header_title:<40} | {'点击量':<6} | {'曝光量':<6} | {'点击率(CTR)':<10} | {'平均排名':<6}")
    print("-" * 85)
    
    for row in rows:
        key_value = row.get("keys", ["Unknown"])[0]
        clicks = int(row.get("clicks", 0))
        impressions = int(row.get("impressions", 0))
        ctr = float(row.get("ctr", 0.0)) * 100
        position = float(row.get("position", 0.0)) + 1
        
        # 裁剪过长的值防止排版错位
        if len(key_value) > 38:
            key_value = key_value[:35] + "..."
            
        print(f"{key_value:<40} | {clicks:<6} | {impressions:<6} | {ctr:>8.2f}% | {position:>6.1f}")
        
    print("=" * 85)
    print(f"[+] 数据抓取完毕，共成功提取 {len(rows)} 条 [{dimension}] 维度记录！\n")


def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(
        description="Henghong GSC 数据遥测器 - 100% 原生代理管道",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python core_gsc_orchestrator.py                     # 默认: query 维度，30 天
  python core_gsc_orchestrator.py --dimension country # 测试国家流量分布
  python core_gsc_orchestrator.py --dimension device  # 测试设备类型分布
  python core_gsc_orchestrator.py --days 60           # 扩展到 60 天范围
"""
    )
    parser.add_argument("--dimension", "-d", default="query", 
                        choices=["query", "country", "device", "page"],
                        help="数据切片维度 (default: query)")
    parser.add_argument("--days", type=int, default=30,
                        help="查询天数范围 (default: 30)")
    parser.add_argument("--site", default="https://www.henghongrv.com/",
                        help="GSC 属性 URL (必须精确匹配 Google 后台格式)")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("        [HENGHONG INTELLIGENT EQUIPMENT - GOOGLE SEO ORCHESTRATOR]        ")
    print("=" * 70)
    
    # 执行数据抓取
    rows = fetch_performance(site_url=args.site, days=args.days, dimension=args.dimension)
    
    if not rows:
        print(f"\n[!] 成功连接，但在指定的日期范围内，该站点在 [{args.dimension}] 维度没有任何数据记录。")
        return

    render_output(rows, args.dimension)

if __name__ == "__main__":
    main()