from FastCDN import get_domain_id

if __name__ == '__main__':
    email = input("请输入你的CloudFlare账户邮箱：")
    global_api_key = input("请输入你的CloudFlare账户Global API令牌：")
    zone_id = input("请输入你的CloudFlare域名的zone_id：")
    domain = input("请输入你的CloudFlare子域名：")

    domain_id = get_domain_id(email, global_api_key, zone_id, domain)
    print(f"{domain}的域名id为：{domain_id}")