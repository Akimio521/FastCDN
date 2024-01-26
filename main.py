import os
import yaml
import json
import pandas as pd
import time

from version import APP_VERSION
from FastCDN import update_ips, cloudflarespeedtest, update_dns

def main():
    tmp_path="./tmp"
    ipv4_path = tmp_path + "/ipv4.txt"
    csv_path = tmp_path + "/result.csv"
    config_path = "./config/config.yaml"

    update_ips(tmp_path, ipv4_path)
    with open(config_path, "r", encoding="utf-8") as file:
        config_data = yaml.safe_load(file)

    #获取CloudFlare账号信息
    email = config_data["setting"]["account"]["email"]
    global_api_key = config_data["setting"]["account"]["global_api_key"]
    zone_id = config_data["setting"]["account"]["zone_id"]
    #获取CFST信息1
    n = config_data["setting"]["CFST"]["n"]
    t = config_data["setting"]["CFST"]["t"]
    dn = config_data["setting"]["CFST"]["dn"]
    dt = config_data["setting"]["CFST"]["dt"]
    tp = config_data["setting"]["CFST"]["tp"]
    url = config_data["setting"]["CFST"]["url"]
    tl = config_data["setting"]["CFST"]["tl"]
    tll = config_data["setting"]["CFST"]["tll"]
    tlr = config_data["setting"]["CFST"]["tlr"]
    sl = config_data["setting"]["CFST"]["sl"]
    #获取CFST信息2
    speed_test_data = config_data["SpeedTest"]

    round = len(speed_test_data)
    infomation_speedtest_setting = f"""一共需要测速{round}次：
{'='*65}
测试参数：
延迟测速线程数：{n}线程
延迟测速次数：{t}次
下载测速数量：{dn}次
下载测速时间：{dt}秒
测速端口：{tp}
测速地址：{url}
平均延迟上限：{tl}ms
平均延迟下限：{tll}ms
丢包几率上限：{tlr}
下载速度下限：{sl}
"""
    print(infomation_speedtest_setting)

    round_count = 1
    for key, value in speed_test_data.items():
        print(f"{'='*65}\n开始测试{key}\n正在测试第{round_count}轮，总计{round}轮\n{'='*65}")

        domain = value["domain"]
        cfcolo = value["cfcolo"]

        command = f"./CloudflareST -f {ipv4_path} -o {csv_path} -p 0 -httping -cfcolo {cfcolo} -n {n} -t {t} -dn {dn} -dt {dt} -tp {tp} -url {url} -tl {tl} -tll {tll} -tlr {tlr} -sl {sl}"
        cloudflarespeedtest(command)

        if not os.path.exists(csv_path):
            print(f"{csv_path}不存在,已跳过更新")
        else:
            df = pd.read_csv(csv_path, encoding="utf-8")
            fastest_ip_row = df.loc[df["下载速度 (MB/s)"].idxmax()]
            fastest_ip = fastest_ip_row["IP 地址"]
            fastest_ip_loss_rate = fastest_ip_row["丢包率"]
            fastest_ip_delay = fastest_ip_row["平均延迟"]
            fastest_ip_speed = fastest_ip_row["下载速度 (MB/s)"]

            infomation_speedtest_result = f"""{key}已测速完毕：
下载速度最快的IP地址是：{fastest_ip}
丢包率：{fastest_ip_loss_rate}
平均延迟：{fastest_ip_delay}ms
下载速度：{fastest_ip_speed}MB/s
"""
            print(infomation_speedtest_result)
            update_dns(email, global_api_key, zone_id, domain, fastest_ip)
            os.remove(csv_path)
        round_count += 1

if __name__ == '__main__':

    print(f"当前的APP版本是：{APP_VERSION}")

    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
    os.environ.pop("http_proxy", None)
    os.environ.pop("https_proxy", None)

    main()

    print("10秒后自动退出程序")
    time.sleep(10)
