#this is a python script to get your id info from cloudflare.
import requests

# setting proxy info, you may need a proxy to connect with Cloudflare
#proxies = {
    #"http": "socks5h://127.0.0.1:6152",
    #"https": "socks5h://127.0.0.1:6152"
#}

# Cloudflare 认证信息
CLOUDFLARE_API_ENDPOINT = "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/dns_records"
CLOUDFLARE_API_KEY = "Your API key in Cloudflare"
CLOUDFLARE_EMAIL = "Your email address login into Cloudflare"

headers = {
    "X-Auth-Email": CLOUDFLARE_EMAIL,
    "X-Auth-Key": CLOUDFLARE_API_KEY,
    "Content-Type": "application/json"
}

# 使用代理发起请求
response = requests.get(CLOUDFLARE_API_ENDPOINT, headers=headers)
#if you use a proxy to connect cloudflare pls use below code
#response = requests.get(CLOUDFLARE_API_ENDPOINT, headers=headers, proxies=proxies)

# 解析并打印响应内容
response_data = response.json()

# 检查是否成功获取数据
if response_data['success']:
    results = response_data['result']
    for idx, result in enumerate(results, 1):
        print(f"Record {idx}:")
        for key, value in result.items():
            print(f"  {key}: {value}")
        print('-' * 40)  # 打印分隔线
else:
    print("Failed to retrieve data.")
