import requests,platform,zipfile,os
from tarfile import TarFile

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# 获取系统信息
system = platform.system()
machine = platform.machine()

# 发送GET请求获取release信息
url = "https://api.github.com/repos/XIU2/CloudflareSpeedTest/releases/latest"
response = requests.get(url)
data = response.json()

# 根据系统和架构选择下载目标
# MAC x86
if system == "Darwin" and machine == "x86_64":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_darwin_amd64.zip" in asset["name"]][0]
# MAC ARM
elif system == "Darwin" and machine == "arm64":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_darwin_arm64.zip" in asset["name"]][0]
# Linux 32位
elif system == "Linux" and machine == "i686":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_386.tar.gz" in asset["name"]][0]
# Linux 64位
elif system == "Linux" and machine.endswith("64") and platform.architecture()[0] == "64bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_amd64.tar.gz" in asset["name"]][0]
# Linux ARM 64位
elif system == "Linux" and machine.startswith("arm") and platform.architecture()[0] == "64bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_arm64.tar.gz" in asset["name"]][0]
# Linux ARM 32位 v5
elif system == "Linux" and machine.startswith("armv5") and platform.architecture()[0] == "32bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_armv5.tar.gz" in asset["name"]][0]
# Linux ARM 32位 v6
elif system == "Linux" and machine.startswith("armv6") and platform.architecture()[0] == "32bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_armv6.tar.gz" in asset["name"]][0]
# Linux ARM 32位 v7
elif system == "Linux" and machine.startswith("armv7") and platform.architecture()[0] == "32bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_armv7.tar.gz" in asset["name"]][0]
# Linux Mips 32位
elif system == "Linux" and machine.startswith("mips") and not machine.endswith("le") and platform.architecture()[0] == "32bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_mips.tar.gz" in asset["name"]][0]
# Linux Mips 64位
elif system == "Linux" and machine.startswith("mips") and not machine.endswith("le") and platform.architecture()[0] == "64bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_mips64.tar.gz" in asset["name"]][0]
# Linux Mipsle 32位
elif system == "Linux" and machine.startswith("mips") and machine.endswith("le") and platform.architecture()[0] == "32bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_mipsle.tar.gz" in asset["name"]][0]
# Linux Mipsle 64位
elif system == "Linux" and machine.startswith("mips") and machine.endswith("le") and platform.architecture()[0] == "64bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_linux_mips64le.tar.gz" in asset["name"]][0]
# Windows 32位
elif system == "Windows" and platform.architecture()[0] == "32bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_windows_386.zip" in asset["name"]][0]
# Windows 64位
elif system == "Windows" and platform.architecture()[0] == "64bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_windows_amd64.zip" in asset["name"]][0]
# Windows ARM 64位
elif system == "Windows" and machine.startswith("arm") and platform.architecture()[0] == "64bit":
    download_url = [asset["browser_download_url"] for asset in data["assets"] if "CloudflareST_windows_arm64.zip" in asset["name"]][0]

# 下载CFST程序
if download_url:
    print("选择的下载链接为:", download_url)
    # 下载文件到当前目录
    file_name = download_url.split("/")[-1]
    with open(file_name, "wb") as file:
        response = requests.get(download_url)
        file.write(response.content)
    print("文件下载完成")

    # 解压文件
    if file_name.endswith(".zip"):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall("./")
        print("文件解压完成")
    elif file_name.endswith(".tar.gz"):
        with TarFile.open(file_name, 'r:gz') as tar_ref:
            tar_ref.extractall("./")
        print("文件解压完成")
    else:
        print("未知的文件格式，无法解压")
else:
    print("未找到匹配的下载文件")

# 删除不必要文件
delete_file("cfst_3proxy.bat")
delete_file("cfst_hosts.bat")
delete_file("ip.txt")
delete_file("ipv6.txt")
delete_file("使用+错误+反馈说明.txt")
