import os
import json
import urllib.request

PROXY_PORT = 3067
os.environ["http_proxy"] = f"http://127.0.0.1:{PROXY_PORT}"
os.environ["https_proxy"] = f"http://127.0.0.1:{PROXY_PORT}"

try:
    # 1. 直接读取你之前秒速刷新的现成 token
    token_path = "token.json"
    if not os.path.exists(token_path):
        # 尝试去上级目录找
        token_path = "../token.json"
        
    with open(token_path, "r") as f:
        token_data = json.load(f)
    
    access_token = token_data.get("token") or token_data.get("access_token")
    if not access_token:
        raise Exception("token.json 中未找到有效 token，请确保该文件在当前目录下。")

    # 2. 设置原生代理处理器
    proxy_handler = urllib.request.ProxyHandler({
        'http': f'http://127.0.0.1:{PROXY_PORT}',
        'https': f'http://127.0.0.1:{PROXY_PORT}'
    })
    opener = urllib.request.build_opener(proxy_handler)

    # 3. 终极探测：向谷歌请求你账号下所有认账的站点属性格式
    list_url = "https://www.googleapis.com/webmasters/v3/sites"
    req = urllib.request.Request(
        url=list_url,
        headers={"Authorization": f"Bearer {access_token}"},
        method='GET'
    )

    print("[*] 正在通过原生代理大动脉读取您的 GSC 站点列表...")
    with opener.open(req, timeout=10) as res:
        print("\n📡 【成功拿到谷歌底层真实的站点属性列表！】 📡")
        print(json.dumps(json.loads(res.read().decode('utf-8')), indent=4))

except Exception as e:
    print(f"\n[!] 探测失败，原因: {e}")