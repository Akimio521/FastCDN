import requests,json

email = input("请输入你的CloudFlare账户邮箱：")
global_api_key = input("请输入你的CloudFlare账户Global API令牌：")
zone_id = input("请输入你的CloudFlare域名的zone_id：")
domain = input("请输入你的CloudFlare域名：")

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
        print(f"{domain}的域名id为：{domain_id}")