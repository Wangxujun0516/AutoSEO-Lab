import httplib2
import json
from oauth2client.service_account import ServiceAccountCredentials

def grant_myself_permission():
    # 1. 声明我们需要修改站点所有权的 API 范围
    SCOPES = ['https://www.googleapis.com/auth/siteverification']
    KEY_FILE = 'credentials.json'
    
    try:
        # 2. 使用你的凭证进行认证
        credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, scopes=SCOPES)
        http = credentials.authorize(httplib2.Http())
        
        # 3. 构造请求：这次我们用标准的 POST 或者是经过谷歌最新规范处理的 API
        # 注意：这里的 id 是转义后的二级域名网址
        target_id = "https://web.blogx.de5.net/"
        api_endpoint = "https://www.googleapis.com/siteVerification/v1/webResource"
        
        payload = {
            "site": {
                "identifier": target_id,
                "type": "SITE"
            },
            # 💡 补上谷歌要的这行关键参数：声明验证类型
            # 常见值有: "DNS_TXT", "FILE", "META", "ANALYTICS"
            # 我们先尝试用通用且继承度最高的 "DNS_TXT" 或者是你之前主账号验证过的方法
            "verificationMethod": "DNS_TXT" 
        }
        print(f"📡 正在尝试通过 Python API 注册站点所有权...")
        response, content = http.request(
            api_endpoint, 
            method="POST", 
            body=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status == 200:
            print("🎉 奇迹发生了！服务账号成功完成了自验证！")
            print(json.dumps(json.loads(content.decode('utf-8')), indent=2))
        else:
            print(f"❌ 还是不行，状态码: {response.status}")
            print(f"详情: {content.decode('utf-8')}")
            
    except Exception as e:
        print(f"💥 发生异常: {str(e)}")

if __name__ == "__main__":
    grant_myself_permission()