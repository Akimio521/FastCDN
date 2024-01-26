import re
import os
import zipfile
import requests
import subprocess
import json
import pandas as pd
from datetime import datetime

def is_valid_ipv4(ip):
    pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
    if pattern.match(ip):
        return True
    else:
        # Check if the input is in CIDR notation
        cidr_pattern = re.compile(r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(\d+)$")
        if cidr_pattern.match(ip):
            return True
        else:
            return False

def update_ips(): 
    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")

    current_date = datetime.now().strftime("%Y%m%d")
    latest_ips_folder = os.path.join("./tmp", current_date)

    if os.path.exists(latest_ips_folder):
        print("已获取今日最新IP，无需重新下载")
    else:
        print("开始下载最新IP列表...")
        if not os.path.exists(latest_ips_folder):
            os.makedirs(latest_ips_folder)

        # 官方IP
        print("开始下载官方IP列表...")
        response = requests.get("https://cdn.jsdelivr.net/gh/XIU2/CloudflareSpeedTest@master/ip.txt")
        with open(os.path.join(latest_ips_folder, 'cf_ip.txt'), "wb") as file:
            file.write(response.content)

        # 反代IP
        print("开始下载反代IP列表...")
        response = requests.get("https://zip.baipiao.eu.org/")
        with open("./tmp/reverse_proxy_ips.zip", "wb") as file:
            file.write(response.content)

        with zipfile.ZipFile('./tmp/reverse_proxy_ips.zip', 'r') as archive:
            archive.extractall(latest_ips_folder)

        valid_ips = []

        for file_name in os.listdir(latest_ips_folder):
            if file_name.endswith('.txt'):
                with open(os.path.join(latest_ips_folder, file_name), 'r') as infile:
                    for line in infile:
                        if line=="\n":
                            continue
                        ip = line.strip()
                        if is_valid_ipv4(ip):
                            valid_ips.append(ip)
        
        if os.path.exists('./tmp/ipv4.txt'):
            os.remove('./tmp/ipv4.txt')

        with open('./tmp/ipv4.txt', 'w') as outfile:
            outfile.write('\n'.join(valid_ips))
        print("所有IP已保存到./tmp/ipv4.txt")

def cloudflarespeedtest(command):
    print("测速中...")
    subprocess.run(command)
    print("测试完成")

def update_dns(email, global_api_key, zone_id, domain, domain_id, ip):
    print("更新DNS记录中...")
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": global_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": domain,
        "content": ip,
        "ttl": 60,
        "proxied": False
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{domain_id}"
    response = requests.put(url, headers=headers, data=json.dumps(data))
    print(response.json())

def get_domain_id(email:str, global_api_key:str, zone_id:str, domain:str):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records?page=1&per_page=20&order=type&direction=asc"
    headers = {
        "X-Auth-Email": email,
        "X-Auth-Key": global_api_key,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    domains_details = response.json()
    results = domains_details.get("result")

    for result in results:
        if domain == result.get("name"):
            domain_id = result.get("id")
            #print(f"{domain}的域名id为：{domain_id}")
    return domain_id