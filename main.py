import os
import yaml
import json
import pandas as pd
import time

from version import APP_VERSION
from FastCDN import update_ips, cloudflarespeedtest, update_dns

def main():
    update_ips()
    with open("./config/config.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    setting = data["setting"]["account"]
    globals().update(setting)
    globals().update(data["setting"]["CFST"])
    speed_test_data = data["SpeedTest"]
    round = len(speed_test_data)
    print(f"一共需要测速{round}次\n测试参数：\n延迟测速线程数：{n}线程\n延迟测速次数：{t}次\n下载测速数量：{dn}次\n下载测速时间：{dt}秒\n测速端口：{tp}\n测速地址：{url}\n平均延迟上限：{tl}ms\n平均延迟下限：{tll}ms\n丢包几率上限：{tlr}\n下载速度下限：{sl}")

    round_count = 1
    for key, value in speed_test_data.items():
        print(f"{'='*65}\n开始测试{key}\n正在测试第{round_count}轮，总计{round}轮\n{'='*65}")

        domain = value["domain"]
        domain_id = value["domain_id"]
        cfcolo = value["cfcolo"]

        command = f"./CloudflareST -f ./tmp/ipv4.txt -o ./tmp/result.csv -p 0 -httping -cfcolo {cfcolo} -n {n} -t {t} -dn {dn} -dt {dt} -tp {tp} -url {url} -tl {tl} -tll {tll} -tlr {tlr} -sl {sl}"
        cloudflarespeedtest(command)

        if not os.path.exists("./tmp/result.csv"):
            print("./tmp/result.csv不存在,已跳过更新")
        else:
            df = pd.read_csv("./tmp/result.csv", encoding="utf-8")
            fastest_ip_row = df.loc[df["下载速度 (MB/s)"].idxmax()]
            fastest_ip = fastest_ip_row["IP 地址"]
            print(f"{key}下载速度最快的IP地址是:{fastest_ip}")
            update_dns(email, global_api_key, zone_id, domain, domain_id, fastest_ip)
            os.remove("./tmp/result.csv")
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
