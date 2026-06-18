import httplib2
import json
import xml.etree.ElementTree as ET
import urllib.request
from oauth2client.service_account import ServiceAccountCredentials

def get_urls_from_sitemap(sitemap_url):
    """从网站的 sitemap.xml 中解析出所有的 URL"""
    urls = []
    try:
        # 下载 sitemap 内容
        req = urllib.request.Request(sitemap_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        
        # 解析 XML
        root = ET.fromstring(xml_data)
        
        # XML 的命名空间处理
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # 寻找所有的 <loc> 标签
        for url_tag in root.findall('ns:url', namespace):
            loc_tag = url_tag.find('ns:loc', namespace)
            if loc_tag is not None and loc_tag.text:
                urls.append(loc_tag.text.strip())
                
        print(f"📂 成功从 Sitemap 中解析出 {len(urls)} 个网址。")
        return urls
    except Exception as e:
        print(f"❌ 解析 Sitemap 失败: {str(e)}")
        return []

def batch_submit(sitemap_url):
    # 1. 提取所有网址
    target_urls = get_urls_from_sitemap(sitemap_url)
    if not target_urls:
        return

    # 2. 谷歌 API 认证
    SCOPES = ['https://www.googleapis.com/auth/indexing']
    KEY_FILE = 'credentials.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    api_endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    # 3. 循环批量推送
    for url in target_urls:
        print(f"🚀 正在推送: {url} ...")
        payload = {
            "url": url,
            "type": "URL_UPDATED"
        }
        try:
            response, content = http.request(
                api_endpoint, 
                method="POST", 
                body=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            if response.status == 200:
                print(f"  ✅ 推送成功！")
            else:
                print(f"  ❌ 推送失败，错误码: {response.status}，详情: {content.decode('utf-8')}")
        except Exception as e:
            print(f"  💥 请求发生异常: {str(e)}")

if __name__ == "__main__":
    # 🎯 换成你最新的独立域名 Sitemap 地址
    MY_SITEMAP = "https://www.henghongrv.com/sitemap.xml" 
    batch_submit(MY_SITEMAP)