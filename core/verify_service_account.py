import httplib2
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# 💡 核心安全网络修复：直接在这里解开，强制防范 WinError 10061 代理死锁
# for key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"):
#     os.environ.pop(key, None)
# os.environ['NO_PROXY'] = 'www.googleapis.com,accounts.google.com,oauth2.googleapis.com'

def get_token_or_verify(action="GET_TOKEN"):
    SCOPES = ['https://www.googleapis.com/auth/siteverification']
    KEY_FILE = 'credentials.json'
    
    # 🎯 关键修正：优先从环境变量读取 SITE_URL，如果读不到，才默认用 blogx 样板站
    target_site = os.environ.get("SITE_URL", "https://web.blogx.de5.net/")
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    
    if action == "GET_TOKEN":
        # 💡 第一步：向谷歌索要验证 meta 标签内容
        api_endpoint = f"https://www.googleapis.com/siteVerification/v1/token"
        payload = {
            "verificationMethod": "META",
            "site": { "identifier": target_site, "type": "SITE" }
        }
        print(f"📡 正在向谷歌索要服务账号对 【{target_site}】 的专属验证 Meta 标签...")
        response, content = http.request(api_endpoint, method="POST", body=json.dumps(payload), headers={'Content-Type': 'application/json'})
        print(json.dumps(json.loads(content.decode('utf-8')), indent=2))
        
    elif action == "VERIFY":
        # 💡 第三步：塞好标签后，让谷歌去检查
        api_endpoint = "https://www.googleapis.com/siteVerification/v1/webResource?verificationMethod=META"
        payload = { "site": { "identifier": target_site, "type": "SITE" } }
        print(f"📡 正在通知谷歌检查【{target_site}】上的 Meta 标签，激活所有权...")
        response, content = http.request(api_endpoint, method="POST", body=json.dumps(payload), headers={'Content-Type': 'application/json'})
        print(json.dumps(json.loads(content.decode('utf-8')), indent=2))

if __name__ == "__main__":
    # 🌟 今天我们要接管新网站，我们需要“先运行第一步”！
    # 拿到令牌并在恒宏后台加好后，再把第一步注释掉，解开第二步。
    
    # get_token_or_verify("GET_TOKEN")
    get_token_or_verify("VERIFY")