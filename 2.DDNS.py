#if you successfully get your info from Cloudflare from Step 1, you can go ahead into Step 2.
#This python code is to get your current IP address and then get cloudflare to update DNS address via API.
import requests
import os

def get_ip_from_ipify():
    return requests.get('https://api.ipify.org').text

# 获取当前公共IP地址
current_ip_address = get_ip_from_ipify()
print(f"当前IP地址: {current_ip_address}")

# 如果成功获取了IP地址
if current_ip_address:
    # 尝试读取上次的IP地址
    last_ip_file = 'last_ip.txt'
    if os.path.exists(last_ip_file):
        with open(last_ip_file, 'r') as file:
            last_ip_address = file.read().strip()
    else:
        last_ip_address = None

    # if the IP address change or 1st running
    if current_ip_address != last_ip_address:
        # SOCKS5 info, you may have to use the proxy to connect
        #proxies = {
            #"http": "socks5h://127.0.0.1:6152",
            #"https": "socks5h://127.0.0.1:6152"
        #}

        # 更新Cloudflare DNS
        CLOUDFLARE_API_ENDPOINT = "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/dns_records/YOUR_DNS_RECORD_ID"
        CLOUDFLARE_API_KEY = "YOUR_API_KEY"
        CLOUDFLARE_EMAIL = "YOUR_EMAIL"

        headers = {
            "X-Auth-Email": CLOUDFLARE_EMAIL,
            "X-Auth-Key": CLOUDFLARE_API_KEY,
            "Content-Type": "application/json"
        }

        data = {
            "type": "A",
            "name": "YOUR_DOMAIN_NAME",
            "content": current_ip_address,
            "ttl": 120,
            "proxied": False
        }

        response = requests.put(CLOUDFLARE_API_ENDPOINT, headers=headers, json=data)
        #if you use the proxy to CloudFlare, pls use below code:
        #response = requests.put(CLOUDFLARE_API_ENDPOINT, headers=headers, json=data, proxies=proxies)
        if response.status_code == 200:
            print("Updated Cloudflare DNS successfully!")
            # 保存新的IP地址
            with open(last_ip_file, 'w') as file:
                file.write(current_ip_address)
        else:
            print(f"Update fail, code: {response.status_code}, 信息: {response.text}")
    else:
        print("No changes on IP address, no update")
